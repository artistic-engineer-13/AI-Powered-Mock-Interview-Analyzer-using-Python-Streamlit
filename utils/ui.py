from __future__ import annotations

from datetime import datetime

import streamlit as st

APP_CSS = """
<style>
:root {
  --bg: #0a0f1c;
  --bg-2: #0f172a;
  --panel: rgba(15, 23, 42, 0.82);
  --panel-2: rgba(17, 24, 39, 0.92);
  --border: rgba(148, 163, 184, 0.18);  
  --text: #e5eefb;
  --muted: #91a4c7;
  --accent: #67e8f9;
  --accent-2: #8b5cf6;
  --success: #34d399;
  --warning: #fbbf24;
  --danger: #fb7185;
  --shadow: 0 24px 80px rgba(2, 6, 23, 0.42);
  --radius-xl: 28px;
  --radius-lg: 20px;
  --radius-md: 16px;
}

html, body, [class*="css"] {
  font-family: Inter, "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.55;
  color-scheme: dark;
}

.stApp {
  background:
    radial-gradient(circle at top left, rgba(103, 232, 249, 0.10), transparent 26%),
    radial-gradient(circle at top right, rgba(139, 92, 246, 0.12), transparent 28%),
    linear-gradient(180deg, #07101f 0%, #0a0f1c 48%, #060b16 100%);
  color: var(--text);
}

.block-container {
  padding-top: 1.4rem;
  padding-bottom: 1.5rem;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(8, 13, 24, 0.96) 0%, rgba(12, 18, 35, 0.96) 100%);
  border-right: 1px solid rgba(148, 163, 184, 0.12);
}

[data-testid="stSidebar"] > div {
  padding-top: 1.2rem;
}

section[data-testid="stSidebar"] .block-container {
  padding-top: 0.8rem;
}

h1, h2, h3, h4, h5, h6 {
  color: #f8fbff;
  letter-spacing: -0.03em;
}

p, li, span, label {
  color: var(--text);
}

small, .muted, .secondary {
  color: var(--muted) !important;
}

[data-testid="stHeader"] {
  background: rgba(0, 0, 0, 0);
}

[data-testid="stToolbar"] {
  right: 1rem;
}

.stButton > button, .stDownloadButton > button {
  background: linear-gradient(135deg, #67e8f9 0%, #8b5cf6 100%);
  color: #07111f;
  border: 0;
  border-radius: 14px;
  padding: 0.7rem 1rem;
  font-weight: 700;
  box-shadow: 0 12px 30px rgba(103, 232, 249, 0.18);
}

.stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 16px 34px rgba(139, 92, 246, 0.20);
}

.stButton > button:focus-visible, .stDownloadButton > button:focus-visible,
.stTextInput input:focus-visible, .stTextArea textarea:focus-visible,
.stSelectbox div[data-baseweb="select"] > div:focus-visible,
.stDateInput input:focus-visible, .stFileUploader input:focus-visible {
  outline: 2px solid rgba(103, 232, 249, 0.95) !important;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(103, 232, 249, 0.14) !important;
}

.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div, .stDateInput input {
  background: rgba(15, 23, 42, 0.75) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
}

.stFileUploader section {
  background: rgba(15, 23, 42, 0.72);
  border: 1px dashed rgba(103, 232, 249, 0.35);
  border-radius: 18px;
}

/* Sidebar Button Styling */
div.sidebar-active-btn .stButton > button, div.sidebar-inactive-btn .stButton > button {
  background: rgba(15, 23, 42, 0.55) !important;
  color: var(--text) !important;
  border: 1px solid rgba(148, 163, 184, 0.12) !important;
  border-radius: 999px !important;
  padding: 0.55rem 0.85rem !important;
  font-size: 0.92rem !important;
  font-weight: 500 !important;
  text-align: left !important;
  justify-content: flex-start !important;
  width: 100% !important;
  box-shadow: none !important;
  margin-bottom: 0.55rem !important;
  transform: none !important;
}

div.sidebar-active-btn .stButton > button {
  background: linear-gradient(135deg, rgba(103, 232, 249, 0.15), rgba(139, 92, 246, 0.16)) !important;
  border-color: rgba(103, 232, 249, 0.26) !important;
  font-weight: 700 !important;
}

div.sidebar-inactive-btn .stButton > button:hover {
  border-color: rgba(103, 232, 249, 0.26) !important;
  background: rgba(15, 23, 42, 0.72) !important;
  box-shadow: none !important;
}

.card {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.84), rgba(10, 15, 28, 0.92));
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow);
  padding: 1.25rem 1.3rem;
}

.card-soft {
  background: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: var(--radius-lg);
  padding: 1rem 1.1rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.kpi {
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(12, 18, 35, 0.96));
  border: 1px solid rgba(148, 163, 184, 0.14);
  border-radius: 22px;
  padding: 1rem 1.05rem;
  box-shadow: var(--shadow);
}

.kpi .label {
  color: var(--muted);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.09em;
}

.kpi .value {
  font-size: 1.7rem;
  font-weight: 800;
  margin-top: 0.25rem;
}

.kpi .delta {
  margin-top: 0.35rem;
  color: var(--success);
  font-size: 0.86rem;
}

.hero {
  background:
    radial-gradient(circle at top right, rgba(103, 232, 249, 0.15), transparent 25%),
    radial-gradient(circle at bottom left, rgba(139, 92, 246, 0.18), transparent 28%),
    linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(8, 13, 24, 0.96));
  border: 1px solid rgba(148, 163, 184, 0.16);
  border-radius: 32px;
  padding: 1.6rem;
  box-shadow: var(--shadow);
}

.hero h1 {
  font-size: 2.7rem;
  margin-bottom: 0.35rem;
}

.hero .eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.4rem 0.75rem;
  border-radius: 999px;
  border: 1px solid rgba(103, 232, 249, 0.22);
  background: rgba(103, 232, 249, 0.08);
  color: #c8f7ff;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.11em;
}

.hero p {
  color: var(--muted);
  max-width: 62ch;
  font-size: 1rem;
}

.nav-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 0.85rem;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.14);
  color: var(--text);
  font-size: 0.92rem;
  width: 100%;
  margin-bottom: 0.55rem;
}

.nav-pill.active {
  background: linear-gradient(135deg, rgba(103, 232, 249, 0.15), rgba(139, 92, 246, 0.16));
  border-color: rgba(103, 232, 249, 0.26);
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.42rem 0.72rem;
  border-radius: 999px;
  font-size: 0.8rem;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: rgba(15, 23, 42, 0.66);
  color: #d8e6ff;
}

.metric-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.metric-card {
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 22px;
  padding: 1rem;
}

.metric-card .title {
  color: var(--muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.metric-card .headline {
  margin-top: 0.35rem;
  font-size: 1.35rem;
  font-weight: 800;
}

.metric-card .subtle {
  color: var(--muted);
  margin-top: 0.35rem;
  font-size: 0.88rem;
}

hr {
  border-color: rgba(148, 163, 184, 0.12);
}

[data-testid="stMarkdownContainer"] a {
  color: #8eeaff;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

@media (max-width: 1100px) {
  .kpi-grid, .metric-row {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .hero h1 {
    font-size: 2.2rem;
  }
}

@media (max-width: 700px) {
  .kpi-grid, .metric-row {
    grid-template-columns: 1fr;
  }
  .hero {
    padding: 1.1rem;
  }
}
</style>
"""

