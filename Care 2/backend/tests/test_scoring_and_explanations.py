from backend.app.pipelines.fusion import fuse_features
from backend.app.preprocessing.text import extract_text_features
from backend.app.scoring.risk import label_from_score, predict_probabilities, score_from_probabilities
from backend.app.services.explanation_service import explain_text


def test_scoring_returns_probability_distribution():
    text_features = extract_text_features("I am overwhelmed and exhausted.")
    fused = fuse_features(text_features, None)
    probabilities = predict_probabilities(fused)

    total = probabilities.low + probabilities.moderate + probabilities.high
    assert 0.99 <= total <= 1.01
    assert 0 <= score_from_probabilities(probabilities) <= 100


def test_label_thresholds():
    assert label_from_score(20) == "Low Risk"
    assert label_from_score(45) == "Moderate Risk"
    assert label_from_score(75) == "High Risk"


def test_explanation_mentions_protective_language():
    text_features = extract_text_features("I feel sad but have support and a therapist.")
    explanations = explain_text(text_features)

    assert any("Protective language" in item for item in explanations)
