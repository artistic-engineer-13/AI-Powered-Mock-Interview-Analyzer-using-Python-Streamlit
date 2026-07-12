from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Iterable

import pandas as pd


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except Exception:
        return default


def format_timestamp(value: Any, pattern: str = "%b %d, %Y %I:%M %p", default: str = "-") -> str:
    if value is None or value == "":
        return default
    try:
        timestamp = pd.to_datetime(value)
    except Exception:
        return default

    if pd.isna(timestamp):
        return default

    if isinstance(timestamp, pd.Timestamp):
        if timestamp.tzinfo is not None:
            timestamp = timestamp.tz_localize(None)
        return timestamp.to_pydatetime().strftime(pattern)

    if isinstance(timestamp, datetime):
        return timestamp.strftime(pattern)

    return default


def safe_filename(value: str, fallback: str = "report") -> str:
    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "_", value.strip().lower())
    normalized = normalized.strip("._-")
    return normalized or fallback


def unique_non_empty(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result