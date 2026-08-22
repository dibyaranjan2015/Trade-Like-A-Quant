"""
pages/1_📐_Vectors.py
Day 1/40 — Vector Playground (UI only — all math is in core/day01_vectors.py)
"""

import streamlit as st

from core import theme
from core.day01_vectors import Vectors

st.set_page_config(page_title="Day 1 — Vectors", page_icon="📐", layout="centered")
theme.inject_base_css()
theme.render_sidebar_brand()

concept = Vectors()

# Top nav row — works even for mobile users who never touch the sidebar
c1, c2 = st.columns(2)
with c1:
    st.page_link("Home.py", label="← Home", icon="🏠")
with c2:
    st.button("Day 2 →", icon="🎯", disabled=True)
    # ^ flip disabled=False once Day 2's page file exists

st.markdown(
    f"<h1 style='color:{theme.LINEAR_ALGEBRA};'>Day {concept.day}/40 — {concept.name}</h1>"
    f"<p style='color:{theme.TEXT_MUTED};'>{concept.pillar} · Week {concept.week}</p>",
    unsafe_allow_html=True,
)

with st.expander("📘 Why it matters (tap to read)", expanded=True):
    st.write(concept.explain())

mode = st.radio("View", ["2D", "3D"], horizontal=True)

st.markdown("**Vector v** — e.g. current portfolio weights")
v1 = st.slider("v.x", -1.0, 1.0, 0.40, 0.05)
v2 = st.slider("v.y", -1.0, 1.0, 0.35, 0.05)
v3 = st.slider("v.z", -1.0, 1.0, 0.25, 0.05) if mode == "3D" else 0.0

st.markdown("**Vector u** — e.g. a rebalancing trade")
u1 = st.slider("u.x", -1.0, 1.0, 0.10, 0.05)
u2 = st.slider("u.y", -1.0, 1.0, -0.05, 0.05)
u3 = st.slider("u.z", -1.0, 1.0, -0.05, 0.05) if mode == "3D" else 0.0

v = [v1, v2, v3] if mode == "3D" else [v1, v2]
u = [u1, u2, u3] if mode == "3D" else [u1, u2]

result = concept.compute(v=v, u=u)

# Stacked metrics — st.columns(3) squeezes badly on phones, so go single column on mobile
m1, m2, m3 = st.columns(3)
m1.metric("‖v‖", f"{result['norm_v']:.2f}")
m2.metric("v · u", f"{result['dot_v_u']:.2f}")
m3.metric("‖v+u‖", f"{sum(x**2 for x in result['v_plus_u'])**0.5:.2f}")

fig = concept.visualize(v=v, u=u, mode=mode)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.page_link("Home.py", label="← Back to all days", icon="🏠")
st.caption("Day 1/40 · #ThefacelessQuant")
