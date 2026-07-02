from dataclasses import dataclass
import re


HIGH_RISK_TERMS = {
    "hopeless",
    "worthless",
    "suicide",
    "suicidal",
    "self harm",
    "self-harm",
    "end it",
    "cannot go on",
    "no reason",
}

MODERATE_RISK_TERMS = {
    "anxious",
    "anxiety",
    "depressed",
    "sad",
    "overwhelmed",
    "exhausted",
    "isolated",
    "panic",
    "numb",
    "empty",
    "sleep",
    "tired",
}

PROTECTIVE_TERMS = {
    "support",
    "friend",
    "family",
    "therapist",
    "doctor",
    "help",
    "safe",
    "plan",
    "hope",
    "coping",
}


@dataclass(frozen=True)
class TextFeatures:
    cleaned_text: str
    word_count: int
    high_risk_hits: int
    moderate_risk_hits: int
    protective_hits: int
    intensity: float
    matched_terms: list[str]


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def extract_text_features(text: str | None) -> TextFeatures | None:
    cleaned = clean_text(text)
    if not cleaned:
        return None

    lowered = cleaned.lower()
    words = re.findall(r"[a-zA-Z']+", lowered)
    word_count = len(words)

    high_matches = sorted(term for term in HIGH_RISK_TERMS if term in lowered)
    moderate_matches = sorted(term for term in MODERATE_RISK_TERMS if term in lowered)
    protective_matches = sorted(term for term in PROTECTIVE_TERMS if term in lowered)

    exclamations = min(cleaned.count("!"), 5)
    all_caps_words = sum(1 for word in re.findall(r"\b[A-Z]{3,}\b", cleaned) if len(word) > 2)
    intensity = min(1.0, (exclamations * 0.08) + (all_caps_words * 0.06))

    return TextFeatures(
        cleaned_text=cleaned,
        word_count=word_count,
        high_risk_hits=len(high_matches),
        moderate_risk_hits=len(moderate_matches),
        protective_hits=len(protective_matches),
        intensity=intensity,
        matched_terms=high_matches + moderate_matches + protective_matches,
    )
