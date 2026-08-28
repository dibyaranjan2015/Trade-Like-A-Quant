"""
pages/2_Dot_Product.py
Day 2 — Dot Product & Geometry. Four-tab interactive format.
"""

import streamlit as st

from core import theme, lesson_ui, progress
from core.day02_dot_product import DotProduct
from core.device import is_mobile

st.set_page_config(page_title="Dot Product — ThefacelessQuant", page_icon="assets/fq.ico", layout="wide")
theme.inject_base_css()
theme.render_sidebar_brand()

concept = DotProduct()
data = concept.content()
mobile = is_mobile()

nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("pages/1_Vectors.py", label="Back: Vectors")
with nav_right:
    st.page_link("pages/3_Matrices.py", label="Next: Matrices")

completed = progress.get_completed_days()
badge = " ✓" if concept.day in completed else ""
st.markdown(
    f"<p style='color:{theme.LINEAR_ALGEBRA}; font-weight:600; letter-spacing:0.08em; "
    f"text-transform:uppercase; font-size:0.8rem; margin-bottom:2px;'>"
    f"Day {concept.day} · {concept.pillar} · Phase 1</p>"
    f"<h1 style='margin-top:0;'>{concept.name}{badge}</h1>"
    f"<p class='hero-subtitle'>{data['tagline']}</p>",
    unsafe_allow_html=True,
)
st.write("")

tab_learn, tab_practice, tab_challenge, tab_deeper = st.tabs(
    ["Learn", "Practice", "Challenge", "Go Deeper"]
)

with tab_learn:
    render_col = st.columns([1, 2, 1])[1] if not mobile else st.container()
    with render_col:
        lesson_ui.render_learn_flow(concept, data)

with tab_practice:
    st.markdown(
        f"<p style='color:{theme.TEXT_MUTED};'>Your PM wants to know how far your book "
        f"has drifted from the benchmark. Tap a positioning:</p>",
        unsafe_allow_html=True,
    )

    PRESETS = {
        "Closet Indexer": ((0.42, 0.48), (0.40, 0.50)),
        "Modest Tilt": ((0.60, 0.30), (0.40, 0.50)),
        "Concentrated Bet": ((0.85, 0.10), (0.40, 0.50)),
        "Contrarian": ((0.20, 0.70), (0.40, 0.50)),
    }
    (v_default, u_default) = lesson_ui.preset_picker(
        PRESETS, key="day2_preset", default="Modest Tilt"
    )
    label = st.session_state["day2_preset"]

    with st.expander("Fine-tune it yourself"):
        v1 = st.slider("Your tech weight", 0.0, 1.0, v_default[0], 0.05, key=f"v1_{label}")
        v2 = st.slider("Your financials weight", 0.0, 1.0, v_default[1], 0.05, key=f"v2_{label}")
        u1 = st.slider("Benchmark tech", 0.0, 1.0, u_default[0], 0.05, key=f"u1_{label}")
        u2 = st.slider("Benchmark financials", 0.0, 1.0, u_default[1], 0.05, key=f"u2_{label}")
    v, u = [v1, v2], [u1, u2]

    result = concept.compute(v=v, u=u)

    m1, m2, m3 = st.columns(3)
    m1.metric("v · u", f"{result['dot']:.3f}")
    m2.metric("cos θ", f"{result['cos_theta']:.3f}")
    m3.metric("θ (degrees apart)", f"{result['angle_deg']:.1f}°")

    fig = concept.visualize(v=v, u=u, mode="2D")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with tab_challenge:
    st.markdown("<h3>Today's Challenge</h3>", unsafe_allow_html=True)
    lesson_ui.render_challenge(concept)

with tab_deeper:
    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Foundational — start here</h4>"
        f"<p><strong>Gilbert Strang, <em>Introduction to Linear Algebra</em> (6th ed.), "
        f"Section 1.2: Lengths and Dot Products.</strong> This is literally the section "
        f"right after Day 1 in Strang. He introduces the dot product as the algebraic "
        f"tool that measures the angle between vectors, and proves that orthogonal "
        f"vectors have a dot product of zero — the reason uncorrelated assets have zero "
        f"covariance later. Work through his proof that cos θ = (v · u)/(‖v‖‖u‖) by "
        f"hand once.</p></div>",
        unsafe_allow_html=True,
    )
    lb1, lb2 = st.columns(2)
    with lb1:
        st.link_button("Watch: MIT OCW 18.06", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", use_container_width=True)
    with lb2:
        st.link_button("Book site (Strang)", "https://math.mit.edu/~gs/linearalgebra/", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Applied to quant finance</h4>"
        f"<p><strong>3Blue1Brown, <em>Essence of Linear Algebra</em> — Episode 9: "
        f"Dot Products and Duality</strong> (YouTube, free). Explains why the algebraic "
        f"and geometric forms are the same number — the projection interpretation the "
        f"formula alone doesn't make obvious.</p></div>",
        unsafe_allow_html=True,
    )
    st.link_button("Watch on YouTube", "https://www.youtube.com/watch?v=LyGKycYT2v0", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Practitioner depth</h4>"
        f"<p><strong>Rishi K. Narang, <em>Inside the Black Box</em> (2nd ed.), "
        f"Chapter 3: Alpha Models.</strong> Cosine similarity between predicted and "
        f"realised returns, in a real fund context.</p></div>",
        unsafe_allow_html=True,
    )
    st.link_button("View the book — Wiley Online", "https://onlinelibrary.wiley.com/doi/book/10.1002/9781118662717", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>Multiply matching components and add — that's the dot product. Turn it "
        f"into an angle and you get a straight answer to how aligned two things are.</p></div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts")
