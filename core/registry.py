"""
core/registry.py
Single source of truth for which days exist, which page file they live in, and
which pillar/week they belong to. Home.py reads this to build the mobile nav
cards AND the weekly grouping — add one line here each day you ship a new page.
"""

from core.day01_vectors import Vectors

# (day_number, concept_instance, page_path)
# page_path must exactly match the filename in pages/
REGISTRY = [
    (1, Vectors(), "pages/1_📐_Vectors.py"),
    # (2, DotProduct(), "pages/2_🎯_Dot_Product.py"),
    # (3, Matrices(), "pages/3_🔢_Matrices.py"),
    # ... add one line per day as you build it
]


def get_by_week(week: int):
    return [r for r in REGISTRY if r[1].week == week]


def get_by_day(day: int):
    for r in REGISTRY:
        if r[0] == day:
            return r
    return None
