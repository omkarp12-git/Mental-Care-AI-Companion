from dataclasses import dataclass
from uuid import uuid4

from backend.app.config.settings import settings
from backend.app.models.schemas import PredictionResponse
from backend.app.pipelines.fusion import fuse_features
from backend.app.preprocessing.audio import AudioFeatures, extract_audio_features
from backend.app.preprocessing.text import TextFeatures, extract_text_features
from backend.app.scoring.risk import (
    confidence_from_probabilities,
    label_from_score,
    predict_probabilities,
    score_from_probabilities,
)
from backend.app.services.explanation_service import explain_audio, explain_text


@dataclass(frozen=True)
class AnalysisInputs:
    text: str | None = None
    audio_filename: str | None = None
    audio_content: bytes | None = None


class PredictionService:
    def analyze(self, inputs: AnalysisInputs, request_id: str | None = None) -> PredictionResponse:
        text_features: TextFeatures | None = extract_text_features(inputs.text)
        audio_features: AudioFeatures | None = None

        if inputs.audio_filename and inputs.audio_content is not None:
            audio_features = extract_audio_features(inputs.audio_filename, inputs.audio_content)

        if not text_features and not audio_features:
            raise ValueError("Provide text, audio, or both before requesting a prediction.")

        fused = fuse_features(text_features, audio_features)
        probabilities = predict_probabilities(fused)
        score = score_from_probabilities(probabilities)

        return PredictionResponse(
            prediction=label_from_score(score),
            score=score,
            confidence=confidence_from_probabilities(probabilities),
            probabilities=probabilities,
            text_explanation=explain_text(text_features),
            audio_explanation=explain_audio(audio_features),
            model_version=settings.model_version,
            request_id=request_id or str(uuid4()),
        )
