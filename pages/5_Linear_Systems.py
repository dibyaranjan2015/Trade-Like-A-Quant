"""
pages/5_Linear_Systems.py
Day 5 — Systems of Linear Equations. UI only; math in core/day05_linear_systems.py.
Matches the finalized Days 1-4 pattern exactly.
"""

import streamlit as st

from core import theme, lesson_ui, progress
from core.day05_linear_systems import LinearSystems
from core.device import is_mobile

st.set_page_config(page_title="Linear Systems — ThefacelessQuant", page_icon="assets/fq.ico", layout="wide")
theme.inject_base_css()
theme.render_sidebar_brand()

concept = LinearSystems()
data = concept.content()
mobile = is_mobile()

# ---------------------------------------------------------------- top nav
nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("pages/4_Linear_Transformations.py", label="Back: Linear Transformations")
with nav_right:
    st.page_link("Home.py", label="Next: Matrix Inverse", disabled=True)

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
        f"<p style='color:{theme.TEXT_MUTED};'>Pick a target return and solve "
        f"for the exact two-stock weighting that hits it, while staying "
        f"fully invested:</p>",
        unsafe_allow_html=True,
    )

    PRESETS = {
        "Conservative Target (5%)": (0.05, 0.12, 0.04),
        "Moderate Target (8%)": (0.08, 0.12, 0.04),
        "Aggressive Target (11%)": (0.11, 0.12, 0.04),
        "Beyond Reach (15%, needs leverage)": (0.15, 0.12, 0.04),
    }
    (target_default, ra_default, rb_default) = lesson_ui.preset_picker(
        PRESETS, key="day5_preset", default="Moderate Target (8%)"
    )
    label = st.session_state["day5_preset"]

    with st.expander("Fine-tune it yourself"):
        target_return = st.slider("TARGET RETURN", 0.0, 0.20, target_default, 0.01, key=f"tr_{label}")
        return_a = st.slider("STOCK A RETURN", 0.0, 0.20, ra_default, 0.01, key=f"ra_{label}")
        return_b = st.slider("STOCK B RETURN", 0.0, 0.20, rb_default, 0.01, key=f"rb_{label}")

    result = concept.compute(target_return=target_return, return_a=return_a, return_b=return_b)

    m1, m2, m3 = st.columns(3)
    m1.metric("Stock A Weight", f"{result['w_a']:.2f}")
    m2.metric("Stock B Weight", f"{result['w_b']:.2f}")
    m3.metric("Determinant of A", f"{result['det']:.3f}")

    if not result["solvable"]:
        st.warning("This system has no unique solution — the two constraint lines never cross at exactly one point.")
    elif result["w_a"] < 0 or result["w_a"] > 1 or result["w_b"] < 0 or result["w_b"] > 1:
        st.info("This solution requires leverage or shorting — one weight is outside the normal 0-100% range.")

    fig = concept.visualize(target_return=target_return, return_a=return_a, return_b=return_b)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ================================================================ TAB 3: CHALLENGE
with tab_challenge:
    st.markdown("<h3>Today's Challenge</h3>", unsafe_allow_html=True)
    lesson_ui.render_challenge(concept)

# ================================================================ TAB 4: GO DEEPER
with tab_deeper:
    st.markdown("<h3>Go Deeper</h3>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h4>Fundamentals — start here</h4>", unsafe_allow_html=True)
        st.markdown(
            "**MIT OpenCourseWare 18.06, Lecture 1: The Geometry of Linear "
            "Equations (Gilbert Strang).** Free video. This lecture's actual "
            "title is about today's exact topic — Strang shows both the "
            "\"row picture\" (lines crossing, like today's chart) and the "
            "\"column picture\" (vectors combining) of Ax = b."
        )
        st.link_button("Watch: MIT OCW 18.06, Lecture 1", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Learn by doing — blog & code</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Kalid Azad, *An Intuitive Guide to Linear Algebra* (BetterExplained).** "
            "The same article from Day 1 and Day 4 — this time, look for where "
            "Azad discusses \"solving\" the transformation, i.e. working backwards "
            "from a known output to find the input that produced it."
        )
        st.link_button("Read the article", "https://betterexplained.com/articles/linear-algebra-guide/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Open-source book — when you want more</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Immersive Linear Algebra (Ström, Åström & Akenine-Möller).** Free "
            "and interactive. Look for the chapter on systems of linear "
            "equations, which shows the row picture (lines/planes intersecting) "
            "you just built in the Practice tab, in an environment you can "
            "manipulate directly."
        )
        st.link_button("Open the book", "http://immersivemath.com/ila/index.html", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Python code — implement it yourself</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Real Python, *Linear Algebra in Python*.** Look for "
            "`numpy.linalg.solve()` — the exact function that solved today's "
            "system for you behind the scenes. Try feeding it your own A and b."
        )
        st.link_button("Read the tutorial", "https://realpython.com/python-linear-algebra/", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>Ax = b means \"find the one x that makes every constraint true at "
        f"once.\" Tomorrow you learn the actual tool — the matrix inverse — that "
        f"solves it.</p></div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts")
