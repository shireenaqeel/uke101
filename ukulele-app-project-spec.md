# Project Spec: Koa — Ukulele Learning App

Hand this whole document to Claude Code as the starting context. It covers the problem, the full feature set, the content data (chords, strumming patterns, songs), the game layer, and a phased build plan so the build stays scoped instead of turning into one giant unfinished feature.

---

## 1. Problem Statement

Existing ukulele learning apps are either paid, cluttered, or don't actually teach the fundamentals in order. This app teaches ukulele from zero — holding the instrument, strings, chords, switching between chords, strumming patterns, and finally real songs — with a game layer so practice feels like progress, not homework.

**Primary user**: a total beginner who owns a ukulele and wants a free, focused, step-by-step way to learn — chords first, then switching cleanly between them, then strumming in rhythm, then playing real songs.

**Platform**: web application only — no native mobile app. Desktop and mobile browsers should both work (responsive layout), but this is not a packaged iOS/Android build.

**Non-goals for v1**: multiplayer, social/friend features. Real-time mic-based pitch/chord detection is now in scope as an ML feature (see Section 9) rather than excluded — it's what makes the practice feedback loop real instead of just a metronome/tap game.

---

## 1a. What Makes This Different

Plenty of ukulele apps already exist — most are paid, or teach chords in isolation with no path from "beginner" to "can actually play a song I chose." This app's differentiation is three things working together, not any single feature:

1. **A visible path to "professional"** — the app should always be able to answer "what's next for me" — from holding the instrument, to chords, to switching cleanly, to strumming in rhythm, to playing full songs, to writing your own. No dead end where the learner has "finished the app" but still can't really play.
2. **A reason to come back daily, not just "study when motivated"** — short daily sessions (5-10 min), a streak that's visible on the dashboard, and something new unlocking regularly (a new chord, a new song, a new drill) rather than one big static library dumped on the learner at once.
3. **Practice that feels like play, not homework** — every drill (chord switching, strumming, songs) has a score/combo/speed attached, so practicing the same thing twice has a visible reason: beat your last number. This is the job of the Strum Arcade and the switch-speed tracking — they turn repetition into a game rather than a chore.

Concretely, the features in this doc that carry the "different from other apps" weight are: the **Chord Switching Trainer** (most beginner apps skip this and jump straight to songs), the **Strum Arcade** (turns strumming practice into a scored game), the **Song Composer** (lets the learner become a creator, not just a consumer of pre-made content), and **Notation Reading** (most beginner uke apps teach chord diagrams only and never teach the learner to read actual notes — this app treats that as a real, if optional, skill track for someone aiming to go beyond "plays along to videos").

---

## 2. Core Content (the actual "curriculum")

### 2.1 Chords
Ukulele standard reentrant tuning: **G4 - C4 - E4 - A4** (G is tuned higher than C).

Chord library, ordered easiest → hardest:

| Chord | Frets (G-C-E-A) | Fingers | Difficulty |
|---|---|---|---|
| C major | 0-0-0-3 | ring on A(3) | easy |
| A minor | 2-0-0-0 | middle on G(2) | easy |
| F major | 2-0-1-0 | middle G(2), index E(1) | easy |
| A7 | 0-1-0-0 | index on C(1) | easy |
| G7 | 0-2-1-2 | index E(1), middle C(2), ring A(2) | easy |
| G major | 0-2-3-2 | index C(2), middle A(2), ring E(3) | medium |
| D major | 2-2-2-0 | barre index across G,C,E at fret 2 | medium |
| E minor | 0-4-3-2 | index A(2), middle E(3), ring C(4) | hard |
| A major | 2-1-0-0 | middle G(2), index C(1) | medium |
| D7 | 2-2-2-3 | index barre + pinky/ring stretch | hard |
| C7 | 0-0-0-1 | index on A(1) | easy |
| Bb major | 3-2-1-3 | barre-ish, hardest common shape | hard |

Each chord entry should carry: name, full name, fret positions per string, which finger goes where (in plain language — "ring finger, A string, 3rd fret"), a difficulty tag, and an audio reference (synthesize via Web Audio oscillators per string frequency, or use short sampled plucks if available).

### 2.2 Chord-Switching Drills
This is the single most requested beginner skill and deserves its own module, not just a side effect of the song player:
- Pick any 2 chords (e.g. C ↔ Am) → app shows both diagrams side by side → metronome ticks → user switches on each tick → track how many clean switches per minute.
- Progressive drill sets: common beginner pairs first (C↔Am, C↔F, Am↔F, G↔Em), then 3-chord loops (C-Am-F, G-Em-C), then 4-chord songs' progressions.
- Track "switch speed" over time per chord pair so the learner can see themselves getting faster — this is the core progress metric for this module.

