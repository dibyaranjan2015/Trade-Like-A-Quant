"""
pages/3_Matrices.py
Day 3 — Matrices & Matrix Operations. Four-tab interactive format.
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

nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("pages/2_Dot_Product.py", label="Back: Dot Product")
with nav_right:
    st.page_link("Home.py", label="Next: Linear Transformations", disabled=True)

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
        f"<p style='color:{theme.TEXT_MUTED};'>Pick how you'd split capital across "
        f"{', '.join(TICKERS)} and watch four days of returns collapse into one "
        f"portfolio return per day:</p>",
        unsafe_allow_html=True,
    )

    PRESETS = {
        "Equal Weight": (0.34, 0.33, 0.33),
        "Concentrated A": (0.70, 0.20, 0.10),
        "Concentrated C": (0.10, 0.20, 0.70),
        "Market-Cap Style": (0.50, 0.30, 0.20),
    }
    w_default = lesson_ui.preset_picker(PRESETS, key="day3_preset", default="Market-Cap Style")
    label = st.session_state["day3_preset"]

    with st.expander("Fine-tune it yourself"):
        w1 = st.slider(f"{TICKERS[0]} weight", 0.0, 1.0, w_default[0], 0.05, key=f"w1_{label}")
        w2 = st.slider(f"{TICKERS[1]} weight", 0.0, 1.0, w_default[1], 0.05, key=f"w2_{label}")
        w3 = st.slider(f"{TICKERS[2]} weight", 0.0, 1.0, w_default[2], 0.05, key=f"w3_{label}")

    result = concept.compute(weights=[w1, w2, w3])

    m1, m2, m3 = st.columns(3)
    m1.metric("Σ weights", f"{result['weight_sum']:.2f}")
    m2.metric("Mean daily return", f"{result['mean_return']:.4f}")
    m3.metric("Volatility (std)", f"{result['volatility']:.4f}")

    fig = concept.visualize(weights=[w1, w2, w3])
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with tab_challenge:
    st.markdown("<h3>Today's Challenge</h3>", unsafe_allow_html=True)
    lesson_ui.render_challenge(concept)

with tab_deeper:
    with st.container(border=True):
        st.markdown("<h4>Foundational — start here</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Gilbert Strang, *Introduction to Linear Algebra* (6th ed.), Chapter 1.** "
            "Paired with MIT OCW 18.06 Lectures 1–3 — the row, column, and matrix "
            "pictures of a linear system."
        )
        lb1, lb2 = st.columns(2)
        with lb1:
            st.link_button("Watch: MIT OCW 18.06 Lectures", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", use_container_width=True)
        with lb2:
            st.link_button("Book site (Strang)", "https://math.mit.edu/~gs/linearalgebra/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Applied to quant finance</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Dan Stefanica, *A Linear Algebra Primer for Financial Engineering*.** "
            "Numerical, pseudocode-driven, with quant interview-style questions."
        )
        st.link_button("View the book — fepress.org", "https://www.fepress.org/nla-primer/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Practitioner depth</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Antonio De la Rosa, \"Numerical Linear Algebra in Quantitative "
            "Finance\"** (Springer, 2025). How matrix factorisations power risk "
            "models, portfolio optimisation, and calibration in production."
        )
        st.link_button("Read the chapter — Springer", "https://link.springer.com/chapter/10.1007/979-8-8688-1793-9_8", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>A matrix times a vector collapses a whole table into one new vector, "
        f"in a single operation. That's R times w.</p></div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts")
