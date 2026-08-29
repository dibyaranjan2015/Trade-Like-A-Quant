"""
pages/1_Vectors.py
Day 1 — Vectors & Vector Operations. UI only; math in core/day01_vectors.py.
Four-tab interactive format: Learn (paced), Practice (tap-first), Challenge
(quiz + streak), Go Deeper.
"""

import streamlit as st

from core import theme, lesson_ui, progress
from core.day01_vectors import Vectors
from core.device import is_mobile

st.set_page_config(page_title="Vectors — ThefacelessQuant", page_icon="assets/fq.ico", layout="wide")
theme.remove_streamlit_header()
theme.inject_base_css()
theme.render_sidebar_brand()

concept = Vectors()
data = concept.content()
mobile = is_mobile()

# ---------------------------------------------------------------- top nav

nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("Home.py", label="All concepts", width= "stretch")
with nav_right:
    st.page_link("Home.py", label="Next: Dot Product",disabled = True, width= "stretch")
    # st.page_link("pages/2_Dot_Product.py", label="Next: Dot Product")

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
        f"<p style='color:{theme.TEXT_MUTED};'>You're a junior analyst building your "
        f"first book. Tap a starting portfolio:</p>",
        unsafe_allow_html=True,
    )

    PRESETS = {
        "Growth Focus (Tech & EV)": ((0.45, 0.45, 0.10), (0.1, -0.05, -0.5)),
        "Safe Haven (Mostly Gold)": ((0.10, 0.10, 0.80), (0.05, -0.05, 0.00)),
        "Balanced (Equal Split)": ((0.33, 0.33, 0.34), (0.1, -0.05, -0.5)),
        "Max Exposure (Leveraged)": ((1.00, 1.00, 1.00), (0.1, -0.05, -0.5))
    }
    (v_default, u_default) = lesson_ui.preset_picker(
        PRESETS, key="day1_preset", default="Balanced (Equal Split)"
    )
    label = st.session_state["day1_preset"]

    with st.expander("Fine-tune it yourself"):
        v1 = st.slider("APPLE weight", -1.0, 1.0, v_default[0], 0.05, key=f"v1_{label}")
        v2 = st.slider("TESLA weight", -1.0, 1.0, v_default[1], 0.05, key=f"v2_{label}")
        v3 = st.slider("GOLD weight", -1.0, 1.0, v_default[2], 0.05, key=f"v3_{label}")
        u1 = st.slider("APPLE trade", -1.0, 1.0, u_default[0], 0.05, key=f"u1_{label}")
        u2 = st.slider("TESLA trade", -1.0, 1.0, u_default[1], 0.05, key=f"u2_{label}")
        u3 = st.slider("GOLD trade", -1.0, 1.0, u_default[2], 0.05, key=f"u3_{label}")
    v, u = [v1, v2, v3], [u1, u2, u3]

    result = concept.compute(v=v, u=u)

    m1, m2, m3 = st.columns(3)
    m1.metric("‖v‖  (exposure)", f"{result['norm_v']:.2f}")
    m2.metric("v + u", f"{result['v_plus_u']}")
    m3.metric("‖v+u‖  (after trade)", f"{result['norm_v_plus_u']:.2f}")

    fig = concept.visualize(v=v, u=u, mode="3D")
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
            "**Sheldon Axler, *Linear Algebra Done Right* (4th ed.).** The author recently "
            "made this legendary textbook 100% open access. Pair Chapter 1 (Vector Spaces) "
            "with **MIT OCW 18.06 Lecture 1**, which covers the same material in 45 minutes visually."
        )
        lb1, lb2 = st.columns(2)
        with lb1:
            st.link_button("Watch: MIT OCW 18.06", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", use_container_width=True)
        with lb2:
            st.link_button("Free PDF (Axler)", "https://linear.axler.net/LADR4e.pdf", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Applied to quant finance</h4>", unsafe_allow_html=True)
        st.markdown(
            "**3Blue1Brown, *Essence of Linear Algebra* — Episode 1: Vectors** "
            "(YouTube, free, 9 minutes). Watch before reading Strang's chapter — the "
            "geometric interpretation makes the portfolio-weight reading click faster."
        )
        st.link_button("Watch on YouTube", "https://www.youtube.com/watch?v=fNk_zzaMoSs", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Practitioner depth (Open Source)</h4>", unsafe_allow_html=True)
        st.markdown(
            "**QuantEcon: *Linear Algebra in Python*.** A world-class, open-source project "
            "sponsored by the Sloan Foundation. This lecture bridges the gap between pure math "
            "and programmatic finance, showing you exactly how to code vectors and matrices using NumPy."
        )
        st.link_button("Read the QuantEcon Lecture", "https://python.quantecon.org/linear_algebra.html", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>A portfolio's weights are a vector. Rebalancing is vector addition. "
        f"Risk size is the norm.</p></div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts" , width="stretch")
theme.footer()
