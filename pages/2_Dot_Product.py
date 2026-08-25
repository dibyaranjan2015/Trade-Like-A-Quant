"""
pages/2_Dot_Product.py
Day 2 — Dot Product & Geometry. UI only; math in core/day02_dot_product.py.
Three-tab study format: Learn, Practice, Go Deeper (matches Day 1's standard).
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
    st.button("#", label="Next: Matrices") # to be updated post page3 is published

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

            st.markdown(
                f"<div class='concept-panel' style='border-color:{theme.LINEAR_ALGEBRA}44;'>"
                f"<h4 style='color:{theme.LINEAR_ALGEBRA};'>Key Insight</h4>"
                f"<p>The dot product is doing two jobs at once: the component-wise formula "
                f"is how you'd actually compute it in code, but the geometric formula "
                f"‖v‖‖u‖cos θ is what it *means* — a measure of alignment. Every time you see "
                f"'cosine similarity' anywhere in finance or machine learning, it is this "
                f"exact formula, just renamed.</p></div>",
                unsafe_allow_html=True,
            )


# ================================================================ TAB 2: PRACTICE
with tab_practice:
    st.markdown("<h3>Interactive Playground</h3>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:{theme.TEXT_MUTED};'>Adjust your book's sector tilt against the "
        f"benchmark's weights and watch the angle between them change in real time. "
        f"A tight angle means you're hugging the benchmark; a wide one means you're "
        f"making an active bet.</p>",
        unsafe_allow_html=True,
    )

    mode = "2D" if mobile else st.radio("View", ["2D", "3D"], horizontal=True)

    if mobile:
        st.markdown("**v — your book's sector tilt**")
        v1 = st.slider("Tech sector", 0.0, 1.0, 0.60, 0.05, key="v1")
        v2 = st.slider("Financials sector", 0.0, 1.0, 0.30, 0.05, key="v2")
        st.markdown("**u — benchmark weights**")
        u1 = st.slider("Benchmark tech", 0.0, 1.0, 0.40, 0.05, key="u1")
        u2 = st.slider("Benchmark financials", 0.0, 1.0, 0.50, 0.05, key="u2")
        v = [v1, v2]
        u = [u1, u2]
    else:
        col_v, col_u = st.columns(2)
        with col_v:
            st.markdown("**v — your book's sector tilt**")
            v1 = st.slider("Tech sector", 0.0, 1.0, 0.60, 0.05, key="v1")
            v2 = st.slider("Financials sector", 0.0, 1.0, 0.30, 0.05, key="v2")
            if mode == "3D":
                v3 = st.slider("Energy sector", 0.0, 1.0, 0.10, 0.05, key="v3")
        with col_u:
            st.markdown("**u — benchmark weights**")
            u1 = st.slider("Benchmark tech", 0.0, 1.0, 0.40, 0.05, key="u1")
            u2 = st.slider("Benchmark financials", 0.0, 1.0, 0.50, 0.05, key="u2")
            if mode == "3D":
                u3 = st.slider("Benchmark energy", 0.0, 1.0, 0.10, 0.05, key="u3")
        v = [v1, v2, v3] if mode == "3D" else [v1, v2]
        u = [u1, u2, u3] if mode == "3D" else [u1, u2]

    result = concept.compute(v=v, u=u)

    m1, m2, m3 = st.columns(3)
    m1.metric("v · u  (dot product)", f"{result['dot']:.3f}")
    m2.metric("cos θ  (alignment)", f"{result['cos_theta']:.3f}")
    m3.metric("θ  (degrees apart)", f"{result['angle_deg']:.1f}°")

    fig = concept.visualize(v=v, u=u, mode=mode)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.divider()
    st.markdown(f"<h4 style='color:{theme.TEXT_MUTED};'>Check your understanding</h4>",
                unsafe_allow_html=True)
    st.markdown("""
