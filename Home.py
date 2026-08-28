"""
Main entry point for ThefacelessQuant Streamlit application.
"""
import streamlit as st

from core import progress, theme
from core.curriculum import WEEKLY_PROJECTS, by_pillar
from core.device import is_mobile
from core.registry import REGISTRY
import re

def setup_page():
    """Configure page settings and inject custom CSS/branding."""
    st.set_page_config(
        page_title="ThefacelessQuant",
        page_icon="assets/fq.ico",
        layout="wide", 
        initial_sidebar_state="expanded",
    )
    theme.inject_base_css()
    theme.render_sidebar_brand()

    theme.Home_page_setup()



def render_hero_section():
    """Render the main title and subtitle."""
    st.markdown("""
<div class='hero-title'>TheFaceLessQuant</div>
<div class='hero-subtitle'>A daily study of the mathematics behind quantitative finance — one concept a day from linear algebra to options pricing.</div>
""", unsafe_allow_html=True)


def render_progress_metrics(completed_days: set, built_days: int):
    
    streak = progress.current_streak(completed_days)
    total_days = 40
    
    # Notice: NO BLANK LINES inside this HTML string!
    st.markdown(f"""
<div class="stats-container">
    <div class="stat-card streak">
        <div class="stat-text">
            <h4>Streak</h4>
            <h2>{streak} days</h2>
        </div>
        <div class="stat-icon" style="font-size: 3rem;">🔥</div>
    </div>
    <div class="stat-card completed">
        <div class="stat-text">
            <h4>Completed</h4>
            <h2>{len(completed_days)} / {built_days}</h2>
        </div>
        <div class="stat-icon" style="font-size: 3rem;">⭕</div>
    </div>
    <div class="stat-card progress">
        <div class="stat-text">
            <h4>Series progress</h4>
            <h2>{built_days} / {total_days}</h2>
        </div>
        <div class="stat-icon" style="font-size: 3rem;">🟢</div>
    </div>
</div>
""", unsafe_allow_html=True)

    if streak == 0 and len(completed_days) == 0:
        st.markdown(
            "<p style='color:#9ca3af; font-size:0.9rem;'>Pass a Day's Challenge quiz to start your streak.</p>",
            unsafe_allow_html=True,
        )


def get_border_color(day: int):
    """Assigns border colors based on the day to match the screenshot pattern."""
    if day in [1, 5]: return "border-blue"
    if day in [2]: return "border-gold"
    if day in [3, 4]: return "border-green"
    if day >= 6: return "border-purple"
    return "border-blue"


def render_curriculum(completed_days: set, registry_by_day: dict):
    """Render the course curriculum grouped by pillar and week."""
    
    # 1. Add this set to keep track of which week banners have been shown
    rendered_weeks = set() 
    
    for pillar, entries in by_pillar():
        
        st.markdown(f"<h2>{pillar}</h2>", unsafe_allow_html=True)

        weeks_in_pillar = sorted(set(e["week"] for e in entries))
        
        for week in weeks_in_pillar:
            week_entries = [e for e in entries if e["week"] == week]
            project = WEEKLY_PROJECTS.get(week)
            
            banner_class = "banner-blue" if week % 2 != 0 else "banner-purple"
            
            # 2. Check if we have a project AND we haven't rendered this week yet
            if project and week not in rendered_weeks:
                st.markdown(f"""
<div class="week-banner {banner_class}">WEEK {week} PROJECT: {project}</div>
""", unsafe_allow_html=True)
                # 3. Mark this week as rendered so it doesn't duplicate in the next pillar
                rendered_weeks.add(week)

            # Build the grid HTML string without leading spaces or blank lines
            grid_html = '<div class="day-grid">\n'
            for e in week_entries:
                day = e["day"]
                name = e["name"]
                border_class = get_border_color(day)
                mark = "<span class='check-mark'>✓</span>" if day in completed_days else ""
                
                # Fetch the page_path from registry
                concept, page_path = registry_by_day.get(day, (name, ""))
                
                if page_path:
                    raw_name = page_path.split('/')[-1].replace('.py', '')
                    page_url = re.sub(r'^\d+_', '', raw_name)
                    
                    # NO INDENTATION in the HTML string!
                    grid_html += f"""<a href="{page_url}" target="_self" style="text-decoration: none; color: inherit; display: block;">
<div class="day-card {border_class}">
<p>Day {day} — {name} {mark}</p>
<span>⚪</span>
</div>
</a>\n"""
                else:
                    # Fallback for locked/unbuilt days
                    grid_html += f"""<div class="day-card {border_class}" style="opacity: 0.6; cursor: not-allowed;">
<p>Day {day} — {name} {mark}</p>
<span>🔒</span>
</div>\n"""
            
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)
        
        st.write("")


def render_footer():
    """Render the page footer details."""
    st.divider()
    st.markdown(
        "<p style='color:#6b7280; font-size:0.85rem;'>"
        "New concepts publish daily on Instagram, with the full build and weekly "
        "projects on LinkedIn.</p>",
        unsafe_allow_html=True,
    )


def main():
    setup_page()
    
    # Process Data
    completed_days = progress.get_completed_days()
    built_days = len(REGISTRY)
    registry_by_day = {day: (concept, page_path) for day, concept, page_path in REGISTRY}
    
    # Render UI Components
    render_hero_section()
    render_progress_metrics(completed_days, built_days)
    render_curriculum(completed_days, registry_by_day)
    render_footer()


if __name__ == "__main__":
    main()