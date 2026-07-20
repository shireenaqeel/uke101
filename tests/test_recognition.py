import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np

from koa.audio.synth import SAMPLE_RATE, chord_samples
from koa.data.chords import CHORDS, get_chord
from koa.ml import recognition


def test_chord_pitch_classes():
    # C major (G0 C0 E0 A3) sounds G, C, E, C -> pitch classes {0, 4, 7}
    assert recognition.chord_pitch_classes(get_chord("C")) == {0, 4, 7}
    # A minor (G2 C0 E0 A0) -> A, C, E, A -> {9, 0, 4}
    assert recognition.chord_pitch_classes(get_chord("Am")) == {0, 4, 9}


def test_extract_chroma_peaks_at_played_pitch_class():
    sr = 22050
    t = np.linspace(0, 1.0, sr, endpoint=False)
    a4 = np.sin(2 * np.pi * 440.0 * t).astype(np.float32)  # A -> pitch class 9
    chroma = recognition.extract_chroma(a4, sr)
    assert int(np.argmax(chroma)) == 9
    assert np.isclose(np.linalg.norm(chroma), 1.0, atol=1e-6)


def test_extract_chroma_handles_short_clip():
    chroma = recognition.extract_chroma(np.zeros(100, dtype=np.float32), 16000)
    assert chroma.shape == (12,)


def test_recognizer_classifies_clean_chords():
    rec = recognition.get_recognizer()
    correct = 0
    for chord in CHORDS:
        samples = chord_samples(chord["frets"], duration=1.5)
        pred, conf = rec.predict_samples(samples, SAMPLE_RATE)
        correct += pred == chord["id"]
        assert 0.0 <= conf <= 1.0
    assert correct >= 11, f"only {correct}/{len(CHORDS)} recognised"


def test_recognizer_distinguishes_am_from_f():
    # Am {A,C,E} and F {A,C,F} differ by one note — the template blend must separate them.
    rec = recognition.get_recognizer()
    for name in ("Am", "F", "G", "G7", "C"):
        pred, _ = rec.predict_samples(chord_samples(get_chord(name)["frets"]), SAMPLE_RATE)
        assert pred == name, f"{name} misread as {pred}"


def test_chord_template_marks_pitch_classes():
    template = recognition.chord_template(get_chord("Am"))
    assert template[9] > 0 and template[0] > 0 and template[4] > 0  # A, C, E
    assert template[5] == 0  # no F
