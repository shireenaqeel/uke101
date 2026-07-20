"""Pure metronome / switch-speed timing helpers.

No framework or audio imports so the timing math is trivially testable; the UI
layer drives the actual ticks with a NiceGUI timer.
"""


def interval_seconds(bpm: float) -> float:
    """Seconds between beats for a given tempo."""
    if bpm <= 0:
        raise ValueError("bpm must be positive")
    return 60.0 / bpm


def switches_per_minute(count: int, elapsed_seconds: float) -> float:
    """Extrapolate a clean-switch count over any elapsed time to a per-minute rate."""
    if elapsed_seconds <= 0:
        return 0.0
    return count * 60.0 / elapsed_seconds
