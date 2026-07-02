from io import BytesIO
import math
import struct
import wave

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def _wav_bytes(duration_seconds: float = 0.2, sample_rate: int = 16000) -> bytes:
    buffer = BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for index in range(int(sample_rate * duration_seconds)):
            value = int(5000 * math.sin(2 * math.pi * 220 * index / sample_rate))
            wav_file.writeframes(struct.pack("<h", value))
    return buffer.getvalue()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json()["model_version"] == "hybrid-demo-v1"


def test_predict_text_only():
    response = client.post("/predict", data={"text": "I feel overwhelmed but my family can help."})

    assert response.status_code == 200
    payload = response.json()
    assert payload["prediction"] in {"Low Risk", "Moderate Risk", "High Risk"}
    assert "probabilities" in payload


def test_predict_audio_only():
    response = client.post(
        "/predict",
        files={"audio": ("sample.wav", _wav_bytes(), "audio/wav")},
    )

    assert response.status_code == 200
    assert response.json()["audio_explanation"]


def test_predict_text_and_audio():
    response = client.post(
        "/predict",
        data={"text": "I feel exhausted and isolated."},
        files={"audio": ("sample.wav", _wav_bytes(), "audio/wav")},
    )

    assert response.status_code == 200
    assert response.json()["score"] >= 0


def test_predict_rejects_empty_request():
    response = client.post("/predict", data={})

    assert response.status_code == 400


def test_predict_rejects_unsupported_audio():
    response = client.post(
        "/predict",
        files={"audio": ("notes.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 400
