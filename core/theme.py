"""
core/theme.py
Shared visual identity for every page: color system, typography, Plotly
template, and the CSS that gives the site an actual design instead of
default-Streamlit gray boxes.
"""

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

DARK_BG = "#c4c6c9"
PANEL_BG = "#D3D3D480"
PANEL_BORDER = "#c9cacb"

LINEAR_ALGEBRA = "#00e5ff"
CALCULUS = "#a855f7"
PROBABILITY = "#22c55e"
QUANT_FINANCE = "#f97316"

TEXT_PRIMARY = "#000206"
TEXT_MUTED = "#000610"
GRID_LINE = "#00050c"

HEADING_FONT = "'Space Grotesk', 'Inter', sans-serif"
BODY_FONT = "'Inter', -apple-system, sans-serif"

PILLAR_COLORS = {
    "Linear Algebra": LINEAR_ALGEBRA,
    "Calculus": CALCULUS,
    "Probability & Stats": PROBABILITY,
    "Quant Finance": QUANT_FINANCE,
}


def build_plotly_template() -> go.layout.Template:
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=BODY_FONT, color=TEXT_PRIMARY, size=13),
        xaxis=dict(gridcolor=GRID_LINE, zerolinecolor=GRID_LINE, color=TEXT_MUTED),
        yaxis=dict(gridcolor=GRID_LINE, zerolinecolor=GRID_LINE, color=TEXT_MUTED),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return template


pio.templates["quant_dark"] = build_plotly_template()


def inject_base_css():
    """Call once per page, right after st.set_page_config()."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: {BODY_FONT};
        }}
        h1, h2, h3 {{
            font-family: {HEADING_FONT} !important;
            letter-spacing: -0.01em;
        }}

        .hero-title {{
            font-family: {HEADING_FONT};
            font-weight: 700;
            font-size: 2.4rem;
            background: linear-gradient(90deg, {LINEAR_ALGEBRA}, {PROBABILITY});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }}
        .hero-subtitle {{
            color: {TEXT_MUTED};
            font-size: 1.05rem;
            margin-top: 6px;
            line-height: 1.5;
        }}

        .concept-panel {{
            background: {PANEL_BG};
            border: 1px solid {PANEL_BORDER};
            border-radius: 14px;
            padding: 20px 22px;
            margin-bottom: 14px;
        }}
        .concept-panel h4 {{
            margin-top: 0;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {TEXT_MUTED};
            font-weight: 600;
        }}
        .concept-panel p {{
            color: {TEXT_PRIMARY};
            line-height: 1.65;
            font-size: 1rem;
        }}

        a[data-testid="stPageLink-NavLink"] {{
            background-color: {PANEL_BG} !important;
            border: 1px solid {PANEL_BORDER} !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            margin-bottom: 10px !important;
            transition: border-color 0.15s ease;
        }}
        a[data-testid="stPageLink-NavLink"]:hover {{
            border-color: {LINEAR_ALGEBRA} !important;
        }}
        a[data-testid="stPageLink-NavLink"] p {{
            font-family: {HEADING_FONT} !important;
            font-weight: 500 !important;
        }}

        [data-testid="stMetric"] {{
            background: {PANEL_BG};
            border: 1px solid {PANEL_BORDER};
            border-radius: 12px;
            padding: 14px 16px;
        }}
        [data-testid="stMetricLabel"] {{
            color: {TEXT_MUTED} !important;
        }}

        hr {{
            border-color: {PANEL_BORDER} !important;
        }}

        @media (max-width: 640px) {{
            .block-container {{
                padding-top: 1.25rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
            .hero-title {{ font-size: 1.8rem; }}
            .hero-subtitle {{ font-size: 0.95rem; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    with st.sidebar:
        st.markdown(
            f"<div style='font-family:{HEADING_FONT}; font-weight:700; "
            f"font-size:1.3rem; color:{LINEAR_ALGEBRA};'>ThefacelessQuant</div>"
            f"<p style='color:{TEXT_MUTED}; font-size:0.85rem; margin-top:2px;'>"
            "A daily study of quantitative finance</p><hr>",
            unsafe_allow_html=True,
        )


def concept_panel(heading: str, body_html: str):
    st.markdown(
        f"<div class='concept-panel'><h4>{heading}</h4>{body_html}</div>",
        unsafe_allow_html=True,
    )