### 2.3 Strumming Patterns
Library of named patterns, each shown as a down/up sequence with beat numbers, playable at adjustable tempo:
- **Basic down**: D-D-D-D
- **Island strum**: D-D-U-U-D-U (the most common beginner pattern)
- **Folk strum**: D-DU-UDU
- **Waltz (3/4)**: D-D-D
- **Reggae/off-beat**: (rest)-U-(rest)-U
- Each pattern: name, time signature, sequence array, a short "songs that use this" tag.

### 2.4 Reading Music (Notation Track — optional skill path)
Most beginner uke apps only ever teach chord diagrams. To genuinely support someone aiming to "become professional," include an optional notation track, taught progressively rather than dumped as one lesson:
- **Rhythm notation first**: quarter/half/whole notes and rests, tied to the strumming patterns the learner already knows (a down-strum on a quarter note is a concept they can already feel before they can name it).
- **Standard staff basics**: treble clef, the notes on the ukulele's open strings (G4, C4, E4, A4) located on the staff, then simple melodies using only those + a few frets.
- **Ukulele tab notation**: 4-line tab (one line per string), numbers indicating frets — easier entry point than the staff and worth teaching before or alongside standard notation, since most uke sheet music online uses tab.
- **Reading practice mode**: short, generated or curated note-reading drills (see a note on the staff/tab → play or identify it → instant feedback), separate from the song player so it can be practiced in isolated short reps.
- Treat this as its own optional track on the dashboard, not a gate in front of songs — a learner should be able to play full songs from chord charts without ever touching notation, and separately choose to go deeper into notation if they want to.

### 2.5 Song Composer (create your own song)
This is what turns the learner from a consumer of pre-made content into someone who can build their own — a strong retention and "I made a real thing" hook:
- **Chord progression builder**: pick chords from the library, arrange them into a sequence/loop (drag to reorder), choose a strumming pattern and tempo, and play the progression back immediately.
- **Lyric + chord placement**: optionally type in their own lyrics and place chord changes above specific words/lines, using the same data structure as the pre-built Songs (Section 2.6) — so a user-composed song is playable in Song Mode exactly like a curated one.
- **Save & revisit**: composed songs are saved to the user's progress data and listed alongside curated songs in Song Mode, tagged "my songs."
- **Optional share/export**: export the chord chart as text/PDF so they can print it or share it outside the app — no need for a social/multiplayer layer to get the "I made something real" payoff.

### 2.6 Songs
Song data model: title, artist, difficulty, chord list used, tempo (bpm), strumming pattern, and lyric lines each tagged with which chord to play at which word (like a standard lyrics-with-chords-above-the-line sheet). Suggested starter songs (all classic, ukulele-friendly, chord-simple — verify each is small enough of an excerpt or link out rather than reproducing full copyrighted lyrics wholesale):
- "Riptide" (Vance Joy) — Am, G, C
- "I'm Yours" (Jason Mraz) — C, G, Am, F
- "Somewhere Over the Rainbow / What a Wonderful World" medley — C, Am, F, G7
- "Count on Me" (Bruno Mars) — C, Em, F, G
- Traditional/folk songs in the public domain are safest to include lyrics for in full; for copyrighted songs, store chord charts + timing but link out to lyrics rather than embedding them verbatim.

**Song Mode UI**: lyrics scroll like a teleprompter, current chord highlighted above the current line, chord diagram shown on the side, tempo-synced.

---

## 3. Feature List (what to actually build)

| # | Feature | What it does |
|---|---|---|
| 1 | Onboarding / how to hold | Static illustrated steps — hold position, hand position |
| 2 | Chord Library | Browse all chords, see fretboard diagram, hear it, mark "learned" |
| 3 | Chord Switching Trainer | Metronome-paced drills between 2+ chords, tracks switch speed over time |
| 4 | Strumming Pattern Trainer | Visual beat pattern, adjustable tempo, practice mode |
| 5 | Strum Arcade (rhythm game) | Timed tap game scored Perfect/Good/Miss, combo + score, uses selected chord/pattern |
| 6 | Song Mode | Scrolling lyrics + chord changes synced to tempo, practice a real song end-to-end |
| 7 | Song Composer | Build your own chord progression + lyrics, save it, play it back like any other song |
| 8 | Notation Reading Track | Rhythm notation → staff basics → tab reading, with short isolated practice drills |
| 9 | Progress Dashboard | Chords learned, switch-drill speeds, arcade high scores, songs completed, notation progress, streak |
| 10 | Gamification layer | XP per practice session, levels, streaks, badges (e.g. "switched C↔Am cleanly 20x") |

