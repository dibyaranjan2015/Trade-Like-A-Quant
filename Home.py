"""
Home.py
#ThefacelessQuant — Home / landing page.

IMPORTANT: this page is the primary navigation, not the sidebar. Many mobile
visitors land here from an Instagram bio link and never tap the hamburger
menu — so every day's app must be reachable as a big tappable card right here.
The sidebar (see core/theme.render_sidebar_brand) still shows the auto page
list for desktop users, but nothing is ever sidebar-only.
"""

import streamlit as st

from core import theme
from core.registry import REGISTRY, get_by_week

st.set_page_config(
    page_title="ThefacelessQuant",
    page_icon="📈",
    layout="centered",          # centered = single readable column, best on mobile
    initial_sidebar_state="collapsed",  # don't rely on it being open
)
theme.inject_base_css()
theme.render_sidebar_brand()

st.markdown(
    f"""
    <h1 style='color:{theme.LINEAR_ALGEBRA}; margin-bottom:0;'>ThefacelessQuant</h1>
    <p style='color:{theme.TEXT_MUTED}; margin-top:4px;'>
        Learn a quant concept a day — Math → Code → Visual → Reel.<br>
        40 days, 4 pillars, 6 real projects.
    </p>
    """,
    unsafe_allow_html=True,
)

total_days = 40
built_days = len(REGISTRY)
st.progress(built_days / total_days, text=f"{built_days}/{total_days} days live")

st.divider()

PILLAR_WEEKS = {
    "Linear Algebra": [1, 2],
    "Calculus": [3],
    "Probability & Stats": [4, 5],
    "Quant Finance": [6, 7, 8],
}

for pillar, weeks in PILLAR_WEEKS.items():
    color = theme.PILLAR_COLORS[pillar]
    st.markdown(f"<h3 style='color:{color};'>{pillar}</h3>", unsafe_allow_html=True)

    any_card = False
    for week in weeks:
        for day, concept, page_path in get_by_week(week):
            any_card = True
            # One big tappable card per day — this IS the mobile nav.
            st.page_link(
                page_path,
                label=f"Day {day} — {concept.name}",
                icon=concept.icon,
            )
    if not any_card:
        st.caption("Coming soon...")

    st.write("")  # spacing between pillar sections

st.divider()
st.markdown(
    f"<p style='color:{theme.TEXT_MUTED}; font-size:0.85rem;'>"
    "Follow the daily build on Instagram @ThefacelessQuant · "
    "Weekly projects posted on LinkedIn</p>",
    unsafe_allow_html=True,
)
