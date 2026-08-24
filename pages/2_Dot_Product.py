"""
pages/2_Dot_Product.py
Day 2 — Dot Product & Geometry. UI only; all math lives in core/day02_dot_product.py.
"""

import streamlit as st

from core import theme
from core.day02_dot_product import DotProduct
from core.device import is_mobile

st.set_page_config(page_title="Dot Product — ThefacelessQuant", page_icon="◆", layout="wide")
theme.inject_base_css()
theme.render_sidebar_brand()

concept = DotProduct()
data = concept.content()
mobile = is_mobile()

# ---------------------------------------------------------------- top nav
nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("pages/1_Vectors.py", label="Back: Vectors")
with nav_right:
    st.page_link("pages/3_Matrices.py", label="Next: Matrices")

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

    mode = "2D" if mobile else st.radio("View", ["2D", "3D"], horizontal=True)

    st.markdown("**v** — your portfolio's sector tilt")
    v1 = st.slider("v, sector 1", 0.0, 1.0, 0.60, 0.05, key="v1")
    v2 = st.slider("v, sector 2", 0.0, 1.0, 0.30, 0.05, key="v2")
    v3 = st.slider("v, sector 3", 0.0, 1.0, 0.10, 0.05, key="v3") if mode == "3D" else None

    st.markdown("**u** — the benchmark's sector weights")
    u1 = st.slider("u, sector 1", 0.0, 1.0, 0.40, 0.05, key="u1")
    u2 = st.slider("u, sector 2", 0.0, 1.0, 0.50, 0.05, key="u2")
    u3 = st.slider("u, sector 3", 0.0, 1.0, 0.10, 0.05, key="u3") if mode == "3D" else None

    v = [v1, v2, v3] if mode == "3D" else [v1, v2]
    u = [u1, u2, u3] if mode == "3D" else [u1, u2]
    result = concept.compute(v=v, u=u)

    m1, m2, m3 = st.columns(3)
    m1.metric("v · u", f"{result['dot']:.2f}")
    m2.metric("cos θ", f"{result['cos_theta']:.2f}")
    m3.metric("θ (degrees)", f"{result['angle_deg']:.1f}°")

    fig = concept.visualize(v=v, u=u, mode=mode)
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