**Suggested MVP scope (Phase 1-3 below)**: features 1, 2, 3, 4, 9 — that alone is a complete, usable app. Features 5, 6, 7, 8, 10 are what make it feel like "the full thing" and can follow immediately after.

---

## 4. Suggested Tech Stack (Python end-to-end, minimal moving parts)

Goal: one Python framework doing both the UI and the backend logic, instead of a separate frontend language/build step. Realistically, a browser-rendered app always has *some* HTML/CSS/JS under the hood — the point is that you never have to write or maintain it directly; the framework generates it.

- **App framework (pick one, this is the main decision)**:
  - **NiceGUI** — best fit here. Pure Python, built on FastAPI + Vue under the hood but you never touch Vue/JS yourself. Supports buttons, sliders, keyboard events, timers, canvas/SVG elements, and audio playback — enough to build the fretboard diagrams, metronome-driven drills, and the Strum Arcade's timing logic all in Python callbacks.
  - **Streamlit** — even simpler and faster to start, great fit for the Chord Library, Progress Dashboard, and Notation drills (mostly display + click + rerun). Weaker fit for the real-time-feeling Strum Arcade, since Streamlit reruns the whole script on interaction rather than handling tight event loops — usable for an MVP version of the arcade, but expect looser timing precision than NiceGUI.
  - **Reflex** — another pure-Python option (compiles to a React frontend for you), a middle ground between the two above.
  - Recommendation: **start with NiceGUI** so the Strum Arcade and switching-drill timers don't need a framework swap later; use Streamlit only if the priority is "get the content/dashboard/library live today" and the arcade can wait.
- **Backend logic**: whichever framework above is chosen already includes a backend (NiceGUI/Reflex run on FastAPI, Streamlit has its own server) — no separate API service needed.
- **Database**: SQLite via Python's built-in `sqlite3` or **SQLAlchemy** for progress data, chords, patterns, and songs — one file, no separate DB server to run.
- **Audio playback (chords, metronome)**: generate short audio clips server-side with Python (e.g. `numpy` to synthesize a plucked-tone waveform, write to a `.wav`/`.ogg` buffer) and hand them to the framework's built-in audio element — avoids hand-writing Web Audio API JS.
- **ML / audio analysis** (see Section 5): `librosa` / `aubio` for pitch and onset detection, `numpy`/`scipy` for chroma features, `scikit-learn` for the first chord classifier — all already Python, no separate ML service needed.
- **Deployment**: a single Python process (NiceGUI/Reflex/Streamlit all support this) — no separate frontend build/deploy step, no Node toolchain at all.

This keeps the stack to: **Python + one app framework + SQLite + numpy/scipy/librosa/scikit-learn** — nothing else required to ship the MVP.

---

## 5. Machine Learning Opportunities

These are what turn this from "another chord-diagram app" into something that actually listens and reacts — genuinely differentiating, and a good fit given the Python backend:

1. **Chord recognition from the mic (core ML feature)**: user plays a chord into the mic → browser records/streams a short clip → backend extracts a chroma feature vector (librosa) → a classifier (start with scikit-learn on hand-labeled/synthetic chroma data, upgrade to a small CNN on spectrograms later if accuracy needs it) predicts which chord was played → compare against the expected chord and give instant right/wrong feedback. This replaces "tap a button when you think you played it" with "the app actually heard what you played."
2. **Strum timing/rhythm detection**: instead of (or in addition to) the tap-button Strum Arcade, use onset detection (librosa/aubio) on a recorded strum to measure actual timing accuracy against the beat grid — same Perfect/Good/Miss scoring, but driven by real audio instead of a manual tap.
3. **Adaptive difficulty engine**: track per-chord and per-drill accuracy/speed over time, and use a simple model (even a rule-based or lightweight bandit approach counts as a legitimate first version) to decide what to serve next — weak chords and drills get surfaced more often, similar in spirit to spaced repetition.
4. **"What should I learn next" recommender**: given the chords a user has already learned, suggest the next song or chord that unlocks the most new songs — a small content-based recommendation, not a deep model, but real logic over the song/chord data.

**Suggested build order for ML**: start with #3 (adaptive difficulty) since it needs no audio pipeline at all — pure logic over progress data already being tracked. Then #1 (chord recognition) as the headline ML feature once the core app is stable, since it needs the most new infrastructure (audio upload/streaming endpoint + a trained or trainable classifier). #2 and #4 are natural follow-ons once #1 and #3 exist.

---

