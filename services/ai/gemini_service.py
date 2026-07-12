from __future__ import annotations

import os
import json
import re
from typing import Any
from google import genai
from utils.settings import get_settings


class GeminiServiceError(RuntimeError):
    pass


class GeminiService:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key or ""
        # Single source of truth from env, falling back to models/gemini-3.5-flash
        self.model = model or os.getenv("GEMINI_MODEL", "models/gemini-3.5-flash")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                pass

    def _get_client(self, api_key: str | None = None) -> genai.Client:
        key = api_key or self.api_key
        if not key:
            raise GeminiServiceError(
                "Gemini API key is not configured. Please set it in the .env file or enter it in the application sidebar."
            )
        if not self.client or key != self.api_key:
            self.client = genai.Client(api_key=key)
            self.api_key = key
        return self.client

    def generate_questions(
        self,
        resume_data: dict[str, Any],
        role: str,
        experience_level: str,
        difficulty: str,
        count: int = 5,
        api_key: str | None = None
    ) -> list[dict[str, Any]]:
        client = self._get_client(api_key)

        resume_context = f"""
        Name: {resume_data.get('name', 'Candidate')}
        Skills: {', '.join(resume_data.get('skills', []))}
        Projects: {'; '.join(resume_data.get('projects', []))}
        Experience: {'; '.join(resume_data.get('experience', []))}
        Education: {'; '.join(resume_data.get('education', []))}
        """

        prompt = (
            f"You are an expert interview coach. Generate exactly {count} interview questions in JSON only. "
            f"The questions must be generated based ONLY on the candidate's resume context. "
            f"Target Role: {role}. Experience level: {experience_level}. Difficulty: {difficulty}. "
            "Make each question specific, practical, and highly relevant to the candidate's projects, technologies, and experience. "
            "Return JSON with this exact schema:\n"
            "{\n"
            "  \"questions\": [\n"
            "    {\n"
            "      \"question\": \"string\",\n"
            "      \"category\": \"string\",\n"
            "      \"expected_signal\": \"string\",\n"
            "      \"difficulty\": \"string\"\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "Do not include markdown or explanations. Return pure JSON text.\n"
            f"Resume context:\n{resume_context}"
        )

        try:
            # Every call resolved dynamically using os.getenv
            target_model = os.getenv("GEMINI_MODEL", "models/gemini-3.5-flash")
            response = client.models.generate_content(model=target_model, contents=prompt)
            raw_text = response.text or ""
            parsed = self._parse_json_response(raw_text)
            questions = parsed.get("questions", [])
            return self._normalize_questions(questions, count)
        except Exception as exc:
            raise GeminiServiceError(f"Failed to generate questions: {exc}")

    def evaluate_answers(
        self,
        resume_data: dict[str, Any],
        qa_pairs: list[dict[str, str]],
        role: str,
        api_key: str | None = None
    ) -> dict[str, Any]:
        client = self._get_client(api_key)

        resume_context = f"""
        Name: {resume_data.get('name', 'Candidate')}
        Skills: {', '.join(resume_data.get('skills', []))}
        Projects: {'; '.join(resume_data.get('projects', []))}
        Experience: {'; '.join(resume_data.get('experience', []))}
        Education: {'; '.join(resume_data.get('education', []))}
        """

        qa_context = ""
        for idx, item in enumerate(qa_pairs):
            qa_context += f"Question {idx+1}: {item.get('question')}\nAnswer: {item.get('answer')}\n\n"

        prompt = (
            "You are an expert interview evaluator. Evaluate the candidate's performance based on the resume and the interview dialogue. "
            "Return JSON only. "
            "Evaluate these criteria carefully and return a JSON object with these exact keys:\n"
            "1. overall_score (integer 0-100)\n"
            "2. communication (integer 0-100)\n"
            "3. technical_knowledge (integer 0-100)\n"
            "4. confidence (integer 0-100)\n"
            "5. completeness (integer 0-100)\n"
            "6. grammar (integer 0-100)\n"
            "7. strengths (list of strings)\n"
            "8. weaknesses (list of strings)\n"
            "9. suggestions (list of strings)\n"
            "10. recommended_topics (list of strings representing recommended technologies/topics to study)\n"
            "11. summary (a concise paragraph summarizing the performance)\n\n"
            "Return JSON with this exact schema:\n"
            "{\n"
            "  \"overall_score\": 85,\n"
            "  \"communication\": 80,\n"
            "  \"technical_knowledge\": 90,\n"
            "  \"confidence\": 85,\n"
            "  \"completeness\": 80,\n"
            "  \"grammar\": 90,\n"
            "  \"strengths\": [\"string\"],\n"
            "  \"weaknesses\": [\"string\"],\n"
            "  \"suggestions\": [\"string\"],\n"
            "  \"recommended_topics\": [\"string\"],\n"
            "  \"summary\": \"string\"\n"
            "}\n"
            "Do not include markdown or explanations.\n"
            f"Candidate Resume:\n{resume_context}\n"
            f"Target Role: {role}\n"
            f"Interview Transcript:\n{qa_context}"
        )

        try:
            # Every call resolved dynamically using os.getenv
            target_model = os.getenv("GEMINI_MODEL", "models/gemini-3.5-flash")
            response = client.models.generate_content(model=target_model, contents=prompt)
            raw_text = response.text or ""
            parsed = self._parse_json_response(raw_text)
            return self._normalize_evaluation(parsed)
        except Exception as exc:
            raise GeminiServiceError(f"Failed to evaluate answers: {exc}")

    def _parse_json_response(self, raw_text: str) -> dict[str, Any]:
        if not raw_text.strip():
            return {}

        json_text = raw_text.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", json_text, re.DOTALL | re.IGNORECASE)
        if fenced:
            json_text = fenced.group(1).strip()

        try:
            parsed = json.loads(json_text)
            return parsed if isinstance(parsed, dict) else {"result": parsed}
        except json.JSONDecodeError:
            start = json_text.find("{")
            end = json_text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    parsed = json.loads(json_text[start : end + 1])
                    return parsed if isinstance(parsed, dict) else {"result": parsed}
                except json.JSONDecodeError:
                    return {}
            return {}

    def _normalize_questions(self, questions: Any, count: int) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []
        if not isinstance(questions, list):
            questions = []

        for item in questions:
            if not isinstance(item, dict):
                continue
            question = str(item.get("question", "")).strip()
            if not question:
                continue
            normalized.append(
                {
                    "question": question,
                    "category": str(item.get("category", "General")).strip(),
                    "expected_signal": str(item.get("expected_signal", "")).strip(),
                    "difficulty": str(item.get("difficulty", "Medium")).strip(),
                }
            )

        normalized = normalized[:count]

        # Fallback if empty
        if not normalized:
            normalized = [
                {
                    "question": "Introduce yourself and walk me through your resume.",
                    "category": "Introduction",
                    "expected_signal": "Communication and confidence.",
                    "difficulty": "Easy",
                },
                {
                    "question": "Explain your most important project in detail.",
                    "category": "Projects",
                    "expected_signal": "Ownership and architecture.",
                    "difficulty": "Medium",
                },
                {
                    "question": "What technical challenge did you face and how did you solve it?",
                    "category": "Problem Solving",
                    "expected_signal": "Analytical thinking.",
                    "difficulty": "Medium",
                },
                {
                    "question": "If you could improve one project from your resume, what would you change?",
                    "category": "Design",
                    "expected_signal": "Critical thinking.",
                    "difficulty": "Medium",
                },
                {
                    "question": "Why should we hire you for this role?",
                    "category": "HR",
                    "expected_signal": "Confidence and communication.",
                    "difficulty": "Easy",
                },
            ]
        return normalized

    def _normalize_evaluation(self, data: dict[str, Any]) -> dict[str, Any]:
        def to_int(value: Any, default: int = 70) -> int:
            try:
                value = int(value)
                return max(0, min(100, value))
            except Exception:
                return default

        def to_list(value: Any) -> list[str]:
            if isinstance(value, list):
                return [str(v).strip() for v in value if str(v).strip()]
            if isinstance(value, str):
                return [value]
            return []

        return {
            "overall_score": to_int(data.get("overall_score"), 70),
            "communication": to_int(data.get("communication"), 70),
            "technical_knowledge": to_int(data.get("technical_knowledge"), 70),
            "confidence": to_int(data.get("confidence"), 70),
            "completeness": to_int(data.get("completeness"), 70),
            "grammar": to_int(data.get("grammar"), 70),
            "strengths": to_list(data.get("strengths") or data.get("strength", [])),
            "weaknesses": to_list(data.get("weaknesses") or data.get("weakness", [])),
            "suggestions": to_list(data.get("suggestions") or data.get("suggestion", [])),
            "recommended_topics": to_list(data.get("recommended_topics") or data.get("recommended_technologies", [])),
            "summary": str(data.get("summary", "Interview evaluation completed successfully.")).strip(),
        }