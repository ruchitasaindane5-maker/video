# SHORT — The Untold Story of Samudragupta
**Format:** YouTube Shorts · 9:16 vertical · 1080×1920 · ~50 seconds · ~140 words
**Tone:** Cinematic storytelling (brag tone: `cinematic`)
**Voices:** NARRATOR (main) + HARISENA (inscription quote)

---

## Full Script (read aloud — timing in brackets)

**[0:00–0:04 · HOOK — Scene 1]**
> **NARRATOR:** He conquered almost all of India… in forty years. And then — he gave it back.

**[0:04–0:12 · Scene 2]**
> **NARRATOR:** This is Samudragupta. The undefeated king of the Gupta Empire. No Indian king before him had won so much.

**[0:12–0:22 · Scene 3]**
> **HARISENA:** *(reading the Allahabad Pillar inscription)* "Kings surrendered at his feet. Their crowns touched the dust. And he restored them — to their thrones."

**[0:22–0:34 · Scene 4]**
> **NARRATOR:** He didn't keep their kingdoms. He didn't loot. He performed a hundred horse sacrifices — and still, he is remembered not as a tyrant… but as a scholar, a poet, and a musician.

**[0:34–0:44 · Scene 5]**
> **NARRATOR:** His gold coins still shine after sixteen hundred years. His name? Vikramaditya. The Sun of Kings.

**[0:44–0:50 · OUTRO / CTA — Scene 6]**
> **NARRATOR:** The full untold story is on the channel. Follow for Episode 2 — and tell me: conqueror… or king?

---

## On-Screen Text (burned-in subtitles)

| Scene | Big text (first 2 sec of scene) | Subtitle line |
|---|---|---|
| 1 | HE CONQUERED INDIA… | He conquered almost all of India… in forty years. |
| 1 | …THEN GAVE IT BACK | And then — he gave it back. |
| 2 | SAMUDRAGUPTA | The undefeated king of the Gupta Empire |
| 3 | ALLAHABAD PILLAR · c. 335 CE | "Kings surrendered at his feet…" — Harisena |
| 4 | HE RESTORED THEIR THRONES | Not a tyrant. A scholar. A poet. A musician. |
| 5 | VIKRAMADITYA | The Sun of Kings · 1,600 years later, still shining |
| 6 | FULL STORY ON CHANNEL | Follow for Episode 2 👇 |

## Production Notes
- **Pacing:** Fast-in, then hold. Every subtitle line stays ≥1.2s. No flashing text.
- **Music:** Low tanpura drone + soft tabla, ducked under voice (-18 dB). Use brag bundled track at low volume or royalty-free drone.
- **SFX:** Single deep drum hit on "gave it back", soft coin shimmer on Scene 5.
- **Safe zone (Shorts):** Keep text between 13%–80% of height; avoid bottom-right buttons area.
- **Thumbnail frame:** Scene 2 — Samudragupta on gold coin, text "HE GAVE IT BACK?"

**Voiceover language: Hinglish (Devanagari हिंदी + English).**

## Voice Casting (OmniVoice voice-design)
| Speaker | OmniVoice `instruct` | VoiceStudio preset |
|---|---|---|
| NARRATOR | `male, middle aged, low pitch, british accent` | Narrator — Deep Storyteller |
| HARISENA | `male, elderly, low pitch, british accent` | Court Poet — Elderly, Formal |
| ALT (optional female) | `female, middle aged, british accent` | Historian — Warm, Clear |

Generate with: `python tools/generate_voice_omnivoice.py --script playlist/short/voice-script.txt --out audio/short`
