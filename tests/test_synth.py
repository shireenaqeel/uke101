import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np

from koa.audio import synth


def test_note_frequency_octave_and_open():
    assert synth.note_frequency(440.0, 0) == 440.0
    assert synth.note_frequency(440.0, 12) == 440.0 * 2  # one octave up


def test_pluck_shape_and_range():
    wave = synth.pluck(440.0, duration=0.5)
    assert wave.shape[0] == int(synth.SAMPLE_RATE * 0.5)
    assert np.max(np.abs(wave)) <= 1.0
    assert np.any(wave != 0)


def test_chord_samples_mix_normalised():
    samples = synth.chord_samples({"G": 0, "C": 0, "E": 0, "A": 3})
    assert np.max(np.abs(samples)) <= 1.0
    assert np.any(samples != 0)


def test_muted_string_is_skipped():
    both = synth.chord_samples({"G": 0, "C": 0, "E": 0, "A": 3})
    muted = synth.chord_samples({"G": None, "C": 0, "E": 0, "A": 3})
    assert not np.array_equal(both, muted)


def test_chord_wav_has_riff_header():
    data = synth.chord_wav({"G": 0, "C": 0, "E": 0, "A": 3})
    assert data[:4] == b"RIFF"
    assert data[8:12] == b"WAVE"
    assert len(data) > 44  # header + samples


def test_up_and_down_strum_differ():
    frets = {"G": 0, "C": 2, "E": 3, "A": 2}
    down = synth.strum_samples(frets, "D")
    up = synth.strum_samples(frets, "U")
    assert down.shape == up.shape
    assert not np.array_equal(down, up)  # opposite sweep direction


def test_strum_wav_riff_header():
    data = synth.strum_wav({"G": 0, "C": 0, "E": 0, "A": 3}, "D")
    assert data[:4] == b"RIFF"


def test_metronome_wav_riff_header():
    assert synth.metronome_wav()[:4] == b"RIFF"
