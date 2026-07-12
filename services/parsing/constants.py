from __future__ import annotations

import re


EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(
    r"(?:(?:\+?\d{1,3})[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}"
)

SECTION_ALIASES = {
    "education": ["education", "academic background", "academics"],
    "skills": ["skills", "technical skills", "core skills"],
    "projects": ["projects", "project experience", "selected projects"],
    "experience": ["experience", "work experience", "professional experience", "employment history"],
    "certificates": ["certificates", "certifications", "licenses", "credentials"],
}
