"""
core/progress.py
Tracks which days a visitor has completed (passed the Challenge quiz) and
their current streak, persisted via browser cookie so it survives closing
the tab — no login system required.

Honest limitation: this is per-browser, not per-account. Clearing cookies
or switching devices resets it. That's an acceptable trade-off for a
public, no-signup learning app; if accounts are ever added, swap this
module's storage for a real per-user database and keep the same functions.

Requires: streamlit-cookies-controller (see requirements.txt). Falls back
to session-only tracking (resets on tab close) if the package isn't
installed, so the app never breaks — it just loses persistence.
"""

import json

import streamlit as st

try:
    from streamlit_cookies_controller import CookieController
    _HAS_COOKIES = True
except ImportError:
    _HAS_COOKIES = False

COOKIE_KEY = "tfq_completed_days"


def _controller():
    if "_cookie_controller" not in st.session_state:
        st.session_state["_cookie_controller"] = CookieController() if _HAS_COOKIES else None
    return st.session_state["_cookie_controller"]


def get_completed_days() -> set:
    if _HAS_COOKIES:
        controller = _controller()
        raw = controller.get(COOKIE_KEY)
        try:
            return set(json.loads(raw)) if raw else set()
        except (TypeError, ValueError):
            return set()
    return st.session_state.setdefault("_completed_days_fallback", set())


def mark_day_complete(day: int):
    completed = get_completed_days()
    completed.add(day)
    if _HAS_COOKIES:
        _controller().set(COOKIE_KEY, json.dumps(sorted(completed)))
    else:
        st.session_state["_completed_days_fallback"] = completed


def current_streak(completed: set = None) -> int:
    """Consecutive days completed counting back from the highest day done."""
    completed = completed if completed is not None else get_completed_days()
    if not completed:
        return 0
    streak = 0
    day = max(completed)
    while day in completed:
        streak += 1
        day -= 1
    return streak
