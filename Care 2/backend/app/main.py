from time import perf_counter
from uuid import uuid4
import logging

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config.settings import settings
from backend.app.models.schemas import HealthResponse, PredictionResponse, VersionResponse
from backend.app.services.prediction_service import AnalysisInputs, PredictionService
from backend.app.utils.logging import RequestLoggerAdapter, configure_logging


configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Decision-support prototype for multimodal mental-health risk estimation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prediction_service = PredictionService()
base_logger = logging.getLogger("backend.app")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name)


@app.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    return VersionResponse(app_version=settings.app_version, model_version=settings.model_version)


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    text: str | None = Form(default=None),
    audio: UploadFile | None = File(default=None),
) -> PredictionResponse:
    return await _analyze_request(text=text, audio=audio)


@app.post("/explain", response_model=PredictionResponse)
async def explain(
    text: str | None = Form(default=None),
    audio: UploadFile | None = File(default=None),
) -> PredictionResponse:
    return await _analyze_request(text=text, audio=audio)


async def _analyze_request(text: str | None, audio: UploadFile | None) -> PredictionResponse:
    request_id = str(uuid4())
    logger = RequestLoggerAdapter(base_logger, {"request_id": request_id})
    started = perf_counter()

    audio_filename: str | None = None
    audio_content: bytes | None = None
    if audio is not None:
        audio_filename = audio.filename
        audio_content = await audio.read()

    try:
        response = prediction_service.analyze(
            AnalysisInputs(text=text, audio_filename=audio_filename, audio_content=audio_content),
            request_id=request_id,
        )
    except ValueError as exc:
        logger.info("validation_error error=%s", str(exc))
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("prediction_failed")
        raise HTTPException(status_code=500, detail="Prediction failed.") from exc

    elapsed_ms = round((perf_counter() - started) * 1000, 2)
    logger.info(
        "prediction_complete model_version=%s elapsed_ms=%s score=%s",
        response.model_version,
        elapsed_ms,
        response.score,
    )
    return response
