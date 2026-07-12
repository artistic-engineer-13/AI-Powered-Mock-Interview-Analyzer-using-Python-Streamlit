from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_model=os.getenv("GEMINI_MODEL", "models/gemini-3.5-flash"),
    )
