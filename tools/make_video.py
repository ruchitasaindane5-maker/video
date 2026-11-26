#!/usr/bin/env python3
"""
Render a scenes.json (see playlist/<ep>/scenes.json) to an MP4 —
the /brag "composition" step for headless environments.

Each scene: Ken Burns zoom on the still image + a PIL-rendered caption
bar (Cinzel-style gold-on-dark) + the scene's Hinglish audio
(NARRATOR/HARISENA/HISTORIAN from OmniVoice or previews), fades, then
concat of all scenes.

Usage:
    python tools/make_video.py --scenes playlist/short/scenes.json \
        --out video/short/samudragupta-short-hinglish.mp4
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import resample_poly


def resample(mono: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    if sr_in == sr_out:
        return mono.astype(np.float32)
    from math import gcd
    g = gcd(sr_in, sr_out)
    return resample_poly(mono, sr_out // g, sr_in // g).astype(np.float32)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf",
]


def get_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def load_scene_audio(files, sr_target=44100):
    """Concat wav files with 400ms gaps; returns (waveform float32 mono, sr)."""
    pause = np.zeros(int(0.4 * sr_target), dtype=np.float32)
    parts = []
    for f in files:
        data, sr = sf.read(f, dtype="float32", always_2d=True)
        mono = data.mean(axis=1)
        if sr != sr_target:
            mono = resample(mono, sr, sr_target)
        parts.append(mono)
        parts.append(pause)
    return np.concatenate(parts), sr_target


def make_caption_overlay(text: str, W: int, H: int) -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    vertical = H > W
    bar_h = int(H * (0.14 if vertical else 0.17))
    y0 = H - bar_h
    # gold accent line
    d.rectangle([0, y0, W, y0 + max(4, H // 240)], fill=(212, 175, 55, 255))
    d.rectangle([0, y0, W, H], fill=(8, 6, 4, 165))
    d.rectangle([0, y0, W, y0 + max(4, H // 240)], fill=(212, 175, 55, 255))
    size = int(H * (0.034 if vertical else 0.046))
    font = get_font(size)
    # wrap text to fit width
    words, lines, cur = text.split(), [], ""
    max_w = int(W * 0.86)
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textbbox((0, 0), trial, font=font)[2] <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    total_h = len(lines) * int(size * 1.35)
    ty = y0 + (bar_h - total_h) // 2 + int(size * 0.15)
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        d.text(((W - tw) / 2, ty), line, font=font, fill=(245, 226, 158, 255))
        ty += int(size * 1.35)
    # small corner tag
    tag_font = get_font(int(H * 0.020))
    d.text((int(W * 0.045), int(H * 0.028)), "THE UNTOLD STORY OF SAMUDRAGUPTA",
            font=tag_font, fill=(212, 175, 55, 220))
    return img


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{res.stderr[-3000:]}")
    return res


def render_scene(idx, scene, W, H, fps, workdir: Path):
    image = Path(scene["image"])
    audio_files = [Path(f) for f in scene["audio"]]
    for f in audio_files:
        if not f.exists():
            sys.exit(f"Missing audio file: {f}")
    if not image.exists():
        sys.exit(f"Missing image: {image}")

    # build scene audio wav
    audio, sr = load_scene_audio([str(f) for f in audio_files])
    hold = float(scene.get("hold", 0.5))
    audio = np.concatenate([audio, np.zeros(int(hold * sr), dtype=np.float32)])
    scene_wav = workdir / f"scene-{idx:02d}.wav"
    sf.write(str(scene_wav), audio, sr)
    dur = len(audio) / sr
    frames = max(1, int(round(dur * fps)))

    # caption overlay png
    overlay_path = workdir / f"overlay-{idx:02d}.png"
    make_caption_overlay(scene.get("text", ""), W, H).save(overlay_path)

    out = workdir / f"scene-{idx:02d}.mp4"
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H},"
        f"scale={W*2}:{H*2},"
        f"zoompan=z='min(zoom+0.0011,1.12)':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={fps},"
        f"fade=t=in:st=0:d=0.35,fade=t=out:st={max(0.0, dur-0.45):.3f}:d=0.45,"
        f"format=yuv420p"
    )
    run([
        FFMPEG, "-y",
        "-loop", "1", "-framerate", str(fps), "-i", str(image),
        "-i", str(scene_wav),
        "-loop", "1", "-framerate", str(fps), "-i", str(overlay_path),
        "-filter_complex",
        f"[0:v]{vf}[bg];[bg][2:v]overlay=0:0[v];"
        f"[1:a]afade=t=in:st=0:d=0.1,afade=t=out:st={max(0.0, dur-0.4):.3f}:d=0.4[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "20", "-preset", "fast",
        "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
        "-shortest", str(out),
    ])
    return out, dur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenes", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    cfg = json.loads(args.scenes.read_text())
    W, H = cfg["resolution"]
    fps = int(cfg.get("fps", 30))
    args.out.parent.mkdir(parents=True, exist_ok=True)

    total = 0.0
    with tempfile.TemporaryDirectory(prefix="brag-render-") as tmp:
        workdir = Path(tmp)
        scene_files = []
        for i, scene in enumerate(cfg["scenes"], 1):
            path, dur = render_scene(i, scene, W, H, fps, workdir)
            scene_files.append(path)
            total += dur
            print(f"scene {i:02d}: {dur:.1f}s -> {path.name}")
        concat = workdir / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in scene_files))
        run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
             "-c", "copy", str(args.out)])
    print(f"\nWrote {args.out}  ({total:.1f}s, {W}x{H}@{fps})")


if __name__ == "__main__":
    main()
