import streamlit as st

from core import theme, lesson_ui, progress
from core.day04_linear_transformations import LinearTransformations
from core.device import is_mobile

st.set_page_config(page_title="Linear Transformations — ThefacelessQuant", page_icon="assets/fq.ico", layout="wide")
theme.inject_base_css()
theme.render_sidebar_brand()

concept = LinearTransformations()
data = concept.content()
mobile = is_mobile()

# ---------------------------------------------------------------- top nav
nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("pages/3_Matrices.py", label="Back: Matrices")
with nav_right:
    st.page_link("pages/5_Linear_Systems.py", label="Next: Linear Systems", disabled=True)

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
        f"<p style='color:{theme.TEXT_MUTED};'>Apply a rebalancing rule to a "
        f"Tech/Gold book and watch the whole space stretch, not just one "
        f"vector. Tap a rule:</p>",
        unsafe_allow_html=True,
    )

    PRESETS = {
        "Bullish Tilt (Scale Tech Up)": (1.5, 0.5),
        "De-Risk (Scale Both Down)": (0.5, 0.5),
        "Equal Growth (Scale Both Up)": (1.5, 1.5),
        "Flip Gold (Short the Hedge)": (1.0, -1.0),
    }
    (a1_default, a2_default) = lesson_ui.preset_picker(
        PRESETS, key="day4_preset", default="Bullish Tilt (Scale Tech Up)"
    )
    label = st.session_state["day4_preset"]

    with st.expander("Fine-tune it yourself"):
        a1 = st.slider("TECH SCALE FACTOR", -2.0, 2.0, a1_default, 0.1, key=f"a1_{label}")
        a2 = st.slider("GOLD SCALE FACTOR", -2.0, 2.0, a2_default, 0.1, key=f"a2_{label}")

    result = concept.compute(a1=a1, a2=a2)

    m1, m2, m3 = st.columns(3)
    m1.metric("‖v‖ (before)", f"{result['norm_v']:.2f}")
    m2.metric("‖Av‖ (after)", f"{result['norm_Av']:.2f}")
    m3.metric("Determinant (Area Scale)", f"{result['det']:.2f}")

    fig = concept.visualize(a1=a1, a2=a2)
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
            "**MIT OpenCourseWare 18.06, Lecture 30: Linear Transformations and "
            "Their Matrices (Gilbert Strang).** Free video. This is the lecture "
            "built specifically for today's topic — Strang shows why every "
            "linear transformation is, underneath, just a matrix."
        )
        st.link_button("Watch: MIT OCW 18.06, Lecture 30", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/video-lectures/lecture-30-linear-transformations-and-their-matrices/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Learn by doing — blog & code</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Kalid Azad, *An Intuitive Guide to Linear Algebra* (BetterExplained).** "
            "The same article from Day 1 — this time, focus on the \"operations "
            "matrix\" section, where Azad explains a matrix as a machine that "
            "transforms every input the same consistent way."
        )
        st.link_button("Read the article", "https://betterexplained.com/articles/linear-algebra-guide/", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Open-source book — when you want more</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Immersive Linear Algebra (Ström, Åström & Akenine-Möller).** Free "
            "and interactive. Look for the chapter on linear transformations — "
            "you can drag a shape and watch it stretch and skew live as you "
            "change the matrix entries, which is exactly today's Practice tab, "
            "just with more freedom."
        )
        st.link_button("Open the book", "http://immersivemath.com/ila/index.html", use_container_width=True)

    with st.container(border=True):
        st.markdown("<h4>Python code — implement it yourself</h4>", unsafe_allow_html=True)
        st.markdown(
            "**Real Python, *Linear Algebra in Python*.** Every matrix-vector "
            "multiply you find in this tutorial — `A @ v` or `numpy.dot(A, v)` "
            "— is a linear transformation being applied. Try changing the "
            "matrix values yourself and see how the output vector shifts."
        )
        st.link_button("Read the tutorial", "https://realpython.com/python-linear-algebra/", use_container_width=True)

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>A matrix is a machine. Feed it a vector, it gives you back another "
        f"vector, always by the exact same rule. That rule is the transformation.</p></div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts")
