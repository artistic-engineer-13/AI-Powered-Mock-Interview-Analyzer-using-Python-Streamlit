from __future__ import annotations

import json

import streamlit.components.v1 as components


def render_text_to_speech(text: str, language: str = "en-US", rate: float = 1.0, pitch: float = 1.0) -> None:
    safe_text = json.dumps(text)
    safe_language = json.dumps(language)
    components.html(
        f"""
        <div></div>
        <script>
          const text = {safe_text};
          const lang = {safe_language};
          if (window.speechSynthesis && text) {{
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = lang;
            utterance.rate = {rate};
            utterance.pitch = {pitch};
            window.speechSynthesis.speak(utterance);
          }}
        </script>
        """,
        height=0,
    )
