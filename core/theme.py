"""
core/theme.py
Shared visual identity for every page: color system, typography, Plotly
template, and the CSS that gives the site an actual design instead of
default-Streamlit gray boxes.
"""

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

DARK_BG = "#0b0f19"          # Deep midnight blue/black background
PANEL_BG = "#131a2a"         # Slightly lighter for panels
PANEL_BORDER = "#1f2937"     # Subtle border

# High-contrast neon accents for mathematical pillars
LINEAR_ALGEBRA = "#00e5ff"   # Cyan
CALCULUS = "#a855f7"         # Purple
PROBABILITY = "#22c55e"      # Green
QUANT_FINANCE = "#f97316"    # Orange

# Typography colors for dark backgrounds
TEXT_PRIMARY = "#f3f4f6"     # Off-white for main text
TEXT_MUTED = "#9ca3af"       # Soft gray for subtitles/axes
GRID_LINE = "#1f2937"        # Dark gridlines to not overpower charts

HEADING_FONT = "'Space Grotesk', 'Inter', sans-serif"
BODY_FONT = "'Inter', -apple-system, sans-serif"

PILLAR_COLORS = {
    "Linear Algebra": LINEAR_ALGEBRA,
    "Calculus": CALCULUS,
    "Probability & Stats": PROBABILITY,
    "Quant Finance": QUANT_FINANCE,
}


def build_plotly_template() -> go.layout.Template:
    """Builds a custom Plotly template that matches the Streamlit dark theme."""
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=BODY_FONT, color=TEXT_PRIMARY, size=13),
        xaxis=dict(
            gridcolor=GRID_LINE, 
            zerolinecolor=GRID_LINE, 
            color=TEXT_MUTED,
            showgrid=True,
            showline=False
        ),
        yaxis=dict(
            gridcolor=GRID_LINE, 
            zerolinecolor=GRID_LINE, 
            color=TEXT_MUTED,
            showgrid=True,
            showline=False
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_PRIMARY)
        ),
        margin=dict(l=40, r=20, t=40, b=40),
        colorway=[LINEAR_ALGEBRA, QUANT_FINANCE, PROBABILITY, CALCULUS] # Default line colors
    )
    return template


pio.templates["quant_dark"] = build_plotly_template()


