import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Student Management System")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sms.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "local-development-secret-change-this-32-chars")
    ACCESS_TOKEN_MINUTES: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))
    ADMISSION_YEAR: int = int(os.getenv("ADMISSION_YEAR", "2026"))

settings = Settings()
if len(settings.SECRET_KEY) < 32:
    raise RuntimeError("SECRET_KEY must be at least 32 characters long; set it in .env")