## 6. Data Model Sketch

```
Chord {
  id, name, fullName, difficulty,
  frets: { G, C, E, A },       // fret number per string, 0 = open
  fingers: [{ string, fret, fingerName }]
}

StrummingPattern {
  id, name, timeSignature,
  sequence: [{ beat, direction: "D"|"U"|"rest" }]
}

Song {
  id, title, artist, difficulty, tempo,
  chordsUsed: [chordId],
  strummingPatternId,
  lines: [{ text, chordChanges: [{ wordIndex, chordId }] }],
  isUserComposed: boolean,       // true for Song Composer creations, false for curated songs
  createdBy: userId | null
}

NotationDrill {
  id, track: "rhythm" | "staff" | "tab",
  level, prompt (e.g. note/rest image or tab snippet), correctAnswer
}

UserProgress {
  chordsLearned: [chordId],
  switchDrillBestSpeeds: { "C-Am": bpm, ... },
  arcadeBestScores: { patternId: score },
  songsCompleted: [songId],
  composedSongs: [songId],       // references Song entries where isUserComposed = true
  notationProgress: { rhythm: level, staff: level, tab: level },
  xp, level, streakDays, lastPracticedDate
}
```

---

## 7. Phased Build Plan (each phase is a usable milestone on its own)

1. **Phase 1 — Content + Chord Library**: build the chord data set, fretboard diagram renderer, audio pluck synth, and a browsable chord library with "mark learned."
2. **Phase 2 — Chord Switching Trainer**: metronome engine, 2-chord switch drills, speed tracking per pair.
3. **Phase 3 — Strumming Pattern Trainer + Progress Dashboard**: pattern library, tempo-adjustable practice view, and a dashboard tying together chords learned + switch speeds.
4. **Phase 4 — Strum Arcade**: turn the strumming trainer into a scored rhythm game (Perfect/Good/Miss timing windows, combo, high scores).
5. **Phase 5 — Song Mode**: song data for 4-6 starter songs, scrolling lyric+chord view synced to tempo.
6. **Phase 6 — Song Composer**: chord progression builder + optional lyric/chord placement, reusing the Song Mode player so composed songs are playable the same way curated ones are.
7. **Phase 7 — Notation Track**: rhythm notation drills first, then staff basics, then tab reading — each as its own short practice mode, kept optional/separate from the main chord-and-song path.
8. **Phase 8 (stretch) — Gamification**: XP, levels, streaks, badges layered on top of the progress data already being tracked (now including composed songs and notation progress).
9. **Phase 9 — Adaptive Difficulty (ML, no audio needed)**: rule-based or lightweight bandit logic over existing progress data to decide what to serve next.
10. **Phase 10 — Mic-Based Chord Recognition (ML, audio pipeline)**: audio upload/streaming endpoint, chroma feature extraction, and a trained classifier giving real "did you actually play that chord" feedback — the headline ML feature, tackled once everything above is stable.

> Note: Phases 1-3 alone already form a complete, demoable app. Treat each phase as a shippable checkpoint rather than something that only matters once everything is done — this avoids the common trap of one feature (usually the game or songs) eating all the time before anything is usable.

---

## 8. Definition of Done for MVP (Phases 1-3)

- [ ] Chord library renders fretboard diagrams from data (not hardcoded per chord) and plays correct pitches
- [ ] At least 8 chords included, each markable as "learned," with learned-state persisted
- [ ] Chord switching drill works for at least the 4 common beginner pairs, with switch speed tracked over multiple sessions
- [ ] At least 3 strumming patterns are practiceable at adjustable tempo
- [ ] Progress dashboard shows chords learned, switch speeds, and is populated from real stored data (not mocked)
- [ ] Progress survives a page reload / new session

---

## 9. Notes for Claude Code

- Treat chords/patterns/songs as a content layer (JSON/data files), separate from the UI components that render them — this makes adding content later trivial.
- Reuse one fretboard-rendering function across the chord library, switching trainer, and song mode rather than duplicating SVG logic three times.
- Reuse one audio-pluck function across all modules.
- Build with **one Python framework** (NiceGUI recommended — see Section 4) instead of splitting into a separate frontend/backend — that's the whole point of minimizing the stack here. Structure the code into modules (pages/views, data layer, audio/ML logic) rather than separate services.
- Keep the ML pieces (Section 5) as plain Python functions/modules from day one, even before they're wired into the UI — this makes it a clean drop-in when Phase 9/10 (ML) work starts, instead of a rewrite.
- Ask before scope-expanding beyond the current phase — this project has a history of scope creep, so each phase should be confirmed working before starting the next one.