def inject_base_css():
    """Call once per page, right after st.set_page_config()."""
    
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        /* Force App Background */
        .stApp {{
            background-color: {DARK_BG} !important;
        }}

        /* Base Text */
        html, body, [class*="css"], [data-testid="stMarkdownContainer"] p {{
            font-family: {BODY_FONT};
            color: {TEXT_PRIMARY} !important;
        }}

        /* Aggressively target all Headers */
        h1, h2, h3, h4, h5, h6, 
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {{
            font-family: {HEADING_FONT} !important;
            letter-spacing: -0.01em;
            color: #ffffff !important;
        }}

        /* FIX: LaTeX / Mathematical Formulas */
        .katex, .katex-html, .katex-display {{
            color: {LINEAR_ALGEBRA} !important; /* Gives formulas a nice neon cyan glow to stand out */
        }}
        .katex .frac-line {{
            border-bottom-color: {LINEAR_ALGEBRA} !important; /* Ensures fraction division lines match */
        }}

        /* Hero Text Specifics */
        .hero-title {{
            font-family: {HEADING_FONT};
            font-weight: 700;
            font-size: 2.4rem;
            background: linear-gradient(90deg, {LINEAR_ALGEBRA}, {CALCULUS});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
            color: transparent !important; /* Fixes Webkit gradient override */
        }}
        .hero-subtitle {{
            color: {TEXT_MUTED} !important;
            font-size: 1.05rem;
            margin-top: 6px;
            line-height: 1.5;
        }}

        /* Concept Panels */
        .concept-panel {{
            background: {PANEL_BG};
            border: 1px solid {PANEL_BORDER};
            border-radius: 14px;
            padding: 20px 22px;
            margin-bottom: 14px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        }}
        .concept-panel h4 {{
            margin-top: 0;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {LINEAR_ALGEBRA} !important; 
            font-weight: 600;
        }}
        .concept-panel p {{
            color: {TEXT_PRIMARY} !important;
            line-height: 1.65;
            font-size: 1rem;
        }}

        /* Styling Streamlit Page Links */
        a[data-testid="stPageLink-NavLink"] {{
            background-color: {PANEL_BG} !important;
            border: 1px solid {PANEL_BORDER} !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            margin-bottom: 10px !important;
            transition: all 0.2s ease;
        }}
        a[data-testid="stPageLink-NavLink"]:hover {{
            border-color: {LINEAR_ALGEBRA} !important;
            box-shadow: 0 0 8px {LINEAR_ALGEBRA}33;
            transform: translateY(-1px);
        }}
        a[data-testid="stPageLink-NavLink"] p {{
            font-family: {HEADING_FONT} !important;
            font-weight: 500 !important;
            color: {TEXT_PRIMARY} !important;
        }}

        /* Metric Cards */
        [data-testid="stMetric"] {{
            background: {PANEL_BG};
            border: 1px solid {PANEL_BORDER};
            border-radius: 12px;
            padding: 14px 16px;
        }}
        [data-testid="stMetricLabel"] p {{
            color: {TEXT_MUTED} !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {TEXT_PRIMARY} !important;
            font-family: {HEADING_FONT};
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
             f"font-size:1.4rem; color:#00E5FF; margin-bottom: 0px;'>"
             f"TheFacelessQuant</div>"
             f"<p style='color:{TEXT_MUTED}; font-size:0.85rem; line-height: 1.4;'>"
                "An Open Learning platform for aspiring Quants - Master the Math, build Models and turn Ideas into Alpha</p><hr>",
            #  "A daily study of quantitative finance & algorithmic trading</p><hr>",
             unsafe_allow_html=True,
        )


def concept_panel(heading: str, body_html: str):
    st.markdown(
        f"<div class='concept-panel'><h4>{heading}</h4>{body_html}</div>",
        unsafe_allow_html=True,
    )


def panel_open(heading: str):
    """Opens a concept-panel div without closing it — use when the body needs
    a mix of Streamlit elements (st.latex, st.markdown) rather than one HTML
    string. Always pair with panel_close()."""
    st.markdown(f"<div class='concept-panel'><h4>{heading}</h4>", unsafe_allow_html=True)


def panel_close():
    st.markdown("</div>", unsafe_allow_html=True)


def Home_page_setup():
    st.markdown("""
    <style>
        /* Main Typography */
        h1, h2, h3, p { font-family: 'Inter', sans-serif; }
        .hero-title { font-size: 1.5rem; font-weight: 700; color: #ffffff; margin-bottom: 0.2rem; }
        .hero-subtitle { font-size: 1rem; color: #a0aec0; margin-bottom: 2rem; max-width: 800px;}
        .stats-container { display: flex; gap: 20px; margin-bottom: 1.5rem; flex-wrap: wrap; }
        .stat-card {
            flex: 1; min-width: 200px;
            background: linear-gradient(145deg, #1a1e27, #13151a);
            border-radius: 12px; padding: 5px;
            display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .stat-card.streak { border: 1px solid #b45309; }
        .stat-card.completed { border: 1px solid #1d4ed8; }
        .stat-card.progress { border: 1px solid #047857; }
        .stat-text h4 { margin: 0; font-size: 0.85rem; color: #9ca3af; font-weight: 500; }
        .stat-text h2 { margin: 0; font-size: 2.2rem; font-weight: 700; }
        .streak h2 { color: #f59e0b; }
        .completed h2 { color: #3b82f6; }
        .progress h2 { color: #10b981; }
        .week-banner {
            font-size: 0.8rem; font-weight: 700; letter-spacing: 0.05em; color: white;
            padding: 6px 20px; border-radius: 0 15px 15px 0;
            display: inline-block; margin: 1.5rem 0 1rem -1rem; 
        }
        .banner-blue { background: linear-gradient(90deg, #1e3a8a, #0ea5e9); clip-path: polygon(0 0, 95% 0, 100% 100%, 0% 100%);}
        .banner-purple { background: linear-gradient(90deg, #4c1d95, #a855f7); clip-path: polygon(0 0, 95% 0, 100% 100%, 0% 100%);}
        .day-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 15px; }
        .day-card {
            background: #111827; border-radius: 10px; padding: 15px 20px;
            display: flex; justify-content: space-between; align-items: center;
            text-decoration: none !important; color: white !important;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .day-card:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.4); }
        .day-card p { margin: 0; font-size: 0.95rem; font-weight: 500; }
        .border-blue { border: 1px solid #0ea5e9; }
        .border-gold { border: 1px solid #f59e0b; }
        .border-green { border: 1px solid #10b981; }
        .border-purple { border: 1px solid #a855f7; }
        .check-mark { color: #f59e0b; margin-left: 8px; font-weight: bold;}
    </style>
        """, unsafe_allow_html=True)
