"""
core/registry.py
Single source of truth for which days exist and which page they live on.
Add one line here each day you ship a new page — Home.py reads this list.
"""

from core.day01_vectors import Vectors
from core.day02_dot_product import DotProduct
# from core.day03_matrices import Matrices

# (day_number, concept_instance, page_path)
REGISTRY = [
    (1, Vectors(), "pages/1_Vectors.py"),
    (2, DotProduct(), "pages/2_Dot_Product.py"),
    # (3, Matrices(), "pages/3_Matrices.py"),
    # (4, LinearTransformations(), "pages/4_Linear_Transformations.py"),
]


def get_by_week(week: int):
    return [r for r in REGISTRY if r[1].week == week]


def get_by_day(day: int):
    for r in REGISTRY:
        if r[0] == day:
            return r
    return None
