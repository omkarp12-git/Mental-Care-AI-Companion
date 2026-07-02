from io import BytesIO
import math
import struct
import wave

import pytest

from backend.app.preprocessing.audio import extract_audio_features, validate_audio_upload


def _wav_bytes(duration_seconds: float = 0.25, sample_rate: int = 16000) -> bytes:
    buffer = BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for index in range(int(sample_rate * duration_seconds)):
            value = int(9000 * math.sin(2 * math.pi * 440 * index / sample_rate))
            wav_file.writeframes(struct.pack("<h", value))
    return buffer.getvalue()


def test_extract_audio_features_from_wav():
    features = extract_audio_features("sample.wav", _wav_bytes())

    assert features.duration_seconds > 0
    assert features.energy > 0
    assert features.extension == ".wav"


def test_validate_audio_rejects_unsupported_extension():
    with pytest.raises(ValueError, match="Unsupported audio format"):
        validate_audio_upload("notes.txt", b"hello")
