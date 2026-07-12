from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import streamlit as st


VOICE_SESSION_DEFAULTS = {
    "voice_questions": [],
    "voice_question_index": 0,
    "voice_transcript": [],
    "voice_transcript_text": "",
    "voice_started_at": None,
    "voice_ended": False,
    "voice_last_spoken_index": None,
    "voice_latest_transcript": "",
    "voice_last_processed_transcript": "",
    "voice_question_set": {},
    "voice_generation_note": "",
    "voice_resume_text": "",
    "voice_role": "",
    "voice_evaluations": [],
}


def initialize_voice_session() -> None:
    for key, value in VOICE_SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_voice_questions(questions: list[dict[str, Any]], question_set: dict[str, Any] | None = None) -> None:
    st.session_state.voice_questions = questions
    st.session_state.voice_question_index = 0
    st.session_state.voice_transcript = []
    st.session_state.voice_transcript_text = ""
    st.session_state.voice_started_at = datetime.now(timezone.utc).isoformat()
    st.session_state.voice_ended = False
    st.session_state.voice_last_spoken_index = None
    st.session_state.voice_latest_transcript = ""
    st.session_state.voice_last_processed_transcript = ""
    st.session_state.voice_question_set = question_set or {}


def set_voice_interview_context(resume_text: str, role: str) -> None:
    st.session_state.voice_resume_text = resume_text
    st.session_state.voice_role = role


def get_current_voice_question() -> dict[str, Any] | None:
    questions = st.session_state.get("voice_questions", [])
    index = int(st.session_state.get("voice_question_index", 0))
    if not questions or index < 0 or index >= len(questions):
        return None
    question = questions[index]
    return question if isinstance(question, dict) else None


def advance_voice_question(step: int = 1) -> None:
    questions = st.session_state.get("voice_questions", [])
    if not questions:
        return
    current_index = int(st.session_state.get("voice_question_index", 0))
    next_index = max(0, min(current_index + step, len(questions) - 1))
    st.session_state.voice_question_index = next_index
    st.session_state.voice_last_spoken_index = None


def repeat_voice_question() -> None:
    st.session_state.voice_last_spoken_index = None


def mark_voice_answer(answer_text: str, status: str = "answered") -> None:
    question = get_current_voice_question()
    if not question:
        return

    entry = {
        "question_index": int(st.session_state.get("voice_question_index", 0)) + 1,
        "question": question.get("question", ""),
        "answer": answer_text.strip(),
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    transcript = list(st.session_state.get("voice_transcript", []))
    transcript.append(entry)
    st.session_state.voice_transcript = transcript
    st.session_state.voice_transcript_text = "\n\n".join(
        [
            f"Q{item['question_index']}: {item['question']}\nA: {item['answer']}"
            for item in transcript
        ]
    )
    st.session_state.voice_latest_transcript = answer_text.strip()
    st.session_state.voice_last_processed_transcript = answer_text.strip()


def end_voice_interview() -> None:
    st.session_state.voice_ended = True


def get_voice_progress() -> dict[str, int]:
    questions = st.session_state.get("voice_questions", [])
    answered = len([item for item in st.session_state.get("voice_transcript", []) if item.get("status") == "answered"])
    skipped = len([item for item in st.session_state.get("voice_transcript", []) if item.get("status") == "skipped"])
    total = len(questions)
    current = min(int(st.session_state.get("voice_question_index", 0)) + 1, total if total else 0)
    return {"total": total, "answered": answered, "skipped": skipped, "current": current}
