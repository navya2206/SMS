import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Always load the project's .env, even when uvicorn is started from another
# directory. Environment variables already set by the shell still win.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _int_setting(name: str, default: str) -> int:
    value = os.getenv(name, default)
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a whole number, got: {value!r}") from exc

@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Student Management System")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sms.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "local-development-secret-change-this-32-chars")
    ACCESS_TOKEN_MINUTES: int = _int_setting("ACCESS_TOKEN_MINUTES", "60")
    ADMISSION_YEAR: int = _int_setting("ADMISSION_YEAR", "2026")

settings = Settings()
if len(settings.SECRET_KEY) < 32:
    raise RuntimeError(
        "SECRET_KEY must be at least 32 characters long. "
        "Copy .env.example to .env and set a longer SECRET_KEY."
    )