- Set v exactly equal to u. What happens to θ, and why does that make sense for a portfolio that perfectly tracks its benchmark?
- Set v = [1.0, 0.0] and u = [0.0, 1.0]. What is v · u, and what does a dot product of zero tell you about two portfolios?
- If cos θ is negative, what does that imply about how your book would perform relative to the benchmark?
""")


# ================================================================ TAB 3: GO DEEPER
with tab_deeper:
    st.markdown("<h3>Go Deeper</h3>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Foundational — start here</h4>"
        f"<p><strong>Gilbert Strang, <em>Introduction to Linear Algebra</em> (4th ed.), "
        f"Section 1.2: Lengths and Dot Products.</strong><br>"
        f"This is literally the section right after Day 1 in Strang. He introduces the dot "
        f"product as the algebraic tool that measures the angle between vectors, and proves "
        f"that orthogonal vectors have a dot product of zero — the reason uncorrelated assets "
        f"have zero covariance later. Work through his proof that "
        f"cos θ = (v · u) / (‖v‖‖u‖) by hand once. You will use this formula constantly "
        f"from Day 21 onward.</p>"
        f"<p>Book: <a href = 'https://jcer.in/jcer-docs/E-Learning/Digital%20Library%20/E-Books/linear-algebra-author-gilbert-strang.pdf'> Gilbert Strang, <em>Introduction to Linear Algebra</em> (4th ed.)</a></p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Applied to quant finance</h4>"
        f"<p><strong>3Blue1Brown, <em>Essence of Linear Algebra</em> — Episode 9: Dot "
        f"Products and Duality (YouTube, free).</strong><br>"
        f"Explains why the dot product has both an algebraic definition (multiply "
        f"components, add) and a geometric one (projection) — and why they're the same "
        f"number. The projection interpretation is not obvious from the formula alone; "
        f"this video is the fastest way to make it click before you hit Day 21's "
        f"correlation coefficient, which is exactly this operation on standardised returns.</p>"
        f"<p> Youtube Link <a href = 'https://www.youtube.com/watch?v=LyGKycYT2v0&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab&index=9'> Episode 9: Dot Products and Duality </a> </p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='concept-panel'>"
        f"<h4>Practitioner depth</h4>"
        f"<p><strong>Rishi K. Narang, <em>Inside the Black Box</em> (2nd ed.), Chapter 3: "
        f"Alpha Models.</strong><br>"
        f"Narang explains how systematic strategies measure similarity between a predicted "
        f"return vector and realised returns — cosine similarity is the metric, and this is "
        f"one of the first places in practitioner literature where the dot product appears "
        f"as an operational tool rather than a textbook exercise. Accessible without heavy "
        f"maths, and gives you a real picture of what today's formula is doing inside "
        f"an actual fund.</p>"
        f"<p> Publically available Book:<a href = 'https://books.google.co.in/books?id=aYA0LnecyTgC&printsec=frontcover#v=onepage&q&f=false'> Inside the Black Box (Partial Readable Book)</a> </p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.LINEAR_ALGEBRA}33;'>"
        f"<h4>How this connects forward</h4>"
        f"<p>The dot product reappears on Day 21 (Covariance & Correlation) — the "
        f"correlation coefficient is the dot product of two standardised return vectors. "
        f"It reappears on Day 29 (CAPM) — beta is a scaled dot product of an asset's "
        f"returns with the market's. And it's the computational core of matrix "
        f"multiplication tomorrow (Day 3): multiplying a matrix by a vector is just "
        f"computing a dot product between each row and the vector, repeated.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='concept-panel' style='border-color:{theme.QUANT_FINANCE}44;'>"
        f"<h4>The one thing to remember tomorrow</h4>"
        f"<p>Multiply matching components and add — that's the dot product. Turn it into "
        f"an angle and you get a straight answer to how aligned two things are, in degrees. "
        f"Write this down tonight, then reproduce it from memory before opening tomorrow's app.</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.divider()
st.page_link("Home.py", label="Back to all concepts")
