from backend.app.models.schemas import Probabilities
from backend.app.pipelines.fusion import FusedFeatures


RISK_LABELS = {
    "low": "Low Risk",
    "moderate": "Moderate Risk",
    "high": "High Risk",
}


def predict_probabilities(features: FusedFeatures) -> Probabilities:
    combined = (features.text_signal * 0.68) + (features.audio_signal * 0.32)
    adjusted = max(0.0, min(1.0, combined - features.protective_signal))

    high = _clamp((adjusted - 0.48) / 0.52)
    moderate = _clamp(1.0 - abs(adjusted - 0.48) / 0.44)
    low = _clamp(1.0 - (adjusted / 0.5))

    total = low + moderate + high
    if total == 0:
        low, moderate, high = 0.7, 0.25, 0.05
        total = 1.0

    return Probabilities(
        low=round(low / total, 4),
        moderate=round(moderate / total, 4),
        high=round(high / total, 4),
    )


def score_from_probabilities(probabilities: Probabilities) -> int:
    score = (probabilities.low * 18) + (probabilities.moderate * 55) + (probabilities.high * 88)
    return int(round(max(0, min(100, score))))


def label_from_score(score: int) -> str:
    if score <= 30:
        return RISK_LABELS["low"]
    if score <= 60:
        return RISK_LABELS["moderate"]
    return RISK_LABELS["high"]


def confidence_from_probabilities(probabilities: Probabilities) -> float:
    return round(max(probabilities.low, probabilities.moderate, probabilities.high), 4)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
