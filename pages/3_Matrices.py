"""
pages/3_Matrices.py
Day 3 — Matrices & Matrix Operations. UI only; math lives in core/day03_matrices.py.
"""

import streamlit as st

from core import theme
from core.day03_matrices import Matrices, TICKERS
from core.device import is_mobile

st.set_page_config(page_title="Matrices — ThefacelessQuant", page_icon="◆", layout="wide")
theme.inject_base_css()
theme.render_sidebar_brand()

concept = Matrices()
data = concept.content()
mobile = is_mobile()

# ---------------------------------------------------------------- top nav
nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("pages/2_Dot_Product.py", label="Back: Dot Product")
with nav_right:
    st.page_link("Home.py", label="Next: Linear Transformations", disabled=True)

# ---------------------------------------------------------------- header
st.markdown(
    f"<p style='color:{theme.LINEAR_ALGEBRA}; font-weight:600; letter-spacing:0.08em; "
    f"text-transform:uppercase; font-size:0.8rem; margin-bottom:2px;'>"
    f"Day {concept.day} · {concept.pillar}</p>"
    f"<h1 style='margin-top:0;'>{concept.name}</h1>"
    f"<p class='hero-subtitle'>{data['tagline']}</p>",
    unsafe_allow_html=True,
)
st.write("")


def render_explanation():
    theme.concept_panel("Definition", f"<p>{data['definition']}</p>")
    for label, latex in data["formulas"]:
        st.markdown(f"<p style='color:{theme.TEXT_MUTED}; margin-bottom:2px;'>{label}</p>",
                    unsafe_allow_html=True)
        st.latex(latex)
    theme.concept_panel("Worked example", f"<p>{data['example']}</p>")
    theme.concept_panel("Where this shows up", f"<p>{data['application']}</p>")


def render_playground():
    st.markdown("<h3>Try it yourself</h3>", unsafe_allow_html=True)
    st.markdown(f"**w** — portfolio weights across {', '.join(TICKERS)}")

    w1 = st.slider(f"{TICKERS[0]} weight", 0.0, 1.0, 0.50, 0.05, key="w1")
    w2 = st.slider(f"{TICKERS[1]} weight", 0.0, 1.0, 0.30, 0.05, key="w2")
    w3 = st.slider(f"{TICKERS[2]} weight", 0.0, 1.0, 0.20, 0.05, key="w3")

    result = concept.compute(weights=[w1, w2, w3])

    m1, m2, m3 = st.columns(3)
    m1.metric("Σ weights", f"{result['weight_sum']:.2f}")
    m2.metric("Mean daily return", f"{result['mean_return']:.4f}")
    m3.metric("Volatility (std)", f"{result['volatility']:.4f}")

    fig = concept.visualize(weights=[w1, w2, w3])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ---------------------------------------------------------------- layout
if mobile:
    render_explanation()
    st.divider()
    render_playground()
else:
    col_read, col_play = st.columns([0.55, 0.45], gap="large")
    with col_read:
        render_explanation()
    with col_play:
        with st.container(border=True):
            render_playground()

st.divider()
st.page_link("Home.py", label="Back to all concepts")
