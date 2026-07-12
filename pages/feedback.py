import streamlit as st
from utils.ui import apply_theme, render_hero


def render() -> None:
    apply_theme()

    # Verify if evaluation results exist in session state
    evaluation = st.session_state.get("evaluation_results")

    if not evaluation:
        render_hero(
            "Evaluation Feedback Studio",
            "No active interview transcript evaluated yet.",
            eyebrow="No Data"
        )
        st.write("")
        st.info("Please complete an interview session to generate and view the feedback report.")
        if st.button("➔ Start A Setup Now", use_container_width=True):
            st.session_state["active_page"] = "Resume Upload"
            st.rerun()
        return

    # Header section
    role = st.session_state.get("target_role", "Developer")
    render_hero(
        f"AI Performance Assessment",
        f"Granular evaluation metrics and learning roadmap generated for the {role} interview.",
        eyebrow="Evaluation Feedback"
    )

    st.write("")

    # Scores section
    col_score, col_metrics = st.columns([1, 1.5], gap="large")

    with col_score:
        st.markdown('<div class="card" style="text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 2rem 1rem;">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin: 0;'>Overall Rating</h4>", unsafe_allow_html=True)
        
        overall = evaluation.get("overall_score", 70)
        
        # A beautiful glassmorphic KPI ring or score box
        st.markdown(
            f"""
            <div style="
                margin: 2rem 0;
                width: 150px;
                height: 150px;
                border-radius: 50%;
                background: radial-gradient(circle at center, rgba(139, 92, 246, 0.2), rgba(103, 232, 249, 0.25));
                border: 4px solid #67e8f9;
                box-shadow: 0 0 30px rgba(103, 232, 249, 0.35);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            ">
                <span style="font-size: 3.5rem; font-weight: 900; color: #f8fbff; line-height: 1;">{overall}</span>
                <span style="font-size: 0.8rem; color: #91a4c7; font-weight: 700; text-transform: uppercase; margin-top: 0.3rem;">/ 100</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Determine verdict
        verdict = "Excellent Match" if overall >= 85 else "Strong Fit" if overall >= 70 else "Needs Preparation"
        badge_color = "#34d399" if overall >= 85 else "#fbbf24" if overall >= 70 else "#fb7185"
        
        st.markdown(
            f"""
            <div>
                <span class="badge" style="border-color: {badge_color}; color: {badge_color}; font-size: 1rem; font-weight: 700;">
                    {verdict}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_metrics:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.subheader("Assessment Dimensions")

        # Metric keys to render
        dimensions = [
            ("Technical Knowledge", evaluation.get("technical_knowledge", 70), "#67e8f9"),
            ("Communication Skills", evaluation.get("communication", 70), "#8b5cf6"),
            ("Confidence & Delivery", evaluation.get("confidence", 70), "#34d399"),
            ("Completeness & Detail", evaluation.get("completeness", 70), "#fbbf24"),
            ("Grammar & Clarity", evaluation.get("grammar", 70), "#fb7185")
        ]

        for label, val, color in dimensions:
            st.markdown(
                f"""
                <div style="margin-bottom: 0.95rem;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.25rem;">
                        <strong>{label}</strong>
                        <span style="color: {color}; font-weight: 700;">{val} / 100</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Render a custom progress bar using st.progress
            st.progress(val / 100)

        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Summary Paragraph
    st.write("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Performance Summary")
    st.write(evaluation.get("summary", "Evaluation processed successfully."))
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # Strengths and Weaknesses
    col_str, col_weak = st.columns(2, gap="large")

    with col_str:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #34d399;'>🟢 Key Strengths</h3>", unsafe_allow_html=True)
        strengths = evaluation.get("strengths", [])
        if strengths:
            for s in strengths:
                st.markdown(f"""
                <div class="card-soft" style="margin-bottom: 0.6rem; border-left: 3px solid #34d399;">
                    {s}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No specific strengths listed.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_weak:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #fb7185;'>🔴 Areas for Improvement</h3>", unsafe_allow_html=True)
        weaknesses = evaluation.get("weaknesses", [])
        if weaknesses:
            for w in weaknesses:
                st.markdown(f"""
                <div class="card-soft" style="margin-bottom: 0.6rem; border-left: 3px solid #fb7185;">
                    {w}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No specific improvements listed.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Actionable Suggestions & Study Roadmap
    st.write("")
    col_sug, col_map = st.columns([1, 1], gap="large")

    with col_sug:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #fbbf24;'>💡 Actionable Suggestions</h3>", unsafe_allow_html=True)
        suggestions = evaluation.get("suggestions", [])
        if suggestions:
            for s in suggestions:
                st.markdown(f"""
                <div class="card-soft" style="margin-bottom: 0.6rem; border-left: 3px solid #fbbf24;">
                    {s}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No specific suggestions listed.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_map:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #67e8f9;'>📚 Study Roadmap & Technologies</h3>", unsafe_allow_html=True)
        topics = evaluation.get("recommended_topics", [])
        if topics:
            st.write("We recommend focusing on the following technologies and topics to address gaps discovered:")
            st.write("")
            badges_html = "".join([f'<span class="badge" style="margin-right: 0.5rem; margin-bottom: 0.5rem; border-color: rgba(103, 232, 249, 0.4); font-size: 0.9rem; padding: 0.5rem 0.8rem; font-weight: 600; color: #67e8f9;">{t}</span>' for t in topics])
            st.markdown(f'<div>{badges_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("No study topics recommended.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    
    # Restart Button
    if st.button("Start A New Interview Prep Session 🔄", use_container_width=True):
        # Reset entire voice and evaluation states
        keys_to_clear = [
            "voice_questions",
            "voice_question_index",
            "voice_transcript",
            "voice_ended",
            "voice_last_spoken_index",
            "evaluation_results",
            "resume_data",
            "last_uploaded_name",
            "target_role"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state["active_page"] = "Home"
        st.rerun()
