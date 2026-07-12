import streamlit as st
from services.parsing.resume_parser import parse_resume_bytes
from services.ai.gemini_service import GeminiService, GeminiServiceError
from services.voice.session import load_voice_questions, set_voice_interview_context
from utils.ui import apply_theme, render_hero


def render() -> None:
    apply_theme()
    render_hero(
        "Upload Resume & Setup Interview",
        "Upload your resume in PDF or DOCX format to extract your skills and experience. Custom interview questions will be generated based on your background.",
        eyebrow="Resume Intake"
    )

    st.write("")

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("1. Select Resume Document")

        uploaded_file = st.file_uploader(
            "Drag & drop a PDF or DOCX file",
            type=["pdf", "docx"],
            accept_multiple_files=False,
            help="Accepted formats: PDF, DOCX"
        )

        st.write("")

        # Save parsed data in session state
        if uploaded_file is not None:
            if "last_uploaded_name" not in st.session_state or st.session_state["last_uploaded_name"] != uploaded_file.name:
                with st.spinner("Extracting resume data..."):
                    try:
                        file_bytes = uploaded_file.getvalue()
                        parsed_data = parse_resume_bytes(uploaded_file.name, file_bytes)
                        st.session_state["resume_data"] = parsed_data
                        st.session_state["last_uploaded_name"] = uploaded_file.name
                        st.success("Resume parsed successfully!")
                    except Exception as e:
                        st.error(f"Failed to parse resume: {e}. Please try another file.")
                        st.session_state["resume_data"] = None

        st.subheader("2. Interview Configuration")
        role = st.text_input("Target Role", value=st.session_state.get("target_role", "Software Engineer"), placeholder="e.g. Python Developer, React Architect")
        experience_level = st.selectbox("Experience Level", ["Entry-Level / Graduate", "Junior Developer", "Mid-Level Engineer", "Senior Architect", "Lead / Manager"])
        difficulty = st.selectbox("Question Difficulty", ["Easy", "Medium", "Hard"])
        num_questions = st.slider("Number of Questions", min_value=3, max_value=10, value=5)

        # Retrieve Gemini API Key from session state or environment
        api_key = st.session_state.get("custom_gemini_api_key", "")

        st.write("")

        start_btn = st.button("Generate Questions & Start Interview ➔", use_container_width=True)
        if start_btn:
            if not st.session_state.get("resume_data"):
                st.error("Please upload and successfully parse a resume before starting the interview.")
            elif not role.strip():
                st.error("Please enter a target role.")
            else:
                # Save configuration
                st.session_state["target_role"] = role.strip()
                st.session_state["experience_level"] = experience_level
                st.session_state["difficulty"] = difficulty
                st.session_state["num_questions"] = num_questions

                with st.spinner("Generating custom questions using Gemini AI..."):
                    try:
                        # Instantiate service using custom key
                        service = GeminiService(api_key=api_key if api_key else None)
                        questions = service.generate_questions(
                            resume_data=st.session_state["resume_data"],
                            role=role.strip(),
                            experience_level=experience_level,
                            difficulty=difficulty,
                            count=num_questions,
                            api_key=api_key if api_key else None
                        )

                        # Set up voice session
                        load_voice_questions(
                            questions,
                            {
                                "role": role.strip(),
                                "experience_level": experience_level,
                                "difficulty": difficulty,
                            }
                        )
                        set_voice_interview_context(
                            resume_text=st.session_state["resume_data"].get("raw_text", ""),
                            role=role.strip()
                        )

                        # Transition page
                        st.session_state["active_page"] = "Interview"
                        st.rerun()

                    except GeminiServiceError as err:
                        st.error(f"Gemini API Error: {err}")
                    except Exception as err:
                        st.error(f"An unexpected error occurred during question generation: {err}")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.subheader("Resume Analysis Preview")

        resume_data = st.session_state.get("resume_data")

        if resume_data:
            # Display extracted name and contact
            name = resume_data.get("name") or "Not found"
            email = resume_data.get("email") or "Not found"
            phone = resume_data.get("phone") or "Not found"

            st.markdown(f"""
            <div class="card-soft" style="margin-bottom: 1rem;">
                <div class="muted" style="font-size: 0.8rem; text-transform: uppercase;">Candidate Details</div>
                <div style="font-weight: 700; font-size: 1.2rem; margin-top: 0.25rem;">{name}</div>
                <div class="muted" style="font-size: 0.9rem; margin-top: 0.15rem;">✉️ {email} &nbsp;|&nbsp; 📞 {phone}</div>
            </div>
            """, unsafe_allow_html=True)

            # Skills
            skills = resume_data.get("skills", [])
            st.markdown("<h5>Extracted Skills</h5>", unsafe_allow_html=True)
            if skills:
                badges_html = "".join([f'<span class="badge" style="margin-right: 0.4rem; margin-bottom: 0.4rem;">{s}</span>' for s in skills[:20]])
                if len(skills) > 20:
                    badges_html += f'<span class="badge">+ {len(skills)-20} more</span>'
                st.markdown(f'<div style="margin-bottom: 1rem;">{badges_html}</div>', unsafe_allow_html=True)
            else:
                st.caption("No skills detected.")

            # Projects
            projects = resume_data.get("projects", [])
            st.markdown("<h5>Projects</h5>", unsafe_allow_html=True)
            if projects:
                for proj in projects[:3]:
                    st.markdown(f'<div class="card-soft" style="margin-bottom: 0.5rem; font-size: 0.9rem;">🛠️ {proj}</div>', unsafe_allow_html=True)
                if len(projects) > 3:
                    st.caption(f"And {len(projects)-3} other projects...")
            else:
                st.caption("No project lines detected.")

            # Experience
            experience = resume_data.get("experience", [])
            st.markdown("<h5>Experience</h5>", unsafe_allow_html=True)
            if experience:
                for exp in experience[:3]:
                    st.markdown(f'<div class="card-soft" style="margin-bottom: 0.5rem; font-size: 0.9rem;">💼 {exp}</div>', unsafe_allow_html=True)
                if len(experience) > 3:
                    st.caption(f"And {len(experience)-3} other experience entries...")
            else:
                st.caption("No experience lines detected.")

            # Education
            education = resume_data.get("education", [])
            st.markdown("<h5>Education</h5>", unsafe_allow_html=True)
            if education:
                for edu in education[:2]:
                    st.markdown(f'<div class="card-soft" style="margin-bottom: 0.5rem; font-size: 0.9rem;">🎓 {edu}</div>', unsafe_allow_html=True)
            else:
                st.caption("No education details detected.")

        else:
            st.info("Upload a PDF/DOCX file to view the extraction results here.")
            st.markdown("""
            <div class="card-soft" style="margin-top: 1rem; border-style: dashed;">
                <div class="muted" style="text-align: center; padding: 2rem 1rem;">
                    Upload your resume to see structured metadata preview.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
