# /brag plan — FULL VIDEO · The Untold Story of Samudragupta (Ep 1)

**Product:** YouTube playlist "The Untold Story of Samudragupta" — Episode 1, full-length
**Tone:** cinematic museum-exhibit documentary (gold/saffron on dark), paced like a premium history channel
**Format:** landscape 1920×1080 @30fps · ~8–9 min
**Voice:** Hinglish, 3 storytelling voices — NARRATOR (voice-00), HARISENA (voice-01), HISTORIAN (voice-02)
**Music:** low tanpura drone, ducked −18dB (dropped in this render; add before upload)
**Voice pipeline:** Arena/Gemini TTS preview → final production via OmniVoice (`tools/generate_voice_omnivoice.py --script playlist/full/voice-script.txt --out audio/full`) or VoiceStudio GUI

## Chapter storyboard

| # | Time | Chapter | Visual | Motion | On-screen text | Voice |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:45 | Hook | `assets/full/01-hook-map.jpg` | zoom-in | HE CONQUERED INDIA… THEN GAVE IT BACK | NARRATOR |
| 2 | 0:45–1:40 | Chosen Prince | `assets/full/02-chosen-prince.jpg` | push-in | CHOSEN, NOT BORN | NARRATOR + HARISENA |
| 3 | 1:40–3:20 | Digvijaya | `assets/full/03-digvijaya-army.jpg` | pan across army | CONQUEST IN EVERY DIRECTION | NARRATOR + HARISENA |
| 4 | 3:20–5:00 | Poet-King | `assets/full/04-poet-king-veena.jpg` | Ken Burns | THE POET-KING · VEENA ON GOLD | NARRATOR + HARISENA |
| 5 | 5:00–6:40 | Untold Secret | `assets/full/05-restored-thrones.jpg` | crossfade | HE RESTORED THEIR THRONES | NARRATOR + HISTORIAN |
| 6 | 6:40–7:50 | Vikramaditya | `assets/full/06-vikramaditya-sun.jpg` | sunrise feel | VIKRAMADITYA · SUN OF KINGS | NARRATOR |
| 7 | 7:50–8:30 | Outro | `assets/full/07-allahabad-pillar.jpg` | pull-back | EPISODE 2 COMING SOON | NARRATOR |

## Render
1. Generate voice lines: `python tools/generate_voice_omnivoice.py --script playlist/full/voice-script.txt --out audio/full` (needs Hugging Face Hub access; see `tools/README.md`). Preview-quality clips already in `audio/full/` were made with Arena TTS.
2. `python tools/make_video.py --scenes playlist/full/scenes.json --out video/full/samudragupta-full-hinglish.mp4`

## Gate
- [x] Storyboard + chapters defined → this plan
- [ ] brag.mp4 exists → pending full audio batch (OmniVoice blocked by HF Hub network restriction in sandbox; Arena TTS previews in use)
- [x] Share copy written → `brag-output-full/share-copy.txt`
