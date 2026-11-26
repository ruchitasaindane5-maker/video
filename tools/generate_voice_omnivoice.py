#!/usr/bin/env python3
"""
Multi-voice Hinglish storytelling generator powered by OmniVoice
(https://github.com/k2-fsa/OmniVoice).

Reads a plain-text voice script with [SPEAKER] tags, synthesises each
line with that speaker's voice-design `instruct`, and writes one WAV
per line plus a concatenated full-track WAV.

Usage:
    python tools/generate_voice_omnivoice.py \
        --script playlist/short/voice-script.txt \
        --out audio/short

VoiceStudio alternative (GUI):
    1. Install VoiceStudio (https://github.com/debpalash/voicestudio)
    2. Open it, import playlist/<ep>/voice-script.txt
    3. Assign each [SPEAKER] tag to a voice-design preset (table below)
    4. Narrate → Export → save to audio/<ep>/

Speaker -> OmniVoice instruct (voice design):
    NARRATOR  : male, middle-aged, low pitch, warm, Indian accent
    HARISENA  : male, elderly, low pitch, deep, regal, Indian accent
    HISTORIAN : female, middle-aged, clear, articulate, Indian accent

NOTE: First run downloads the k2-fsa/OmniVoice weights from the
Hugging Face Hub (~several GB). If your network blocks huggingface.co,
run this on a machine with Hub access, or use VoiceStudio (which also
uses OmniVoice under the hood).
"""

import argparse
import re
import sys
from pathlib import Path

SPEAKER_INSTRUCTS = {
    "NARRATOR":  "male, middle-aged, low pitch, warm, gentle, Indian accent, storytelling",
    "HARISENA":  "male, elderly, low pitch, deep, regal, slow, Indian accent, ancient orator",
    "HISTORIAN": "female, middle-aged, clear, articulate, measured, Indian accent, historian",
}
DEFAULT_INSTRUCT = "male, middle-aged, warm, Indian accent"
SR_FALLBACK = 24000


def parse_script(path: Path):
    """Yield (speaker, text) for each [TAG] line."""
    pattern = re.compile(r"^\[([A-Z_]+)\]\s*(.+)$")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        m = pattern.match(line)
        if m:
            yield m.group(1), m.group(2).strip()
        else:  # un-tagged line -> narrator
            yield "NARRATOR", line


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--language", default="Hindi", help="OmniVoice language name/code (default: Hindi — Hinglish text mixes Devanagari + Latin English, Hindi is the base)")
    ap.add_argument("--model", default="k2-fsa/OmniVoice")
    ap.add_argument("--speed", type=float, default=1.0)
    args = ap.parse_args()

    if not args.script.exists():
        sys.exit(f"Script not found: {args.script}")

    try:
        import soundfile as sf
        from omnivoice import OmniVoice
    except ImportError as e:
        sys.exit(f"Missing dependency: {e}\nRun: pip install omnivoice torch torchaudio soundfile")

    lines = list(parse_script(args.script))
    print(f"Parsed {len(lines)} lines from {args.script}")

    args.out.mkdir(parents=True, exist_ok=True)

    print(f"Loading {args.model} (first run downloads weights from Hugging Face Hub)...")
    model = OmniVoice.from_pretrained(args.model)
    sr = getattr(model, "sampling_rate", SR_FALLBACK)
    print(f"Model ready. Sampling rate: {sr} Hz")

    wavs = []
    manifest = []
    for i, (speaker, text) in enumerate(lines, 1):
        instruct = SPEAKER_INSTRUCTS.get(speaker, DEFAULT_INSTRUCT)
        print(f"[{i:02d}] {speaker}: {text[:60]}{'...' if len(text) > 60 else ''}")
        audio = model.generate(
            text=text,
            language=args.language,
            instruct=instruct,
            speed=args.speed,
        )[0]
        out_path = args.out / f"{i:02d}-{speaker.lower()}.wav"
        sf.write(str(out_path), audio, sr)
        wavs.append(audio)
        manifest.append((i, speaker, out_path.name, len(audio) / sr))

    # Concatenated master track with 400ms pauses between lines
    import numpy as np
    pause = np.zeros(int(0.4 * sr), dtype=np.float32)
    master = np.concatenate([x for w in wavs for x in (w.astype(np.float32), pause)])
    master_path = args.out / "master.wav"
    sf.write(str(master_path), master, sr)

    print("\nWrote:")
    for i, speaker, name, dur in manifest:
        print(f"  {name:32s} {speaker:10s} {dur:6.1f}s")
    print(f"  {'master.wav':32s} {'ALL':10s} {len(master)/sr:6.1f}s")


if __name__ == "__main__":
    main()
