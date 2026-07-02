from backend.app.preprocessing.text import clean_text, extract_text_features


def test_clean_text_collapses_whitespace():
    assert clean_text("  I   feel\n overwhelmed\t today  ") == "I feel overwhelmed today"


def test_extract_text_features_detects_risk_and_protective_terms():
    features = extract_text_features("I feel hopeless and exhausted, but my friend can help.")

    assert features is not None
    assert features.high_risk_hits == 1
    assert features.moderate_risk_hits == 1
    assert features.protective_hits >= 2
