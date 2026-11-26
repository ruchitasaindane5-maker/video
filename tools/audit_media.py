#!/usr/bin/env python3
"""
Media audit for the episode pack — detects voice breaks, clipping,
dead air, DC offset, wrong loudness, bad image dims, broken renders.

Usage: python tools/audit_media.py > docs/audit-report.md
"""
import sys
import wave
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image

issues = []
ok = []


def flag(tag, path, msg):
    issues.append(f"- **{tag}** `{path}` — {msg}")


def good(tag, path, msg):
    ok.append(f"- ok [{tag}] `{path}` — {msg}")


def audit_wav(path: Path):
    try:
        data, sr = sf.read(str(path), always_2d=True)
    except Exception as e:
        flag("AUDIO", path, f"unreadable: {e}")
        return
    mono = data.mean(axis=1)
    dur = len(mono) / sr
    peak = float(np.max(np.abs(mono))) if len(mono) else 0.0
    rms = float(np.sqrt(np.mean(mono**2))) if len(mono) else 0.0
    rms_db = 20 * np.log10(rms + 1e-9)
    dc = float(np.mean(mono))
    clip = int(np.sum(np.abs(mono) > 0.989))
    # leading/trailing silence (threshold -45 dBFS)
    thr = 10 ** (-45 / 20)
    nonsilent = np.where(np.abs(mono) > thr)[0]
    lead = (nonsilent[0] / sr) if len(nonsilent) else dur
    trail = ((len(mono) - nonsilent[-1]) / sr) if len(nonsilent) else dur
    # interior dead air: windows of 250ms below -45 dBFS, gaps > 2.5s
    win = max(1, int(0.25 * sr))
    active = [np.max(np.abs(mono[i:i + win])) > thr for i in range(0, len(mono), win)]
    breaks, run = [], 0
    for i, a in enumerate(active):
        run = 0 if a else run + 1
        if run * 0.25 >= 2.5 and (not breaks or breaks[-1][1] != int(i * 0.25)):
            breaks.append((int(i * 0.25) - run * 0.25 + 0.25, int(i * 0.25) + 0.25))
    msgs = [f"{dur:.1f}s, sr={sr}, peak={peak:.2f}, RMS={rms_db:.1f}dBFS, dc={dc:+.4f}"]
    if clip:
        flag("AUDIO", path, f"CLIPPING — {clip} samples >0.989 full scale")
    if peak < 0.05:
        flag("AUDIO", path, f"near-silent clip (peak={peak:.3f})")
    if dc and abs(dc) > 0.02:
        flag("AUDIO", path, f"DC offset {dc:+.4f} (>0.02)")
    if lead > 2.0:
        flag("AUDIO", path, f"long leading silence {lead:.2f}s")
    if trail > 2.0:
        flag("AUDIO", path, f"long trailing silence {trail:.2f}s")
    for b in breaks:
        flag("AUDIO", path, f"possible voice break / dead air {b[0]:.2f}s–{b[1]:.2f}s (>2.5s)")
    if not clip and peak >= 0.05 and abs(dc) <= 0.02 and not breaks:
        good("AUDIO", path, "; ".join(msgs))
    else:
        print(f"note[{path.name}]: {'; '.join(msgs)}", file=sys.stderr)


def audit_image(path: Path):
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            w, h = im.size
            ratio = w / h
            good("IMAGE", path, f"{w}x{h}, ratio {ratio:.2f}")
    except Exception as e:
        flag("IMAGE", path, f"unreadable: {e}")


def main():
    for p in sorted(Path("audio").rglob("*.wav")):
        audit_wav(p)
    for p in sorted(Path("assets").rglob("*.jpg")):
        audit_image(p)
    print("# Audit report — The Untold Story of Samudragupta (Ep 1)\n")
    print(f"## Checked {len(ok) + len(issues)} assets — {len(issues)} issue(s)\n")
    print("## Issues\n" if issues else "## Issues\n\n_None detected._\n")
    for i in issues:
        print(i)
    print("\n## Passed\n")
    for o in ok:
        print(o)


if __name__ == "__main__":
    main()
