from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pdfplumber
from docx import Document


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    lines: list[str] = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                lines.append(text)
    return "\n".join(lines).strip()


def extract_text_from_docx_bytes(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_text_from_file(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()
    with open(file_path, "rb") as file_handle:
        file_bytes = file_handle.read()

    if extension == ".pdf":
        return extract_text_from_pdf_bytes(file_bytes)

    if extension == ".docx":
        return extract_text_from_docx_bytes(file_bytes)

    raise ValueError("Only PDF and DOCX files are supported.")


def extract_text_from_bytes(file_name: str, file_bytes: bytes) -> str:
    extension = Path(file_name).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf_bytes(file_bytes)

    if extension == ".docx":
        return extract_text_from_docx_bytes(file_bytes)

    raise ValueError("Only PDF and DOCX files are supported.")
