from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from services.parsing.section_parser import parse_structured_fields
from services.parsing.text_extractors import extract_text_from_bytes, extract_text_from_file


@dataclass(frozen=True)
class ParsedResume:
    name: str | None
    email: str | None
    phone: str | None
    education: list[str]
    skills: list[str]
    projects: list[str]
    experience: list[str]
    certificates: list[str]
    raw_text: str
    source_file_name: str | None
    parsed_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


def parse_resume_text(text: str, source_file_name: str | None = None) -> ParsedResume:
    structured = parse_structured_fields(text)
    return ParsedResume(
        name=structured["name"],
        email=structured["email"],
        phone=structured["phone"],
        education=structured["education"],
        skills=structured["skills"],
        projects=structured["projects"],
        experience=structured["experience"],
        certificates=structured["certificates"],
        raw_text=text,
        source_file_name=source_file_name,
        parsed_at=datetime.now(timezone.utc).isoformat(),
    )


def parse_resume_bytes(file_name: str, file_bytes: bytes) -> dict:
    text = extract_text_from_bytes(file_name, file_bytes)
    parsed = parse_resume_text(text, source_file_name=file_name)
    return parsed.to_dict()


def parse_resume_file(file_path: str) -> dict:
    text = extract_text_from_file(file_path)
    parsed = parse_resume_text(text, source_file_name=Path(file_path).name)
    return parsed.to_dict()
