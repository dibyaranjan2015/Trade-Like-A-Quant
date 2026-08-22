"""
Home.py
ThefacelessQuant — landing page and primary navigation. Sidebar carries
branding and Streamlit's automatic page list, but everything a visitor needs
is reachable from cards on this page, since many arrive on mobile and never
open the sidebar.
"""

import streamlit as st

from core import theme
from core.device import is_mobile
from core.registry import REGISTRY, get_by_week

st.set_page_config(
    page_title="ThefacelessQuant",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed",
)
theme.inject_base_css()
theme.render_sidebar_brand()

st.markdown(
    "<p class='hero-title'>ThefacelessQuant</p>"
    "<p class='hero-subtitle'>A daily study of the mathematics behind quantitative "
    "finance — one concept a day, built in the open, from linear algebra through "
    "to options pricing.</p>",
    unsafe_allow_html=True,
)

total_days = 40
built_days = len(REGISTRY)
st.progress(built_days / total_days, text=f"{built_days} of {total_days} concepts published")
st.write("")

PILLAR_WEEKS = {
    "Linear Algebra": [1, 2],
    "Calculus": [3],
    "Probability & Stats": [4, 5],
    "Quant Finance": [6, 7, 8],
}

mobile = is_mobile()

for pillar, weeks in PILLAR_WEEKS.items():
    color = theme.PILLAR_COLORS[pillar]
    days_in_pillar = [d for w in weeks for d in get_by_week(w)]

    st.markdown(
        f"<h3 style='color:{color}; margin-bottom:4px;'>{pillar}</h3>",
        unsafe_allow_html=True,
    )

    if not days_in_pillar:
        st.markdown(
            f"<p style='color:{theme.TEXT_MUTED};'>In progress — first concept publishes soon.</p>",
            unsafe_allow_html=True,
        )
        st.write("")
        continue

    if mobile:
        for day, concept, page_path in days_in_pillar:
            st.page_link(page_path, label=f"Day {day} — {concept.name}")
    else:
        cols = st.columns(2)
        for i, (day, concept, page_path) in enumerate(days_in_pillar):
            with cols[i % 2]:
                st.page_link(page_path, label=f"Day {day} — {concept.name}")

    st.write("")

st.divider()
st.markdown(
    f"<p style='color:{theme.TEXT_MUTED}; font-size:0.85rem;'>"
    "New concepts publish daily on Instagram, with the full build and weekly "
    "projects on LinkedIn.</p>",
    unsafe_allow_html=True,
)
