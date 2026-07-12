import streamlit as st
from streamlit_mic_recorder import speech_to_text
from services.voice.session import (
    initialize_voice_session,
    get_current_voice_question,
    get_voice_progress,
    mark_voice_answer,
    advance_voice_question,
    repeat_voice_question
)
from services.voice.tts import render_text_to_speech
from services.ai.gemini_service import GeminiService, GeminiServiceError
from utils.ui import apply_theme, render_hero


def render() -> None:
    apply_theme()
    initialize_voice_session()

    # If no questions generated yet
    if not st.session_state.get("voice_questions"):
        render_hero(
            "Voice Interview Studio",
            "Generate questions from your resume to begin.",
            eyebrow="Waiting for Setup"
        )
        st.write("")
        st.info("Please upload a resume and configure your settings to start the interview.")
        if st.button("➔ Go to Resume Upload", use_container_width=True):
            st.session_state["active_page"] = "Resume Upload"
            st.rerun()
        return

    progress = get_voice_progress()
    current_idx = st.session_state.get("voice_question_index", 0)

    render_hero(
        f"Mock Interview Session",
        f"Practice speaking your answers clearly. Review the transcript, refine your answer, and click submit.",
        eyebrow=f"Active Role: {st.session_state.get('target_role', 'Developer')}"
    )

    st.write("")

    # Progress bar and status indicator
    total_q = progress["total"]
    current_q = progress["current"]
    pct = (current_q - 1) / total_q if total_q > 0 else 0
    st.progress(pct)

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <span class="badge">Question {current_q} of {total_q}</span>
            <span class="badge" style="color: #67e8f9; border-color: rgba(103, 232, 249, 0.3);">
                Difficulty: {st.session_state.get('difficulty', 'Medium')}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # State check: has the interview been completed or ended?
    if st.session_state.get("voice_ended"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎉 Interview Completed!")
        st.write("You have answered all questions. You can review your transcript below before requesting AI evaluation.")

        # Show full transcript
        for item in st.session_state.get("voice_transcript", []):
            status_color = "#34d399" if item.get("status") == "answered" else "#fb7185"
            status_text = "Answered" if item.get("status") == "answered" else "Skipped"
            st.markdown(
                f"""
                <div class="card-soft" style="margin-bottom: 0.85rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>Q{item['question_index']}</strong>
                        <span style="color: {status_color}; font-size: 0.8rem; font-weight: 700;">{status_text}</span>
                    </div>
                    <div style="margin-top: 0.4rem; font-weight: 600;">{item['question']}</div>
                    <div class="muted" style="margin-top: 0.3rem; white-space: pre-wrap; background: rgba(0,0,0,0.2); padding: 0.5rem; border-radius: 8px;">
                        {item['answer']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        api_key = st.session_state.get("custom_gemini_api_key", "")

        st.write("")
        if st.button("Generate Detailed AI Feedback Report 📊", use_container_width=True):
            with st.spinner("Analyzing answers with Gemini AI..."):
                try:
                    service = GeminiService(api_key=api_key if api_key else None)
                    # Prepare transcript pairs
                    qa_pairs = [
                        {"question": item["question"], "answer": item["answer"]}
                        for item in st.session_state.get("voice_transcript", [])
                    ]
                    evaluation = service.evaluate_answers(
                        resume_data=st.session_state.get("resume_data", {}),
                        qa_pairs=qa_pairs,
                        role=st.session_state.get("target_role", "Developer"),
                        api_key=api_key if api_key else None
                    )
                    st.session_state["evaluation_results"] = evaluation
                    st.session_state["active_page"] = "Final Feedback"
                    st.rerun()
                except GeminiServiceError as err:
                    st.error(f"Gemini API Error: {err}")
                except Exception as err:
                    st.error(f"Evaluation failed: {err}")

        if st.button("Restart Interview", use_container_width=True):
            # Reset only voice session
            for key in ["voice_questions", "voice_question_index", "voice_transcript", "voice_ended", "voice_last_spoken_index", "evaluation_results"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state["active_page"] = "Resume Upload"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Active Question UI
    current_question = get_current_voice_question()
    if not current_question:
        st.warning("Could not load the current question.")
        return

    left_col, right_col = st.columns([1.1, 0.9], gap="large")

    with left_col:
        # Question Card
        st.markdown(
            f"""
            <div class="card" style="margin-bottom: 1rem;">
                <div class="badge" style="color: #8b5cf6; border-color: rgba(139, 92, 246, 0.3);">
                    {current_question.get('category', 'General')}
                </div>
                <h3 style="margin-top: 1rem; line-height: 1.45;">
                    {current_question.get('question', '')}
                </h3>
                <p class="muted" style="font-size: 0.88rem; margin-top: 0.5rem; margin-bottom: 0;">
                    💡 Expected signal: {current_question.get('expected_signal', 'Clear and logical reasoning.')}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Handle automatic speech synthesis on question load
        if st.session_state.get("voice_last_spoken_index") != current_idx:
            render_text_to_speech(current_question.get("question", ""))
            st.session_state["voice_last_spoken_index"] = current_idx

        # Answer input card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Your Response")

        # Set up a temporary state key for speech transcription
        temp_key = f"temp_ans_{current_idx}"
        if temp_key not in st.session_state:
            st.session_state[temp_key] = ""

        # Renders the mic recorder
        st.markdown('<div class="card-soft" style="margin-bottom: 1rem; text-align: center;">', unsafe_allow_html=True)
        st.caption("Press Start, speak your answer clearly, then press Stop when done.")
        
        transcript = speech_to_text(
            language="en",
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹️ Stop & Transcribe",
            just_once=True,
            use_container_width=True,
            key=f"voice_stt_{current_idx}"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if transcript and transcript.strip():
            # If a new transcript is captured, update session state and sync with the textbox key
            st.session_state[temp_key] = transcript.strip()
            st.session_state[f"text_area_{current_idx}"] = transcript.strip()

        # Text input fallback/review area
        user_answer = st.text_area(
            "Review or Type Your Answer:",
            value=st.session_state[temp_key],
            key=f"text_area_{current_idx}",
            height=150,
            placeholder="Your transcribed text will appear here. You can also type your answer directly."
        )

        st.write("")

        # Action Buttons row
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("Submit Answer ➔", use_container_width=True):
                trimmed_answer = st.session_state.get(f"text_area_{current_idx}", "").strip()
                if not trimmed_answer:
                    st.error("Please speak or type an answer before submitting.")
                else:
                    mark_voice_answer(trimmed_answer, status="answered")
                    # If this was the last question, we end
                    if current_idx >= len(st.session_state["voice_questions"]) - 1:
                        st.session_state["voice_ended"] = True
                    else:
                        advance_voice_question(1)
                    st.rerun()

        with btn_col2:
            if st.button("Skip Question ⏭️", use_container_width=True):
                mark_voice_answer("Skipped by candidate.", status="skipped")
                if current_idx >= len(st.session_state["voice_questions"]) - 1:
                    st.session_state["voice_ended"] = True
                else:
                    advance_voice_question(1)
                st.rerun()

        with btn_col3:
            if st.button("Clear / Retry 🔄", use_container_width=True):
                st.session_state[temp_key] = ""
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.subheader("Controls & Audio")

        if st.button("🔊 Replay Question Audio", use_container_width=True):
            repeat_voice_question()
            st.session_state["voice_last_spoken_index"] = None
            st.rerun()

        st.write("")
        st.subheader("Session Log")
        
        # Display list of previously answered questions
        voice_transcript = st.session_state.get("voice_transcript", [])
        if voice_transcript:
            for item in voice_transcript:
                status_color = "#34d399" if item.get("status") == "answered" else "#fb7185"
                status_text = "Answered" if item.get("status") == "answered" else "Skipped"
                st.markdown(
                    f"""
                    <div class="card-soft" style="margin-top: 0.5rem; font-size: 0.85rem; padding: 0.6rem 0.8rem;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong>Q{item['question_index']}</strong>
                            <span style="color: {status_color}; font-weight: 700;">{status_text}</span>
                        </div>
                        <div style="margin-top: 0.2rem; font-weight: 600; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                            {item['question']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.caption("Your progress will be logged here.")

        st.markdown("</div>", unsafe_allow_html=True)