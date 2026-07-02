from backend.app.preprocessing.audio import AudioFeatures
from backend.app.preprocessing.text import TextFeatures


def explain_text(text_features: TextFeatures | None) -> list[str]:
    if not text_features:
        return ["No text input was provided for text-based explanation."]

    explanations: list[str] = []
    high_terms = [term for term in text_features.matched_terms if term in {"hopeless", "worthless", "suicide", "suicidal", "self harm", "self-harm", "end it", "cannot go on", "no reason"}]
    if high_terms:
        explanations.append("Higher-risk language was detected in the text input.")
    if text_features.moderate_risk_hits:
        explanations.append("The text includes emotional strain terms such as fatigue, sadness, anxiety, or overwhelm.")
    if text_features.protective_hits:
        explanations.append("Protective language about support, safety, help, or coping reduced the estimated risk.")
    if text_features.intensity > 0.2:
        explanations.append("Urgent punctuation or emphasized wording increased the text signal.")

    if not explanations:
        explanations.append("The text did not contain strong risk terms in the demo vocabulary.")
    return explanations


def explain_audio(audio_features: AudioFeatures | None) -> list[str]:
    if not audio_features:
        return ["No audio input was provided for audio-based explanation."]

    explanations: list[str] = []
    if audio_features.energy < 0.18:
        explanations.append("Lower audio energy increased the audio risk signal.")
    if audio_features.silence_ratio > 0.45:
        explanations.append("Longer quiet or low-amplitude portions contributed to the audio signal.")
    if audio_features.duration_seconds >= 8:
        explanations.append("The recording was long enough to provide a more stable audio estimate.")

    if not explanations:
        explanations.append("The audio did not show strong low-energy or silence patterns in the demo extractor.")
    return explanations
