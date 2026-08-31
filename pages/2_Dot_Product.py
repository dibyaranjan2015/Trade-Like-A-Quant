"""
pages/2_Dot_Product.py
Day 2 — Dot Product & Geometry. UI only; math in core/day02_dot_product.py.
Matches the finalized pages/1_Vectors.py pattern: wide Learn column, single
visualization mode (no 2D/3D toggle), tap-first presets, open-access Go Deeper.
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

# ---------------------------------------------------------------- top nav
nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("pages/1_Vectors.py", label="Back: Vectors")
with nav_right:
    st.page_link("Home.py", label="Next: Matrices", disabled=True)
    # st.page_link("pages/3_Matrices.py", label="Next: Matrices")

# ---------------------------------------------------------------- header
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

# ================================================================ TAB 1: LEARN
with tab_learn:
    render_col = st.columns([1, 8, 1])[1] if not mobile else st.container()
    with render_col:
        lesson_ui.render_learn_flow(concept, data)

# ================================================================ TAB 2: PRACTICE
with tab_practice:
    st.markdown(
        f"<p style='color:{theme.TEXT_MUTED};'>Your PM wants to know how far your "
        f"book has drifted from the benchmark. Tap a positioning:</p>",
        unsafe_allow_html=True,
    )

    PRESETS = {
        "Closet Indexer (Hugging the Benchmark)": ((0.42, 0.48), (0.40, 0.50)),
        "Modest Tilt (Slightly Overweight Tech)": ((0.60, 0.30), (0.40, 0.50)),
        "Concentrated Bet (High Conviction Tech)": ((0.85, 0.10), (0.40, 0.50)),
        "Contrarian (Betting Against Tech)": ((0.20, 0.70), (0.40, 0.50)),
    }
    (v_default, u_default) = lesson_ui.preset_picker(
        PRESETS, key="day2_preset", default="Modest Tilt (Slightly Overweight Tech)"
    )
    label = st.session_state["day2_preset"]

    with st.expander("Fine-tune it yourself"):
        v1 = st.slider("YOUR TECH WEIGHT", 0.0, 1.0, v_default[0], 0.05, key=f"v1_{label}")
        v2 = st.slider("YOUR FINANCIALS WEIGHT", 0.0, 1.0, v_default[1], 0.05, key=f"v2_{label}")
        u1 = st.slider("BENCHMARK TECH WEIGHT", 0.0, 1.0, u_default[0], 0.05, key=f"u1_{label}")
        u2 = st.slider("BENCHMARK FINANCIALS WEIGHT", 0.0, 1.0, u_default[1], 0.05, key=f"u2_{label}")
    v, u = [v1, v2], [u1, u2]

    result = concept.compute(v=v, u=u)

    m1, m2, m3 = st.columns(3)
    m1.metric("v · u", f"{result['dot']:.3f}")
    m2.metric("cos θ", f"{result['cos_theta']:.3f}")
    m3.metric("θ (degrees apart)", f"{result['angle_deg']:.1f}°")

    fig = concept.visualize(v=v, u=u, mode="2D")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ================================================================ TAB 3: CHALLENGE
with tab_challenge:
    st.markdown("<h3>Today's Challenge</h3>", unsafe_allow_html=True)
    lesson_ui.render_challenge(concept)

# ================================================================ TAB 4: GO DEEPER
with tab_deeper:
    st.markdown("<h3>Go Deeper</h3>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h4>Foundational — start here</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Sheldon Axler, *Linear Algebra Done Right* (4th ed.), Chapter 6: "
            "Inner Product Spaces.** This is the chapter where Axler formally "
            "introduces the dot product (as a special case of an inner product) "
            "and proves the Cauchy-Schwarz inequality that makes cos θ always "
            "land between -1 and 1. Pair it with **MIT OCW 18.06 Lecture 1**, "
            "which covers the same ground visually with coordinates and pictures."
        )
        lb1, lb2 = st.columns(2)
        with lb1:
            st.link_button("Watch: MIT OCW 18.06", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", use_container_width=True)
        with lb2:
            st.link_button("Free PDF (Axler)", "https://linear.axler.net/LADR4e.pdf", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Applied to quant finance</h4>", unsafe_allow_html=True)
        st.markdown(
            "**3Blue1Brown, *Essence of Linear Algebra* — Episode 9: Dot Products "
            "and Duality** (YouTube, free). Explains why the algebraic and "
            "geometric forms of the dot product are the same number — the "
            "projection interpretation the formula alone doesn't make obvious."
        )
        st.link_button("Watch on YouTube", "https://www.youtube.com/watch?v=LyGKycYT2v0", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Practitioner depth</h4>", unsafe_allow_html=True)
        st.markdown(
            "**QuantEcon: *Orthogonal Projections and Their Applications*.** "
            "A free, open-source lecture from the same Sloan Foundation-sponsored "
            "project as Day 1's resource. It opens with exactly today's formula — "
            "the law of cosines and the definition of orthogonality — then shows "
            "you how real quant systems use projection to build least-squares "
            "predictions in Python."
        )
        st.link_button("Read the QuantEcon Lecture", "https://python-advanced.quantecon.org/orth_proj.html", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>Multiply matching components and add — that's the dot product. Turn "
        f"it into an angle and you get a straight answer to how aligned two "
        f"things are.</p></div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts")
