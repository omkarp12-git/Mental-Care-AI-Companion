from pydantic import BaseModel, Field


class Probabilities(BaseModel):
    low: float = Field(ge=0, le=1)
    moderate: float = Field(ge=0, le=1)
    high: float = Field(ge=0, le=1)


class PredictionResponse(BaseModel):
    prediction: str
    score: int = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    probabilities: Probabilities
    text_explanation: list[str]
    audio_explanation: list[str]
    model_version: str
    request_id: str


class HealthResponse(BaseModel):
    status: str
    app: str


class VersionResponse(BaseModel):
    app_version: str
    model_version: str
