"""Mic-based chord recognition (headline ML feature).

Pipeline: recorded audio samples -> 12-bin chroma feature (pure numpy FFT) ->
a classifier that predicts which chord was played. The classifier is trained on
*synthetic* chroma generated from the app's own chord synthesizer plus noise, so
no external dataset is needed. scikit-learn is used if available; otherwise a
numpy nearest-centroid classifier (trained the same way) is the fallback, which
keeps the feature working even where sklearn has no wheel.
"""

import numpy as np

from koa.audio.synth import SAMPLE_RATE, chord_samples
from koa.data.chords import CHORDS

# pitch class of each open string (C=0, C#=1, ... B=11)
_OPEN_PC = {"G": 7, "C": 0, "E": 4, "A": 9}

try:  # optional stronger model
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    _HAVE_SKLEARN = True
except Exception:  # pragma: no cover - depends on environment
    _HAVE_SKLEARN = False


def chord_pitch_classes(chord: dict) -> set[int]:
    """The pitch classes sounded by a chord's fretting (music-theory ground truth)."""
    pcs = set()
    for string, fret in chord["frets"].items():
        if fret is None:
            continue
        pcs.add((_OPEN_PC[string] + fret) % 12)
    return pcs


def extract_chroma(samples: np.ndarray, sample_rate: int, n_fft: int = 4096, hop: int = 2048) -> np.ndarray:
    """Fold an audio clip's spectral energy into 12 pitch-class bins (L2-normalised)."""
    samples = np.asarray(samples, dtype=np.float64)
    if samples.size < n_fft:
        samples = np.pad(samples, (0, n_fft - samples.size))

    freqs = np.fft.rfftfreq(n_fft, 1.0 / sample_rate)
    valid = freqs > 20.0
    pc = np.zeros(freqs.shape, dtype=int)
    with np.errstate(divide="ignore"):
        midi = 69 + 12 * np.log2(np.where(valid, freqs, 1.0) / 440.0)
    pc[valid] = np.rint(midi[valid]).astype(int) % 12

    window = np.hanning(n_fft)
    chroma = np.zeros(12)
    frames = 0
    for start in range(0, samples.size - n_fft + 1, hop):
        mag = np.abs(np.fft.rfft(samples[start : start + n_fft] * window))
        np.add.at(chroma, pc[valid], mag[valid])
        frames += 1
    if frames == 0:
        return chroma
    norm = np.linalg.norm(chroma)
    return chroma / norm if norm > 0 else chroma


def _synthetic_dataset(variants: int = 8, seed: int = 0) -> tuple[np.ndarray, list[str]]:
    """Chroma features for each chord, rendered from the synth with added noise."""
    rng = np.random.default_rng(seed)
    features = []
    labels = []
    for chord in CHORDS:
        clean = chord_samples(chord["frets"], duration=1.4)
        for _ in range(variants):
            gain = rng.uniform(0.6, 1.0)
            noise = rng.normal(0, 0.02, clean.shape).astype(np.float32)
            features.append(extract_chroma(clean * gain + noise, SAMPLE_RATE))
            labels.append(chord["id"])
    return np.array(features), labels


class Recognizer:
    def __init__(self):
        self.labels: list[str] = []
        self._centroids: np.ndarray | None = None
        self._model = None

    def train(self) -> "Recognizer":
        X, y = _synthetic_dataset()
        self.labels = [c["id"] for c in CHORDS]
        if _HAVE_SKLEARN:
            self._model = make_pipeline(
                StandardScaler(), LogisticRegression(max_iter=1000, C=5.0)
            )
            self._model.fit(X, y)
        else:
            self._centroids = np.array(
                [X[[i for i, lbl in enumerate(y) if lbl == c]].mean(axis=0) for c in self.labels]
            )
        return self

    def predict(self, chroma: np.ndarray) -> tuple[str, float]:
        """Return (chord_id, confidence 0..1) for a chroma vector."""
        if self._model is not None:
            probs = self._model.predict_proba([chroma])[0]
            idx = int(np.argmax(probs))
            return self._model.classes_[idx], float(probs[idx])
        if self._centroids is None:
            self.train()
        sims = self._centroids @ chroma / (
            np.linalg.norm(self._centroids, axis=1) * (np.linalg.norm(chroma) + 1e-9) + 1e-9
        )
        probs = _softmax(sims * 8.0)
        idx = int(np.argmax(probs))
        return self.labels[idx], float(probs[idx])

    def predict_samples(self, samples: np.ndarray, sample_rate: int) -> tuple[str, float]:
        return self.predict(extract_chroma(samples, sample_rate))

    @property
    def backend(self) -> str:
        return "sklearn" if self._model is not None else "nearest-centroid"


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / e.sum()


_recognizer: Recognizer | None = None


def get_recognizer() -> Recognizer:
    """Lazily train and cache one recognizer for the process."""
    global _recognizer
    if _recognizer is None:
        _recognizer = Recognizer().train()
    return _recognizer
