
import streamlit as st

from core import theme, progress
from core.device import is_mobile
from core.registry import REGISTRY
from core.curriculum import by_pillar, WEEKLY_PROJECTS

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
    "finance — one concept a day from linear algebra "
    "to options pricing.</p>",
    unsafe_allow_html=True,
)

completed = progress.get_completed_days()
streak = progress.current_streak(completed)
total_days = 40
built_days = len(REGISTRY)
registry_by_day = {day: (concept, page_path) for day, concept, page_path in REGISTRY}

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

mobile = is_mobile()


def render_day_link(day: int, name: str):
    mark = " \u2713" if day in completed else ""
    if day in registry_by_day:
        _, page_path = registry_by_day[day]
        st.page_link(page_path, label=f"Day {day} \u2014 {name}{mark}")
    else:
        st.page_link("Home.py", label=f"Day {day} \u2014 {name}", disabled=True)


for pillar, entries in by_pillar():
    color = theme.PILLAR_COLORS.get(pillar, theme.LINEAR_ALGEBRA)
    st.markdown(
        f"<h3 style='color:{color}; margin-bottom:4px;'>{pillar}</h3>",
        unsafe_allow_html=True,
    )

    # Group this pillar's entries by week so each week's project note sits
    # directly above that week's days, with a fresh column pair per week
    # (reusing one st.columns() across an interspersed markdown call doesn't
    # interleave correctly in Streamlit's layout model).
    weeks_in_pillar = sorted(set(e["week"] for e in entries))
    for week in weeks_in_pillar:
        week_entries = [e for e in entries if e["week"] == week]
        project = WEEKLY_PROJECTS.get(week)
        if project:
            st.markdown(
                f"<p style='color:{theme.LINEAR_ALGEBRA}; font-size:0.9rem; "
                f"margin:10px 0 8px 0; text-transform:uppercase; letter-spacing:0.05em;'>"
                f"Week {week} project: {project}</p>",
                unsafe_allow_html=True,
            )

        if mobile:
            for e in week_entries:
                render_day_link(e["day"], e["name"])
        else:
            cols = st.columns(2)
            for i, e in enumerate(week_entries):
                with cols[i % 2]:
                    render_day_link(e["day"], e["name"])

    st.write("")

st.divider()
st.markdown(
    f"<p style='color:{theme.TEXT_MUTED}; font-size:0.85rem;'>"
    "New concepts publish daily on Instagram, with the full build and weekly "
    "projects on LinkedIn.</p>",
    unsafe_allow_html=True,
)
