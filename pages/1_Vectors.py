"""
pages/1_Vectors.py
Day 1 — Vectors & Vector Operations. UI only; math in core/day01_vectors.py.
Rebuilt as a full study tool — three tabs: Learn, Practice, Go Deeper.
"""

import streamlit as st

from core import theme
from core.day01_vectors import Vectors
from core.device import is_mobile

st.set_page_config(page_title="Vectors — ThefacelessQuant", page_icon="◆", layout="wide")
theme.inject_base_css()
theme.render_sidebar_brand()

concept = Vectors()
data = concept.content()
mobile = is_mobile()

# ---------------------------------------------------------------- top nav
nav_left, nav_right = st.columns(2)
with nav_left:
    st.page_link("Home.py", label="All concepts")
with nav_right:
    st.page_link("pages/2_Dot_Product.py", label="Next: Dot Product")

# ---------------------------------------------------------------- header
st.markdown(
    f"<p style='color:{theme.LINEAR_ALGEBRA}; font-weight:600; letter-spacing:0.08em; "
    f"text-transform:uppercase; font-size:0.8rem; margin-bottom:2px;'>"
    f"Day {concept.day} · {concept.pillar} · Phase 1</p>"
    f"<h1 style='margin-top:0;'>{concept.name}</h1>"
    f"<p class='hero-subtitle'>{data['tagline']}</p>",
    unsafe_allow_html=True,
)
st.write("")

tab_learn, tab_practice, tab_deeper = st.tabs(["Learn", "Practice", "Go Deeper"])


# ================================================================ TAB 1: LEARN
with tab_learn:
    if mobile:
        # Single column on mobile
        theme.concept_panel("Definition", f"<p>{data['definition']}</p>")
        st.markdown(f"<h3 style='color:{theme.TEXT_MUTED}; font-size:0.9rem; "
                    f"text-transform:uppercase; letter-spacing:0.06em;'>The Formulas</h3>",
                    unsafe_allow_html=True)
        for label, latex_str in data["formulas"]:
            st.markdown(f"<p style='color:{theme.TEXT_MUTED}; margin-bottom:2px; "
                        f"font-size:0.9rem;'>{label}</p>", unsafe_allow_html=True)
            st.latex(latex_str)
        theme.concept_panel("Worked Example", f"<p>{data['example']}</p>")
        theme.concept_panel("Where This Shows Up", f"<p>{data['application']}</p>")
    else:
        col_left, col_right = st.columns([0.55, 0.45], gap="large")
        with col_left:
            theme.concept_panel("Definition", f"<p>{data['definition']}</p>")
            theme.concept_panel("Worked Example", f"<p>{data['example']}</p>")
            theme.concept_panel("Where This Shows Up", f"<p>{data['application']}</p>")
        with col_right:
            st.markdown(f"<h3 style='color:{theme.TEXT_MUTED}; font-size:0.9rem; "
                        f"text-transform:uppercase; letter-spacing:0.06em; margin-bottom:12px;'>"
                        f"The Formulas</h3>", unsafe_allow_html=True)
            for label, latex_str in data["formulas"]:
                st.markdown(f"<p style='color:{theme.TEXT_MUTED}; margin-bottom:2px; "
                            f"font-size:0.9rem;'>{label}</p>", unsafe_allow_html=True)
                st.latex(latex_str)
                st.write("")

            # Key insight callout
            st.markdown(
                f"<div class='concept-panel' style='border-color:{theme.LINEAR_ALGEBRA}44;'>"
                f"<h4 style='color:{theme.LINEAR_ALGEBRA};'>Key Insight</h4>"
                f"<p>The norm ‖v‖ is a single number that tells you the total size of a "
                f"vector — how concentrated a portfolio is, or how large a factor exposure "
                f"is. Every risk metric you will learn later reduces something complex to a "
                f"single number in exactly the same way.</p></div>",
                unsafe_allow_html=True,
            )


