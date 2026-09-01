"""
pages/3_Matrices.py
Day 3 — Matrices & Matrix Operations. UI only; math in core/day03_matrices.py.
Matches the finalized pages/1_Vectors.py and pages/2_Dot_Product.py pattern.
"""

import streamlit as st

from core import theme, lesson_ui, progress
from core.day03_matrices import Matrices, TICKERS
from core.device import is_mobile

st.set_page_config(page_title="Matrices — ThefacelessQuant", page_icon="assets/fq.ico", layout="wide")
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
    st.page_link("Home.py", label="Next: Linear Transformations")
    # st.page_link("pages/4_Linear_Transformations.py", label="Next: Linear Transformations")

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
        f"<p style='color:{theme.TEXT_MUTED};'>Build a portfolio across "
        f"{', '.join(TICKERS)} and watch four days of returns collapse into "
        f"one portfolio return per day:</p>",
        unsafe_allow_html=True,
    )

    PRESETS = {
        "Equal Weight (No Favorites)": (0.34, 0.33, 0.33),
        "Concentrated Apple (Overweight Tech)": (0.70, 0.15, 0.15),
        "Concentrated Amazon (Overweight Ecommerce)": (0.10, 0.20, 0.70),
        "Market-Cap Style (Balanced)": (0.50, 0.30, 0.20),
    }
    w_default = lesson_ui.preset_picker(PRESETS, key="day3_preset", default="Market-Cap Style (Balanced)")
    label = st.session_state["day3_preset"]

    with st.expander("Fine-tune it yourself"):
        w1 = st.slider(f"{TICKERS[0].upper()} WEIGHT", 0.0, 1.0, w_default[0], 0.05, key=f"w1_{label}")
        w2 = st.slider(f"{TICKERS[1].upper()} WEIGHT", 0.0, 1.0, w_default[1], 0.05, key=f"w2_{label}")
        w3 = st.slider(f"{TICKERS[2].upper()} WEIGHT", 0.0, 1.0, w_default[2], 0.05, key=f"w3_{label}")

    result = concept.compute(weights=[w1, w2, w3])

    m1, m2, m3 = st.columns(3)
    m1.metric("Σ weights", f"{result['weight_sum']:.2f}")
    m2.metric("Mean daily return", f"{result['mean_return']*100:.2f}%")
    m3.metric("Volatility (std)", f"± {result['volatility']*100:.2f}%")

    fig = concept.visualize(weights=[w1, w2, w3])
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
            "**MIT OpenCourseWare 18.06, Lectures 1–3 (Gilbert Strang).** Free "
            "video. Strang builds matrices up visually — row picture, column "
            "picture, then matrix multiplication — before any of the formal "
            "notation. Watch these three before reading anything else."
        )
        st.link_button("Watch: MIT OCW 18.06, Lectures 1–3", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Learn by doing — blog & code</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Kalid Azad, *A Programmer's Intuition for Matrix Multiplication* "
            "(BetterExplained).** Written for people who think in code, not proofs. "
            "Explains matrix multiplication as \"data flowing through a pipeline\" "
            "instead of a grid of arithmetic rules to memorise."
        )
        st.link_button("Read the article", "https://betterexplained.com/articles/matrix-multiplication/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Open-source book — when you want more</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Immersive Linear Algebra (Ström, Åström & Akenine-Möller).** Free "
            "and interactive — the matrix chapter lets you drag a matrix's entries "
            "and watch a shape stretch, rotate, and skew in real time, which is a "
            "far more intuitive way to internalise 'matrix times vector' than any "
            "formula on its own."
        )
        st.link_button("Open the book", "http://immersivemath.com/ila/index.html", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Python code — implement it yourself</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Real Python, *Linear Algebra in Python*.** Look for where they build "
            "a matrix with `numpy.array()` and multiply it by a vector — the exact "
            "R times w operation from today's example, in real, runnable code."
        )
        st.link_button("Read the tutorial", "https://realpython.com/python-linear-algebra/", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>A matrix times a vector collapses a whole table into one new vector, "
        f"in a single operation. That's R times w — and everything from here builds on it.</p></div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts")
