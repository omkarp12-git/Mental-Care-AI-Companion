from array import array
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import wave

from backend.app.config.settings import settings


@dataclass(frozen=True)
class AudioFeatures:
    filename: str
    extension: str
    duration_seconds: float
    average_amplitude: float
    energy: float
    silence_ratio: float


def validate_audio_upload(filename: str, content: bytes) -> None:
    extension = Path(filename or "").suffix.lower()
    if extension not in settings.supported_audio_extensions:
        supported = ", ".join(settings.supported_audio_extensions)
        raise ValueError(f"Unsupported audio format. Supported formats: {supported}.")
    if not content:
        raise ValueError("Uploaded audio file is empty.")
    if len(content) > settings.max_audio_bytes:
        raise ValueError("Uploaded audio file exceeds the 30 MB limit.")


def extract_audio_features(filename: str, content: bytes) -> AudioFeatures:
    validate_audio_upload(filename, content)
    extension = Path(filename).suffix.lower()
    if extension == ".wav":
        try:
            return _extract_wav_features(filename, content)
        except wave.Error:
            pass
    return _extract_byte_features(filename, content)


def _extract_wav_features(filename: str, content: bytes) -> AudioFeatures:
    with wave.open(BytesIO(content), "rb") as wav_file:
        frame_count = wav_file.getnframes()
        sample_rate = wav_file.getframerate() or 16000
        sample_width = wav_file.getsampwidth()
        channels = wav_file.getnchannels() or 1
        frames = wav_file.readframes(frame_count)

    duration = frame_count / sample_rate if sample_rate else 0.0
    if not frames:
        return AudioFeatures(filename, ".wav", duration, 0.0, 0.0, 1.0)

    max_possible = float(2 ** (8 * sample_width - 1))
    samples = _decode_samples(frames, sample_width)
    rms = _rms(samples)
    average_amplitude = min(1.0, rms / max_possible)
    energy = min(1.0, average_amplitude * 1.35)

    if not samples:
        silence_ratio = 1.0
    else:
        threshold = max(1, int(max_possible * 0.025))
        silent = sum(1 for sample in samples if abs(sample) < threshold)
        silence_ratio = silent / len(samples)

    if channels > 1:
        silence_ratio = min(1.0, silence_ratio * 1.05)

    return AudioFeatures(
        filename=filename,
        extension=".wav",
        duration_seconds=round(duration, 3),
        average_amplitude=round(average_amplitude, 4),
        energy=round(energy, 4),
        silence_ratio=round(silence_ratio, 4),
    )


def _decode_samples(frames: bytes, sample_width: int) -> list[int]:
    if sample_width == 1:
        return [sample - 128 for sample in frames]
    if sample_width == 2:
        samples = array("h")
    elif sample_width == 4:
        samples = array("i")
    else:
        return []
    samples.frombytes(frames)
    return list(samples)


def _rms(samples: list[int]) -> float:
    if not samples:
        return 0.0
    mean_square = sum(sample * sample for sample in samples) / len(samples)
    return mean_square**0.5


def _extract_byte_features(filename: str, content: bytes) -> AudioFeatures:
    extension = Path(filename).suffix.lower()
    sample = content[: min(len(content), 16000)]
    if not sample:
        return AudioFeatures(filename, extension, 0.0, 0.0, 0.0, 1.0)

    centered = [abs(byte - 128) / 128 for byte in sample]
    average_amplitude = sum(centered) / len(centered)
    quiet = sum(1 for value in centered if value < 0.03)

    return AudioFeatures(
        filename=filename,
        extension=extension,
        duration_seconds=round(len(content) / 32000, 3),
        average_amplitude=round(min(1.0, average_amplitude), 4),
        energy=round(min(1.0, average_amplitude * 1.2), 4),
        silence_ratio=round(quiet / len(centered), 4),
    )