NAV_ITEMS = [
    ("Home", "home"),
    ("Resume Upload", "resume_upload"),
    ("Interview", "interview"),
    ("Final Feedback", "feedback"),
]


def apply_theme() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)


def render_sidebar(active_page: str = "home") -> None:
    from utils.settings import get_settings
    settings = get_settings()

    with st.sidebar:
        st.markdown(
            """
            <div class="card" style="padding: 1.2rem; margin-bottom: 1rem;">
              <div class="badge">AI Voice Mock Interview</div>
              <h2 style="margin: 0.9rem 0 0.35rem;">Interview Studio</h2>
              <p class="muted" style="margin: 0;">A premium voice-enabled candidate interview experience powered by Gemini.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Interview Progress")
        for label, key in NAV_ITEMS:
            is_disabled = False
            # Check prerequisites
            if key == "interview" and not st.session_state.get("voice_questions"):
                is_disabled = True
            elif key == "feedback" and not st.session_state.get("evaluation_results"):
                is_disabled = True
                
            is_active = (key == active_page)
            page_name_map = {
                "home": "Home",
                "resume_upload": "Resume Upload",
                "interview": "Interview",
                "feedback": "Final Feedback"
            }
            
            if is_active:
                st.markdown('<div class="sidebar-active-btn">', unsafe_allow_html=True)
                st.button(label, key=f"nav_{key}", use_container_width=True, disabled=is_disabled)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="sidebar-inactive-btn">', unsafe_allow_html=True)
                if st.button(label, key=f"nav_{key}", use_container_width=True, disabled=is_disabled):
                    st.session_state["active_page"] = page_name_map[key]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        
        # API Key management
        st.write("")
        st.caption("AI Configuration")
        
        env_key = settings.gemini_api_key
        if not env_key:
            custom_key = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Paste your Gemini key here...",
                value=st.session_state.get("custom_gemini_api_key", ""),
                help="Get a free key from Google AI Studio"
            )
            if custom_key:
                st.session_state["custom_gemini_api_key"] = custom_key.strip()
            
            if st.session_state.get("custom_gemini_api_key"):
                st.markdown('<span class="badge" style="color: #34d399; border-color: rgba(52, 211, 153, 0.4); width: 100%; display: inline-block; text-align: center;">🔑 Custom API Key Loaded</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge" style="color: #fb7185; border-color: rgba(251, 113, 133, 0.4); width: 100%; display: inline-block; text-align: center;">⚠️ Missing API Key</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge" style="color: #34d399; border-color: rgba(52, 211, 153, 0.4); width: 100%; display: inline-block; text-align: center;">🔑 System API Key Loaded</span>', unsafe_allow_html=True)
            

            
        st.markdown(
            f"<div class='card-soft' style='margin-top: 1rem;'><div class='muted'>Session Date</div><div style='font-weight: 700; margin-top: 0.25rem;'>{datetime.now().strftime('%b %d, %Y')}</div></div>",
            unsafe_allow_html=True,
        )


def render_hero(title: str, subtitle: str, eyebrow: str = "Premium AI SaaS UI") -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div class="eyebrow">{eyebrow}</div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(items: list[tuple[str, str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value, delta) in zip(cols, items):
        with col:
            st.markdown(
                f"""
                <div class="kpi">
                  <div class="label">{label}</div>
                  <div class="value">{value}</div>
                  <div class="delta">{delta}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


from typing import List, Tuple

def render_feature_grid(features: List[Tuple[str, str]]) -> None:
    cols = st.columns(3)
    for idx, (title, body) in enumerate(features):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class="metric-card">
                  <div class="title">{title}</div>
                  <div class="headline">{body}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
