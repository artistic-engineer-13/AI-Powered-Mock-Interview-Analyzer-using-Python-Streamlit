from __future__ import annotations

import streamlit as st
from utils.ui import apply_theme, render_sidebar
from pages import home, resume_upload, interview, feedback

# -------------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="AI Voice Mock Interview Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global dark theme and styles
apply_theme()

# -------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Home"

# Mapping of page names to rendering functions
PAGES = {
    "Home": home.render,
    "Resume Upload": resume_upload.render,
    "Interview": interview.render,
    "Final Feedback": feedback.render,
}

# Ensure the active page is valid
if st.session_state["active_page"] not in PAGES:
    st.session_state["active_page"] = "Home"

# Render the sidebar showing progress and configuration status
# Match visual key for styling (e.g. "home", "resume_upload", "interview", "feedback")
active_key = st.session_state["active_page"].lower().replace(" ", "_")
render_sidebar(active_page=active_key)

# -------------------------------------------------------
# Render Selected Page
# -------------------------------------------------------
PAGES[st.session_state["active_page"]]()
