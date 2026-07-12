import streamlit as st
from utils.ui import apply_theme, render_hero

def render() -> None:
    apply_theme()
    render_hero(
        title="AI Voice Mock Interview Studio",
        subtitle="Refine your skills with a smart, real-time voice interview simulator powered by Gemini AI. Upload your resume to start practicing tailored questions and receive a comprehensive scoring audit.",
        eyebrow="AI-Powered Practice"
    )

    st.write("")

    # Grid of core functionalities
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1rem; margin-bottom: 2rem;">
        <div class="card">
            <h3 style="margin-top: 0; color: #67e8f9; display: flex; align-items: center; gap: 0.5rem;">
                <span>📄</span> Resume Parsing
            </h3>
            <p class="muted" style="margin-bottom: 0;">Upload any standard PDF or DOCX resume. The engine extracts your core projects, skills, experience, and educational background instantly.</p>
        </div>
        <div class="card">
            <h3 style="margin-top: 0; color: #8b5cf6; display: flex; align-items: center; gap: 0.5rem;">
                <span>🎯</span> Targeted Questions
            </h3>
            <p class="muted" style="margin-bottom: 0;">Gemini generates interview questions mapped 1:1 with your experience. No generic templates—every session is custom-tailored to you.</p>
        </div>
        <div class="card">
            <h3 style="margin-top: 0; color: #34d399; display: flex; align-items: center; gap: 0.5rem;">
                <span>🎙️</span> Voice Integration
            </h3>
            <p class="muted" style="margin-bottom: 0;">Hear questions spoken aloud in high quality. Use speech recognition to capture your responses and review live transcriptions.</p>
        </div>
        <div class="card">
            <h3 style="margin-top: 0; color: #fbbf24; display: flex; align-items: center; gap: 0.5rem;">
                <span>📊</span> AI Performance Audit
            </h3>
            <p class="muted" style="margin-bottom: 0;">Get quantified feedback on your communication, technical competence, confidence, grammar, and completeness, along with a detailed study path.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered start button
    st.write("")
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        if st.button("Start Your Interview Prep 🚀", use_container_width=True):
            st.session_state["active_page"] = "Resume Upload"
            st.rerun()
