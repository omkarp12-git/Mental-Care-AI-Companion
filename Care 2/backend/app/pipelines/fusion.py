from dataclasses import dataclass

from backend.app.preprocessing.audio import AudioFeatures
from backend.app.preprocessing.text import TextFeatures


@dataclass(frozen=True)
class FusedFeatures:
    text_signal: float
    audio_signal: float
    protective_signal: float
    completeness: float


def fuse_features(
    text_features: TextFeatures | None,
    audio_features: AudioFeatures | None,
) -> FusedFeatures:
    text_signal = 0.0
    protective_signal = 0.0
    if text_features:
        keyword_signal = (text_features.high_risk_hits * 0.34) + (text_features.moderate_risk_hits * 0.13)
        length_signal = min(0.12, text_features.word_count / 500)
        text_signal = min(1.0, keyword_signal + length_signal + text_features.intensity)
        protective_signal = min(0.35, text_features.protective_hits * 0.08)

    audio_signal = 0.0
    if audio_features:
        low_energy_signal = max(0.0, 0.4 - audio_features.energy) * 0.65
        silence_signal = min(0.35, audio_features.silence_ratio * 0.28)
        duration_signal = 0.08 if audio_features.duration_seconds >= 8 else 0.0
        audio_signal = min(1.0, low_energy_signal + silence_signal + duration_signal)

    completeness = float(bool(text_features)) + float(bool(audio_features))
    completeness = completeness / 2

    return FusedFeatures(
        text_signal=round(text_signal, 4),
        audio_signal=round(audio_signal, 4),
        protective_signal=round(protective_signal, 4),
        completeness=round(completeness, 4),
    )
