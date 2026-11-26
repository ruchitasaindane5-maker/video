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


def make_caption_overlay(W: int, H: int) -> Image.Image:
    """Dark bottom bar + gold accent line + English brand tag.
    Hindi/Unicode caption text is drawn by ffmpeg drawtext (HarfBuzz) —
    PIL without raqm cannot shape Devanagari."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    vertical = H > W
    bar_h = int(H * (0.14 if vertical else 0.17))
    y0 = H - bar_h
    accent = max(4, H // 240)
    d.rectangle([0, y0, W, H], fill=(8, 6, 4, 165))
    d.rectangle([0, y0, W, y0 + accent], fill=(212, 175, 55, 255))
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

    # caption overlay png (bar + tag only)
    overlay_path = workdir / f"overlay-{idx:02d}.png"
    overlay = make_caption_overlay(W, H)
    overlay.save(overlay_path)

    # caption text file for ffmpeg drawtext (HarfBuzz shapes Devanagari)
    caption_path = workdir / f"caption-{idx:02d}.txt"
    caption_path.write_text(scene.get("text", "").replace("·", "—"), encoding="utf-8")
    vertical = H > W
    bar_h = int(H * (0.14 if vertical else 0.17))
    bar_top = H - bar_h
    fontsize = int(H * (0.036 if vertical else 0.046))
    cap_y = bar_top + (bar_h - fontsize) // 2
    caption_text = scene.get("text", "")
    has_deva = any("\u0900" <= ch <= "\u097f" for ch in caption_text)
    noto_bold = Path(__file__).parent / "fonts" / "NotoSansDevanagari-Bold.ttf"
    if has_deva and noto_bold.exists():
        font_arg = str(noto_bold)  # NotoSansDevanagari has no Latin glyphs — keep Deva captions pure
    else:
        font_arg = FONT_CANDIDATES[0]

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
        f"[0:v]{vf}[bg];[bg][2:v]overlay=0:0[ov];"
        f"[ov]drawtext=fontfile={font_arg}:textfile={caption_path}:"
        f"fontcolor=0xF5E29E:fontsize={fontsize}:x=(w-text_w)/2:y={cap_y}[v];"
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
