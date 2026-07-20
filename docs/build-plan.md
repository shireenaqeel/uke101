# Build Plan

Each phase is a shippable checkpoint. We confirm a phase works before starting the next one (this project has a history of scope creep — phases are the guardrail).

## Phases

| Phase | Deliverable | Status |
|---|---|---|
| 0 | Repo scaffold: venv, structure, runnable NiceGUI landing page, tests | ✅ done |
| 1 | Chord Library: chord data set, data-driven fretboard renderer, audio pluck synth, browse + "mark learned" | ✅ done |
| 2 | Chord Switching Trainer: metronome engine, 2-chord drills, switch-speed tracking per pair | ✅ done |
| 3 | Strumming Pattern Trainer + Progress Dashboard | ✅ done |
| 4 | Strum Arcade (scored rhythm game) | ✅ done |
| 5 | Song Mode (scrolling lyrics + synced chords) | ✅ done |
| 6 | Song Composer | ✅ done |
| 7 | Notation Reading Track | ✅ done |
| 8 | Gamification (XP, levels, streaks, badges) | ⬜ next |
| 9 | Adaptive Difficulty (ML, no audio) | ⬜ |
| 10 | Mic-Based Chord Recognition (ML, audio pipeline) | ⬜ |

**MVP = Phases 1–3** (Definition of Done in the project spec, Section 8) — ✅ **complete**. Phases 4–10 make it "the full thing."

## Reuse contracts (decided up front to avoid duplication)

- One `render_fretboard(chord)` function — used by Chord Library, Switching Trainer, and Song Mode.
- One `pluck(frequency)` / chord-synthesis function — used everywhere audio plays.
- Content (chords / patterns / songs) lives in `src/koa/data/` as plain data, never hardcoded inside UI components.
- ML lives in `src/koa/ml/` as plain functions from day one, wired into the UI only when its phase arrives.

## Working agreement

- Build incrementally; after each phase, stop and summarize what was built + tested + what's left.
- Tests written alongside features (core logic, edge cases, one integration check per major feature).
- Ask before scope-expanding beyond the current phase.
- Commits: conventional, one meaningful change each, no AI attribution anywhere.
