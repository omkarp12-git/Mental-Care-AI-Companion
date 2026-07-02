from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Mental Health AI Decision Support"
    app_version: str = "0.1.0"
    model_version: str = "hybrid-demo-v1"
    max_audio_bytes: int = 30 * 1024 * 1024
    supported_audio_extensions: tuple[str, ...] = (
        ".wav",
        ".mp3",
        ".m4a",
        ".flac",
        ".ogg",
        ".webm",
    )
    cors_origins: tuple[str, ...] = (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    )


settings = Settings()
