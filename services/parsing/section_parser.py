from __future__ import annotations

from services.parsing.constants import EMAIL_PATTERN, PHONE_PATTERN, SECTION_ALIASES


def normalize_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def extract_email(text: str) -> str | None:
    match = EMAIL_PATTERN.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = PHONE_PATTERN.search(text)
    return match.group(0) if match else None


def guess_name(lines: list[str], email: str | None, phone: str | None) -> str | None:
    for line in lines[:8]:
        lowered = line.lower()
        if email and email.lower() in lowered:
            continue
        if phone and phone in line:
            continue
        if any(alias in lowered for aliases in SECTION_ALIASES.values() for alias in aliases):
            continue
        if len(line.split()) <= 6 and len(line) <= 60:
            return line
    return None


def _is_section_heading(line: str) -> str | None:
    lowered = line.strip().lower().rstrip(":")
    for section_name, aliases in SECTION_ALIASES.items():
        if lowered in aliases:
            return section_name
    return None


def parse_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {key: [] for key in SECTION_ALIASES}
    lines = normalize_lines(text)
    current_section: str | None = None

    for line in lines:
        heading = _is_section_heading(line)
        if heading:
            current_section = heading
            continue

        if current_section:
            sections[current_section].append(line)

    return sections


def flatten_section_items(section_lines: list[str]) -> list[str]:
    items: list[str] = []
    for line in section_lines:
        normalized = line.lstrip("-•*0123456789. ").strip()
        if normalized:
            items.append(normalized)
    return items


def parse_structured_fields(text: str) -> dict:
    lines = normalize_lines(text)
    email = extract_email(text)
    phone = extract_phone(text)
    name = guess_name(lines, email, phone)
    sections = parse_sections(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "education": flatten_section_items(sections["education"]),
        "skills": flatten_section_items(sections["skills"]),
        "projects": flatten_section_items(sections["projects"]),
        "experience": flatten_section_items(sections["experience"]),
        "certificates": flatten_section_items(sections["certificates"]),
    }
