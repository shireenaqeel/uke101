# Koa — Ukulele Learning App

A free, focused, step-by-step web app that teaches ukulele from zero: chords → switching cleanly between them → strumming in rhythm → playing real songs → writing your own. A game layer (scores, streaks, XP) makes practice feel like progress rather than homework.

**Platform:** web app only (responsive desktop + mobile browser). Built as a single Python process — no separate frontend build step.

## Tech Stack

- **NiceGUI** — pure-Python UI + backend (FastAPI + Vue under the hood, but no JS/Vue written by hand)
- **SQLite** — local user-progress storage (chords learned, switch speeds, scores, streak)
- **numpy** — server-side audio synthesis (plucked-tone chords, metronome)
- ML/audio analysis (librosa, scikit-learn) — added later for the mic-based chord recognition track (Phases 9–10)

## Project Structure

```
src/koa/
  app.py        # NiceGUI app entry + page routing
  data/         # content layer: chords, strumming patterns, songs (data, not UI)
  audio/        # pluck/metronome synthesis
  ml/           # adaptive difficulty + chord recognition (plain functions)
run.py          # launcher
tests/          # pytest suite
docs/           # design notes and the build plan
```

The content layer (chords/patterns/songs) is kept separate from the UI so adding content later is trivial. One fretboard renderer and one audio-pluck function are reused across all modules.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

Then open the URL NiceGUI prints (default http://localhost:8080).

## Tests

```bash
pytest
```

## Status

**MVP complete (Phases 1–3).**

- **Chord Library** — 12 chords rendered from data as fretboard diagrams (`render_fretboard`), each playable via server-synthesized audio (`koa.audio.synth`) and markable as "learned", persisted to SQLite across reloads.
- **Chord Switching Trainer** — metronome (adjustable tempo + click), timed switch test over preset beginner pairs / 3- and 4-chord loops (or any custom pair), counts clean switches via tap or spacebar, and tracks the best switch count per drill across sessions.
- **Strumming Pattern Trainer** — six named patterns shown as a down/up/rest beat grid, play-along at adjustable tempo with the current beat highlighted and the chosen chord strummed on each stroke.
- **Strum Arcade** — a scored rhythm game over any pattern: tap in time with each stroke (Space or button), judged Perfect/Good/Miss with a combo multiplier and per-pattern high scores.
- **Song Mode** — play a real song end to end: lyrics and chord changes scroll in time with the tempo, the current line is highlighted, and the current chord's diagram shows on the side. Ships public-domain songs with full lyrics plus copyrighted starters as chord-chart-only (progression + link out, no verbatim lyrics). Completed songs are tracked.
- **Song Composer** — build a chord progression (add/reorder/remove), add optional lyrics in a ChordPro-style format (`[C]Twinkle [F]little`), preview it, and save. Composed songs are stored and play back in the same Song Mode player as curated ones, listed as "My songs", and can be deleted or exported as a text chord chart.
- **Notation Reading Track** — an optional skill track with three progressive sub-tracks (rhythm durations → treble-staff notes → 4-line ukulele tab), each a short multiple-choice drill session with SVG-rendered prompts, instant feedback, and per-track level progress. Kept separate from the chord/song path.
- **Gamification** — every practice action awards XP; XP drives levels, a daily practice streak, and unlockable badges (chords learned, switch/arcade milestones, songs, composing, notation, streaks). Surfaced at the top of the dashboard.
- **Progress Dashboard** — level/XP/streak and badges, chords learned, best switch speeds per drill, arcade high scores, songs completed, notation levels, and available patterns, all populated from real stored data.
- **Coach (adaptive)** — a rule-based recommender (`koa.ml.adaptive`) over your progress: the next chord that unlocks the most songs, your weakest switch drills (deep-linked into the trainer), songs you can play now, and songs one chord away.
- **Ear Trainer (mic ML)** — play a chord on a real ukulele and the app listens: the browser records a short clip, the server extracts a 12-bin chroma feature (pure numpy FFT), and a classifier trained on synthetic chroma from the app's own synth predicts the chord and compares it to your target. Uses scikit-learn when available, with a numpy nearest-centroid fallback.

**All 10 phases complete.** 86 tests passing. Full plan and status in [`docs/build-plan.md`](docs/build-plan.md).
