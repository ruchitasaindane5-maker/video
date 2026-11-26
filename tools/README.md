# tools/ — voice + render pipeline

## OmniVoice (primary voice engine)
https://github.com/k2-fsa/OmniVoice — zero-shot TTS, 600+ languages, voice design + cloning.

```bash
pip install omnivoice torch torchaudio soundfile
python tools/generate_voice_omnivoice.py \
  --script playlist/short/voice-script.txt --out audio/short
python tools/generate_voice_omnivoice.py \
  --script playlist/full/voice-script.txt  --out audio/full
```

Speaker → `instruct` (voice design):

| Speaker | Instruct |
|---|---|
| NARRATOR | male, middle-aged, low pitch, warm, gentle, Indian accent, storytelling |
| HARISENA | male, elderly, low pitch, deep, regal, slow, Indian accent, ancient orator |
| HISTORIAN | female, middle-aged, clear, articulate, measured, Indian accent, historian |

Language: `Hindi` (`--language`) — the scripts are Hinglish (Devanagari + Latin English),
Hindi is the base language. **Note:** first run downloads the `k2-fsa/OmniVoice` weights
from the Hugging Face Hub. If your network blocks huggingface.co, run on a machine with
Hub access, or use VoiceStudio.

## VoiceStudio (GUI alternative — also OmniVoice under the hood)
https://github.com/debpalash/voicestudio — desktop app (Win/macOS/Linux).

1. Install VoiceStudio (installer script / DMG / brew, see repo README).
2. Launch → Model Manager → download OmniVoice models.
3. Voice Design: create the three presets from the table above (or Voice Clone from a sample).
4. Import `playlist/<ep>/voice-script.txt` → Narrate (batch) → assign voices per `[SPEAKER]` tag → Export WAV to `audio/<ep>/`.
5. VoiceStudio also exposes a local API/MCP for automating this step.

## make_video.py — render (brag "composition" step, headless)
Ken Burns zoom + gold caption bar + scene audio + fades, concatenated to MP4 via ffmpeg
(imageio-ffmpeg). No browser required — used because this sandbox cannot run Hyperframes'
browser-based renderer.

```bash
pip install pillow imageio-ffmpeg numpy soundfile
python tools/make_video.py --scenes playlist/short/scenes.json \
  --out video/short/samudragupta-short-hinglish.mp4
python tools/make_video.py --scenes playlist/full/scenes.json \
  --out video/full/samudragupta-full-hinglish.mp4
```

`scenes.json` maps images → audio clips (multiple files are concatenated with 0.4 s gaps)
+ on-screen caption text. Duration comes from the audio; `hold` adds a silent tail.

## Audio previews
`audio/preview/` holds the Arena TTS Hinglish previews played for review
(short: 6 scenes + combined preview MP3; full: hook + HARISENA + HISTORIAN sample).
Replace with OmniVoice output for the production master.
