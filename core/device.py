"""
core/device.py
Detects the visitor's viewport width so pages can render a genuinely different
layout for desktop vs mobile — not just CSS reflow, but different Python-level
decisions (column counts, default chart height, which controls are grouped
together). Falls back to a sane default if JS hasn't reported back yet.
"""

import streamlit as st

try:
    from streamlit_javascript import st_javascript
    _HAS_JS = True
except ImportError:
    _HAS_JS = False

MOBILE_BREAKPOINT = 768


def get_viewport_width() -> int:
    """Returns the browser's inner width in pixels. Cached per session so it's
    only queried once (avoids flicker on every rerun)."""
    if "viewport_width" in st.session_state:
        return st.session_state.viewport_width

    width = 1200  # desktop-first default while JS is still reporting back
    if _HAS_JS:
        try:
            result = st_javascript("window.innerWidth")
            if isinstance(result, (int, float)) and result > 0:
                width = int(result)
        except Exception:
            pass

    st.session_state.viewport_width = width
    return width


def is_mobile() -> bool:
    return get_viewport_width() < MOBILE_BREAKPOINT
