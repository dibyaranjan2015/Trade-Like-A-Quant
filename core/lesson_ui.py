"""
core/lesson_ui.py
Shared interactive components so every day's page is built from the same
three moves instead of a hand-written wall of text: a paced Learn flow, a
tap-first Practice picker, and a Challenge quiz. Reused by every pages/*.py.
"""

import streamlit as st

from core import theme, progress


# ==================================================================
# LEARN — one idea per screen, not three paragraphs at once
# ==================================================================
def render_learn_flow(concept, data: dict):
    step_key = f"learn_step_day{concept.day}"
    st.session_state.setdefault(step_key, 0)

    steps = [
        ("The Big Idea", "definition"),
        ("The Formula", "formulas"),
        ("Worked Example", "example"),
        ("Why It Matters", "application"),
    ]
    idx = max(0, min(st.session_state[step_key], len(steps) - 1))
    title, field = steps[idx]

    # progress dots
    dots = "".join(
        f"<span style='display:inline-block; width:8px; height:8px; border-radius:50%; "
        f"margin-right:6px; background:{theme.LINEAR_ALGEBRA if i <= idx else theme.PANEL_BORDER};'></span>"
        for i in range(len(steps))
    )
    st.markdown(f"<div style='margin-bottom:10px;'>{dots}</div>", unsafe_allow_html=True)

    if field == "formulas":
        theme.concept_panel(title, "")
        for label, latex_str in data["formulas"]:
            st.markdown(f"<p style='color:{theme.TEXT_MUTED}; margin-bottom:2px; "
                        f"font-size:0.9rem;'>{label}</p>", unsafe_allow_html=True)
            st.latex(latex_str)
    elif field == "example" and isinstance(data["example"], list):
        # Segmented format: alternating ("text", str) / ("latex", str) tuples,
        # so a worked example can interleave plain prose with real typeset
        # formulas instead of unicode math crammed into one paragraph.
        theme.panel_open(title)
        for kind, content in data["example"]:
            if kind == "latex":
                st.latex(content)
            else:
                st.markdown(f"<p>{content}</p>", unsafe_allow_html=True)
        theme.panel_close()
    else:
        theme.concept_panel(title, f"<p>{st.markdown(data[field])}</p>")

    nav_back, nav_next = st.columns(2)
    with nav_back:
        if st.button("Back", disabled=(idx == 0), use_container_width=True, key=f"{step_key}_back"):
            st.session_state[step_key] = idx - 1
            st.rerun()
    with nav_next:
        is_last = idx == len(steps) - 1
        label = "Head to Practice ->" if is_last else "Next"
        if st.button(label, use_container_width=True, type="primary", key=f"{step_key}_next"):
            if not is_last:
                st.session_state[step_key] = idx + 1
                st.rerun()


# ==================================================================
# PRACTICE — tap a preset first; sliders are an opt-in, not the default
# ==================================================================
def preset_picker(presets: dict, key: str, default: str, columns: int = 2):
    """
    presets: {label: value}. Renders as a button grid; tapping one selects
    it (highlighted), returns the currently-selected value. Replaces
    drag-heavy sliders as the default mobile interaction.
    """
    st.session_state.setdefault(key, default)
    labels = list(presets.keys())
    cols = st.columns(columns)
    for i, label in enumerate(labels):
        with cols[i % columns]:
            selected = st.session_state[key] == label
            if st.button(
                label, use_container_width=True, key=f"{key}_{label}",
                type="primary" if selected else "secondary",
            ):
                st.session_state[key] = label
                st.rerun()
    return presets[st.session_state[key]]


# ==================================================================
# CHALLENGE — the end-of-day quiz that drives the streak
# ==================================================================
def render_challenge(concept):
    questions = concept.quiz()
    if not questions:
        st.info("This day's challenge is coming soon.")
        return

    day = concept.day
    completed = progress.get_completed_days()
    already_done = day in completed

    if already_done:
        st.markdown(
            f"<div class='concept-panel' style='border-color:{theme.PROBABILITY}66;'>"
            f"<h4 style='color:{theme.PROBABILITY};'>Day {day} complete</h4>"
            f"<p>You've already passed this challenge. Retake it any time to refresh "
            f"your memory — it won't change your streak.</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown(f"<p style='color:{theme.TEXT_MUTED};'>Three questions. Get them all "
                f"right to mark today complete and keep your streak.</p>",
                unsafe_allow_html=True)

    answers = []
    for i, q in enumerate(questions):
        st.markdown(f"**{i + 1}. {q['question']}**")
        picked = st.radio("options", q["options"], key=f"quiz_day{day}_{i}",
                           label_visibility="collapsed", index=None)
        answers.append(picked)

    if st.button("Check my answers", type="primary", use_container_width=True, key=f"quiz_day{day}_submit"):
        if any(a is None for a in answers):
            st.warning("Answer all three before checking.")
            return

        correct_count = 0
        for i, q in enumerate(questions):
            is_correct = answers[i] == q["options"][q["correct"]]
            correct_count += int(is_correct)
            color = theme.PROBABILITY if is_correct else theme.QUANT_FINANCE
            verdict = "Correct" if is_correct else "Not quite"
            st.markdown(
                f"<p style='color:{color};'><strong>{verdict}</strong> — {q['explanation']}</p>",
                unsafe_allow_html=True,
            )

        if correct_count == len(questions):
            progress.mark_day_complete(day)
            streak = progress.current_streak()
            st.balloons()
            st.success(f"Day {day} complete. {streak}-day streak.")
        else:
            st.info(f"{correct_count}/{len(questions)} correct — give it another look above and try again.")