# ================================================================ TAB 2: PRACTICE
with tab_practice:
    st.markdown("<h3>Interactive Playground</h3>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{theme.TEXT_MUTED};'>Adjust the sliders to build any portfolio "
        f"vector v and trade vector u. Watch how vector addition changes your allocation "
        f"and how the norm measures total exposure.</p>",
        unsafe_allow_html=True,
    )

    mode = "2D" if mobile else st.radio("View", ["2D", "3D"], horizontal=True)

    if mobile:
        st.markdown("**v — portfolio weights**")
        v1 = st.slider("Apple (AAPL)", -1.0, 1.0, 0.40, 0.05, key="v1")
        v2 = st.slider("Microsoft (MSFT)", -1.0, 1.0, 0.35, 0.05, key="v2")
        st.markdown("**u — proposed trade**")
        u1 = st.slider("AAPL trade", -1.0, 1.0, 0.10, 0.05, key="u1")
        u2 = st.slider("MSFT trade", -1.0, 1.0, -0.05, 0.05, key="u2")
        v = [v1, v2]
        u = [u1, u2]
    else:
        col_v, col_u = st.columns(2)
        with col_v:
            st.markdown(f"**v — portfolio weights**")
            v1 = st.slider("Apple (AAPL)", -1.0, 1.0, 0.40, 0.05, key="v1")
            v2 = st.slider("Microsoft (MSFT)", -1.0, 1.0, 0.35, 0.05, key="v2")
            if mode == "3D":
                v3 = st.slider("Alphabet (GOOGL)", -1.0, 1.0, 0.25, 0.05, key="v3")
        with col_u:
            st.markdown(f"**u — proposed trade**")
            u1 = st.slider("AAPL trade", -1.0, 1.0, 0.10, 0.05, key="u1")
            u2 = st.slider("MSFT trade", -1.0, 1.0, -0.05, 0.05, key="u2")
            if mode == "3D":
                u3 = st.slider("GOOGL trade", -1.0, 1.0, -0.05, 0.05, key="u3")
        v = [v1, v2, v3] if mode == "3D" else [v1, v2]
        u = [u1, u2, u3] if mode == "3D" else [u1, u2]

    result = concept.compute(v=v, u=u)

    m1, m2, m3 = st.columns(3)
    m1.metric("‖v‖  (exposure size)", f"{result['norm_v']:.3f}")
    m2.metric("v · u  (dot product)", f"{result['dot_v_u']:.3f}")
    m3.metric("‖v + u‖  (after trade)", f"{result['norm_v_plus_u']:.3f}")

    fig = concept.visualize(v=v, u=u, mode=mode)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Self-check questions — no answers, forces recall
    st.divider()
    st.markdown(f"<h4 style='color:{theme.TEXT_MUTED};'>Check your understanding</h4>",
                unsafe_allow_html=True)
    st.markdown("""
- Set v = [0.5, 0.5] and u = [−0.5, −0.5]. What does ‖v + u‖ equal, and what does that mean about the trade?
- Why does scalar multiplication of a portfolio vector not change its *direction*, only its *magnitude*?
- If two portfolios have the same norm but different directions, what financial property makes them different?
""")


# ================================================================ TAB 3: GO DEEPER
with tab_deeper:
    st.markdown("<h3>Go Deeper</h3>", unsafe_allow_html=True)

    # Tier 1
    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Foundational — start here</h4>"
        f"<p><strong>Gilbert Strang, <em>Introduction to Linear Algebra</em> (4th ed.), "
        f"Chapter 1: Vectors and Linear Combinations.</strong><br>"
        f"Strang opens with vectors before matrices precisely because everything else is built "
        f"on this chapter. Read sections 1.1 and 1.2. His language — 'linear combination', "
        f"'column picture' — is the language every quant paper uses. Pair with his free MIT "
        f"OpenCourseWare 18.06 Lecture 1 (link Below), which "
        f"covers the same material in 45 minutes visually before you do the exercises.</p>"
        f"<p>Book: <a href = 'https://jcer.in/jcer-docs/E-Learning/Digital%20Library%20/E-Books/linear-algebra-author-gilbert-strang.pdf'> Gilbert Strang, <em>Introduction to Linear Algebra</em> (4th ed.)</a></p>"
        f"<p>Free lectures: <a href = 'https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-1-the-geometry-of-linear-equations/'> The Geometry of Linear Equations</a></p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Tier 2
    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Applied to quant finance</h4>"
        f"<p><strong>3Blue1Brown, <em>Essence of Linear Algebra</em> — Episode 1: Vectors "
        f"(YouTube, free, 9 minutes).</strong><br>"
        f"Watch this before reading Strang's chapter. Grant Sanderson's geometric "
        f"interpretation of vectors — as arrows in space — builds the visual intuition that "
        f"makes the portfolio-weight interpretation obvious rather than abstract. "
        f"The whole series is 15 short videos and covers everything in Phase 1.</p>"
        f"<p>YouTube Link: <a href='https://www.youtube.com/watch?v=fNk_zzaMoSs'> Essence of Linear Algebra </a></p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Tier 3
    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Practitioner depth</h4>"
        f"<p><strong>Dan Stefanica, <em>A Linear Algebra Primer for Financial Engineering</em>, "
        f"Chapter 1.</strong><br>"
        f"Stefanica covers vectors and norms specifically in the context of financial "
        f"engineering — portfolio weight vectors, return vectors, and the Euclidean norm as "
        f"a risk measure. The examples use real asset classes, not abstract x and y. "
        f"The chapter also includes the kind of worked numerical problems that appear in "
        f"quant interviews at banks and hedge funds, making it useful as both a study text "
        f"and an interview prep resource for later.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Forward connection
    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.LINEAR_ALGEBRA}33;'>"
        f"<h4>How this connects forward</h4>"
        f"<p>Vectors are the atom. Everything you build in the next 39 days is made of them. "
        f"Day 2 (Dot Product) asks: how do you measure alignment between two vectors? "
        f"Day 3 (Matrices) stacks vectors into a grid. Day 8 (Eigenvalues) finds the "
        f"special vectors that a matrix does not rotate. Day 9 (Covariance Matrices) builds "
        f"a matrix whose entries are dot products between return vectors. Day 10 (PCA) finds "
        f"the directions — vectors — along which your data varies most. "
        f"If the vector operations feel mechanical today, do not worry. "
        f"They will feel obvious by Day 10.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Recall card
    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>A portfolio's weights are a vector. Rebalancing is vector addition. "
        f"Risk size is the norm. Write these three sentences down tonight, "
        f"then close your notes and see if you can reproduce them tomorrow morning "
        f"before opening the app.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )


st.divider()
st.page_link("Home.py", label="Back to all concepts")
