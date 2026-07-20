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

**Phase 1 (Chord Library) complete.** 12 chords rendered from data as fretboard diagrams (`render_fretboard`), each playable via server-synthesized audio (`koa.audio.synth`) and markable as "learned" with state persisted to SQLite across reloads. 18 tests passing.

Next: Phase 2 (Chord Switching Trainer). Full plan and status in [`docs/build-plan.md`](docs/build-plan.md); each phase is a shippable checkpoint.
