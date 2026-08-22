"""
core/theme.py
Shared visual brand + mobile-friendly layout helpers for every page in the app.
Import and call inject_base_css() + render_sidebar_brand() at the top of Home.py
and every file in pages/ so the whole site looks and behaves like one product.
"""

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

DARK_BG = "#0a0e1a"
PANEL_BG = "#111827"

LINEAR_ALGEBRA = "#00e5ff"   # cyan
CALCULUS = "#a855f7"         # purple
PROBABILITY = "#22c55e"      # green
QUANT_FINANCE = "#f97316"    # orange

TEXT_PRIMARY = "#e5e7eb"
TEXT_MUTED = "#9ca3af"
GRID_LINE = "#1f2937"
FONT_FAMILY = "Inter, -apple-system, sans-serif"

PILLAR_COLORS = {
    "Linear Algebra": LINEAR_ALGEBRA,
    "Calculus": CALCULUS,
    "Probability & Stats": PROBABILITY,
    "Quant Finance": QUANT_FINANCE,
}


def build_plotly_template() -> go.layout.Template:
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_PRIMARY, size=14),
        xaxis=dict(gridcolor=GRID_LINE, zerolinecolor=GRID_LINE, color=TEXT_MUTED),
        yaxis=dict(gridcolor=GRID_LINE, zerolinecolor=GRID_LINE, color=TEXT_MUTED),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return template


pio.templates["quant_dark"] = build_plotly_template()


def inject_base_css():
    """Call once per page (top of file, right after st.set_page_config).
    Makes tap targets bigger, text readable, and cards stack cleanly on phones —
    since many mobile users never open the sidebar at all.
    """
    st.markdown(
        f"""
        <style>
        /* Bigger, thumb-friendly tap targets everywhere */
        button, a[data-testid="stPageLink-NavLink"] {{
            min-height: 48px !important;
        }}

        /* Page links rendered as branded cards */
        a[data-testid="stPageLink-NavLink"] {{
            background-color: {PANEL_BG} !important;
            border: 1px solid {GRID_LINE} !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            margin-bottom: 8px !important;
        }}
        a[data-testid="stPageLink-NavLink"]:hover {{
            border-color: {LINEAR_ALGEBRA} !important;
        }}

        /* Shrink top padding on mobile so content starts higher */
        @media (max-width: 640px) {{
            .block-container {{
                padding-top: 1.5rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
            h1 {{ font-size: 1.6rem !important; }}
            h2 {{ font-size: 1.25rem !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    """Sidebar is kept for branding + Streamlit's auto page list (desktop users rely
    on it), but nothing important is EVER sidebar-only — see nav cards on Home.py."""
    with st.sidebar:
        st.markdown(
            f"<h2 style='color:{LINEAR_ALGEBRA}; margin-bottom:0;'>ThefacelessQuant</h2>"
            f"<p style='color:{TEXT_MUTED}; margin-top:0;'>Learn a quant daily 📈</p>"
            "<hr>",
            unsafe_allow_html=True,
        )
