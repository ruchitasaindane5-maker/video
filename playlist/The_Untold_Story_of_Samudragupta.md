# The Untold Story of Samudragupta — YouTube Playlist

**Channel Playlist Name:** `The Untold Story of Samudragupta`
**Language:** शुद्ध Hindi (Devanagari) — SINGLE FEMALE VOICE (voice-02) in both episodes; all Hinglish assets deleted
**Format:** 1 Full Video (16:9, 8–10 min) + 1 YouTube Short (9:16, ~50 sec) per episode

> This repo is the complete production pack for Episode 1. Scripts, storyboards,
> images, voice scripts, audio previews, and a ready-to-render video pipeline
> using [brag](https://github.com/latent-spaces/brag) (video),
> [OmniVoice](https://github.com/k2-fsa/OmniVoice) + [VoiceStudio](https://github.com/debpalash/voicestudio) (natural human voices).

---

## Episode 1 — Titles

| | Title |
|---|---|
| **Full Video** | The Untold Story of Samudragupta — The King Who Conquered India… Then Gave It Away |
| **Short** | He Conquered India in 40 Years… But Refused to Rule It? 😱 #shorts |

## Playlist Description (copy-paste to YouTube)

```
👑 The Untold Story of Samudragupta

He conquered almost the entire Indian subcontinent. Kings surrendered at his feet.
Yet he didn't keep their kingdoms. He didn't build an empire of fear. He built an empire of respect.

Who was Samudragupta — the Vikramaditya, the poet, the musician, the undefeated king of the Gupta Empire?
This playlist uncovers the story history textbooks never told you — from the Allahabad Pillar inscription
to the gold coins that still shine after 1,600 years.

▶ Episode 1: The Untold Story of Samudragupta (Full Video)
▶ Episode 1 Short: He Conquered India… But Refused to Keep It?

New episodes every week. Subscribe for untold Indian history, told like a story.

#Samudragupta #GuptaEmpire #IndianHistory #UntoldHistory #AncientIndia
```

## Tags (Full Video)

```
Samudragupta, Gupta Empire, ancient India history, Indian history untold,
Chandragupta, Allahabad pillar inscription, Harisena, Vikramaditya,
Indian kings history, Gupta dynasty, Nalanda, Aryabhata, untold story,
history documentary, Indian history in English
```

## Tags (Short)

```
Samudragupta, Gupta Empire, Indian history, ancient India, untold history,
shorts, history shorts, Indian kings, Vikramaditya, Allahabad inscription
```

## Files in this repo

```
playlist/
  short/script.md          ← 50-sec Shorts script (scene-by-scene)
  short/storyboard.md      ← shot list + on-screen text + timing
  short/voice-script.txt   ← plain text for OmniVoice / VoiceStudio
  full/script.md           ← 8–10 min full script (chapters)
  full/storyboard.md       ← shot list + B-roll + timing
  full/voice-script.txt    ← plain text for OmniVoice / VoiceStudio
assets/short/              ← images for Short (9:16)
assets/full/               ← images for Full Video (16:9)
audio/preview/             ← Hinglish multi-voice audio previews (NARRATOR/HARISENA/HISTORIAN)
audio/full/                ← full-episode Hinglish scene lines (Arena TTS; OmniVoice blocked by HF Hub network)
docs/audit-report.md       ← automated media audit (clipping/DC/dead-air/silence/dims) — 37 assets, 0 issues
video/short/samudragupta-short-hindi.mp4 ← Ep 1 Short (Hindi, 65.9s)
video/full/samudragupta-full-hindi.mp4 ← Ep 1 Full (Hindi, 6:53, 413s, 8 chapters incl. 15/15 lines)
video/ep2/                 ← Ep 2 Short (74.5s) + Full (5:21), Hindi
audio/README.md            ← how to regenerate final voices with OmniVoice
tools/
  generate_voice_omnivoice.py  ← multi-voice storytelling with OmniVoice
  make_video.py                ← brag-style slideshow video (ffmpeg)
  README.md                    ← full pipeline instructions
video/short/ video/full/   ← rendered MP4s (when generated)
brag-output-short/ brag-output-full/  ← brag plans + compositions
```

## Quick Start — Render the videos

```bash
# 1) Install tools (once)
pip install imageio-ffmpeg pillow soundfile numpy

# 2) Generate natural human voices (choose ONE)
#    Option A — OmniVoice (recommended, free, local):
pip install omnivoice torch torchaudio soundfile
python tools/generate_voice_omnivoice.py --script playlist/short/voice-script.txt --out audio/short
python tools/generate_voice_omnivoice.py --script playlist/full/voice-script.txt --out audio/full

#    Option B — VoiceStudio desktop app (same OmniVoice engine, GUI):
#    Download from https://github.com/debpalash/voicestudio
#    Import playlist/*/voice-script.txt → Narrate → export WAV per speaker

# 3) Render video (brag-style: images + voice + subtitles + music bed)
python tools/make_video.py --script playlist/short/script.md --assets assets/short --audio audio/short --out video/short/samudragupta-short.mp4 --vertical
python tools/make_video.py --script playlist/full/script.md  --assets assets/full  --audio audio/full  --out video/full/samudragupta-full.mp4

# 4) Upload to YouTube → add to playlist "The Untold Story of Samudragupta"
```

See `tools/README.md` for the full brag + OmniVoice + VoiceStudio workflow.


## Episode 2 — चन्द्रगुप्त द्वितीय (in progress)
**Title (Short):** जिसने Sakas को हमेशा के लिए मिटा दिया… वो था असली विक्रमादित्य? #shorts
**Title (Full):** चन्द्रगुप्त द्वितीय — वह सम्राट जिसने Sakas का अंत किया और 'विक्रमादित्य' बन गया
**Language:** शुद्ध Hindi (Devanagari), SINGLE FEMALE VOICE (voice-02) — कोई Hinglish नहीं
- `playlist/ep2/short/` — script + voice-script (6 scenes) + storyboard
- `playlist/ep2/full/` — script (8 chapters) + voice-script + storyboard
- `audio/preview/ep2-short-hindi-preview.mp3` — Short voice preview (all 6 lines)
- `audio/preview/ep2-full-hindi-preview.mp3` — Full sample preview (Hook + नवरत्न/कालिदास)

**Status: COMPLETE** — audio approved; `video/ep2/ep2-short-hindi.mp4` (74.5s) and `video/ep2/ep2-full-hindi.mp4` (5:21, 321s, 8 chapters) rendered; Devanagari captions verified.
Note: रामगुप्त–ध्रुवदेवी कथा drama "देवीचन्द्रगुप्तम्" से आई है — scripts इसे legend-as-such mark करती हैं; Iron Pillar / नवरत्न / विक्रम संवत् myth corrections included for accuracy.


## Episode 3 — स्कान्दगुप्त और हूण (in progress)
**Title (Short):** वो दीवार जिसने भारत को बचाया — Skandagupta #shorts
**Title (Full):** Skandagupta — वो आखिरी दीवार: हूण जिन्होंने गुप्त साम्राज्य को हिला दिया था (पूरा सच)
**Language:** शुद्ध Hindi (Devanagari), SINGLE FEMALE VOICE (voice-02)
- `playlist/ep3/short/` + `playlist/ep3/full/` — scripts, storyboards, scenes.json
- Short rendered: `video/ep3/ep3-short-hindi.mp4` (67.1s)
- **Status: COMPLETE** — `video/ep3/ep3-full-hindi.mp4` (4:21, 261s) + Short (67.1s) rendered; Hindi, voice-02
