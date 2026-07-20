"""Server-side audio synthesis for chords and single notes.

Pure numpy — no framework imports — so it stays reusable across the chord
library, switching trainer, strum arcade and song mode, and is easy to test.
"""

import io
import wave

import numpy as np

SAMPLE_RATE = 44100

# Ukulele standard reentrant tuning: G4 - C4 - E4 - A4 (G higher than C).
OPEN_STRINGS = {
    "G": 392.00,
    "C": 261.63,
    "E": 329.63,
    "A": 440.00,
}
STRING_ORDER = ["G", "C", "E", "A"]


def note_frequency(open_freq: float, fret: int) -> float:
    """Frequency of a string stopped at ``fret`` (12-tone equal temperament)."""
    return open_freq * (2 ** (fret / 12))


def pluck(frequency: float, duration: float = 1.6, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """A plucked-string-ish tone: a few decaying harmonics with a soft attack.

    Returns a mono float32 waveform in roughly [-1, 1].
    """
    n = int(sample_rate * duration)
    t = np.linspace(0.0, duration, n, endpoint=False)

    harmonics = [1.0, 0.5, 0.33, 0.22, 0.14]
    tone = np.zeros_like(t)
    for i, amp in enumerate(harmonics, start=1):
        tone += amp * np.sin(2 * np.pi * frequency * i * t)

    decay = np.exp(-3.2 * t)
    attack = np.clip(t / 0.005, 0.0, 1.0)  # ~5ms fade-in to avoid a click
    tone *= decay * attack

    peak = np.max(np.abs(tone))
    if peak > 0:
        tone /= peak
    return tone.astype(np.float32)


def chord_samples(
    frets: dict,
    duration: float = 1.8,
    strum_delay: float = 0.035,
    sample_rate: int = SAMPLE_RATE,
) -> np.ndarray:
    """Mix the four strings of a chord into one waveform, staggered like a strum."""
    total = int(sample_rate * duration)
    mix = np.zeros(total, dtype=np.float32)

    for i, string in enumerate(STRING_ORDER):
        fret = frets.get(string)
        if fret is None:  # muted string
            continue
        freq = note_frequency(OPEN_STRINGS[string], fret)
        voice = pluck(freq, duration=duration, sample_rate=sample_rate)
        offset = int(i * strum_delay * sample_rate)
        end = min(total, offset + len(voice))
        mix[offset:end] += voice[: end - offset]

    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = mix / peak * 0.9
    return mix


def to_wav_bytes(samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> bytes:
    """Encode a mono float waveform as 16-bit PCM WAV bytes."""
    pcm = np.int16(np.clip(samples, -1.0, 1.0) * 32767)
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm.tobytes())
    return buffer.getvalue()


def chord_wav(frets: dict) -> bytes:
    """Convenience: synthesize a chord straight to WAV bytes."""
    return to_wav_bytes(chord_samples(frets))
