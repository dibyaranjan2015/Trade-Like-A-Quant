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
from core import progress

st.set_page_config(
    page_title="ThefacelessQuant",
    page_icon="assets/fq.ico",
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

completed = progress.get_completed_days()
streak = progress.current_streak(completed)
total_days = 40
built_days = len(REGISTRY)

stat1, stat2, stat3 = st.columns(3)
stat1.metric("Streak", f"{streak} day{'s' if streak != 1 else ''}")
stat2.metric("Completed", f"{len(completed)} / {built_days}")
stat3.metric("Series progress", f"{built_days} / {total_days}")

if streak == 0 and len(completed) == 0:
    st.markdown(
        f"<p style='color:{theme.TEXT_MUTED}; font-size:0.9rem;'>Pass a Day's "
        f"Challenge quiz to start your streak.</p>",
        unsafe_allow_html=True,
    )
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
            mark = " ✓" if day in completed else ""
            st.page_link(page_path, label=f"Day {day} — {concept.name}{mark}")
    else:
        cols = st.columns(2)
        for i, (day, concept, page_path) in enumerate(days_in_pillar):
            with cols[i % 2]:
                mark = " ✓" if day in completed else ""
                st.page_link(page_path, label=f"Day {day} — {concept.name}{mark}")

    st.write("")

st.divider()
st.markdown(
    f"<p style='color:{theme.TEXT_MUTED}; font-size:0.85rem;'>"
    "New concepts publish daily on Instagram, with the full build and weekly "
    "projects on LinkedIn.</p>",
    unsafe_allow_html=True,
)
