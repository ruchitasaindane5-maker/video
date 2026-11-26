# /brag plan — SHORT · The Untold Story of Samudragupta (Ep 1)

**Product:** YouTube playlist "The Untold Story of Samudragupta" — Episode 1 Short
**Tone:** cinematic museum-exhibit documentary (gold/saffron on dark)
**Format:** vertical 1080×1920 @30fps · ~64s
**Voice:** Hinglish, 2 storytelling voices — NARRATOR (voice-00), HARISENA (voice-01)
**Music:** low tanpura drone, ducked −18dB (dropped in this render; add royalty-free drone before upload)
**Voice pipeline:** Arena/Gemini TTS preview → final production via OmniVoice (`tools/generate_voice_omnivoice.py`) or VoiceStudio GUI

## Beat storyboard

| # | Time | Visual | Motion | On-screen text | Voice |
|---|---|---|---|---|---|
| 1 | 0:00–0:07 | `assets/short/01-hook-map.jpg` — Gupta India glowing at night | slow zoom, gold pulse | HE CONQUERED INDIA… THEN GAVE IT BACK | NARRATOR |
| 2 | 0:07–0:17 | `assets/short/02-samudragupta-coin.jpg` — golden veena coin | Ken Burns | SAMUDRAGUPTA · Undefeated | NARRATOR |
| 3 | 0:17–0:27 | `assets/short/03-allahabad-pillar.jpg` — inscription close-up | push-in | ALLAHABAD PILLAR · c. 335 CE | HARISENA |
| 4 | 0:27–0:45 | `assets/short/04-restored-thrones.jpg` — kings bow, then rise to thrones | crossfade bow→rise | HE RESTORED THEIR THRONES | NARRATOR |
| 5 | 0:45–0:54 | `assets/short/05-gold-coins.jpg` — Gupta gold coins | sparkle zoom | VIKRAMADITYA · Sun of Kings | NARRATOR |
| 6 | 0:54–1:05 | `assets/short/06-outro.jpg` — Gupta temple sunset, end card | fade | FULL STORY ON CHANNEL | NARRATOR |

## Render
`python tools/make_video.py --scenes playlist/short/scenes.json --out video/short/samudragupta-short-hinglish.mp4`
Result: 63.6s, 1080×1920, H.264 + AAC. (Headless sandbox — Hyperframes' browser-based render was substituted with the PIL+ffmpeg Ken-Burns pipeline; `npx hyperframes` was not run.)

## Gate
- [x] brag.mp4 exists → `video/short/samudragupta-short-hinglish.mp4`
- [x] Storyboard summed to runtime (63.6s)
- [x] Share copy written → `brag-output-short/share-copy.txt`
