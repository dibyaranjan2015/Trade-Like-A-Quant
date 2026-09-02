"""
core/day04_linear_transformations.py
Day 4 — Linear Transformations (Linear Algebra, Week 1)
Pure logic + Plotly figure only. UI lives in pages/4_Linear_Transformations.py.
"""

import numpy as np
import plotly.graph_objects as go

from core.base import QuantConcept
from core import theme


class LinearTransformations(QuantConcept):
    name = "Linear Transformations"
    day = 4
    pillar = "Linear Algebra"
    week = 1

    def content(self) -> dict:
        return {
            "tagline": "A matrix isn't just a grid of numbers — it's a machine that moves every point in space.",
            "definition": (
                "A linear transformation is what a matrix actually *does* to a vector. "
                "It takes every point in space and moves it somewhere else — but in a "
                "very restrained way: the origin never moves, straight lines stay "
                "straight, and evenly spaced points stay evenly spaced. Multiplying "
                "by a matrix isn't just arithmetic — it's applying a consistent rule "
                "that stretches, shrinks, or flips an entire space, all in one operation."
            ),
            "formulas": [
                ("A linear transformation, defined (Ex: doubling every stock's return scales your whole return vector at once)",
                 r"T(\mathbf{v}) = A\mathbf{v}"),
                ("Additivity (Ex: the outcome of a combined trade equals the sum of each trade's outcome, transformed separately)",
                 r"T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})"),
                ("Homogeneity (Ex: doubling your position size doubles the transformed outcome, exactly)",
                 r"T(c\mathbf{v}) = c\,T(\mathbf{v})"),
                ("What the columns of A mean (Ex: knowing what happens to '1 share of each stock' tells you what happens to any portfolio)",
                 r"T(\mathbf{e}_i) = i\text{-th column of } A"),
            ],
            "example": [
                ("text", "Say you apply a simple rule to your book: scale your Tech "
                          "position up 1.5× (raise conviction), and scale your Gold "
                          "position down to 0.5× (cut the hedge). That rule is a matrix:"),
                ("latex", r"A = \begin{bmatrix} 1.5 & 0 \\ 0 & 0.5 \end{bmatrix}"),
                ("text", "Apply it to a starting portfolio — 40% Tech, 60% Gold:"),
                ("latex", r"A\mathbf{v} = \begin{bmatrix} 1.5 & 0 \\ 0 & 0.5 \end{bmatrix}\begin{bmatrix} 0.40 \\ 0.60 \end{bmatrix} = \begin{bmatrix} 0.60 \\ 0.30 \end{bmatrix}"),
                ("text", "Every portfolio you run through this same matrix gets scaled "
                          "the exact same way — Tech positions grow by 50%, Gold "
                          "positions shrink by half, no matter what the starting "
                          "weights were. That consistency is exactly what makes it "
                          "\"linear\": the rule never changes based on the input."),
            ],
            "application": (
                "Every model that turns one set of numbers into another set of "
                "numbers, consistently, is a linear transformation.</p>"
                "<ul>"
                "<li><strong>Currency hedging</strong> = a matrix that converts raw "
                "exposure into currency-hedged exposure</li>"
                "<li><strong>Risk scaling</strong> = a matrix that converts dollar "
                "positions into volatility-adjusted risk units</li>"
                "<li><strong>Factor models</strong> = a matrix that converts stock "
                "returns into factor exposures</li>"
                "</ul>"
                "<p><strong>The Bottom Line:</strong> Every matrix you'll use for the "
                "rest of this series is secretly a transformation — a consistent rule "
                "for turning one vector into another. That idea is exactly what makes "
                "eigenvalues (Day 8) make sense: an eigenvector is just a direction "
                "the transformation doesn't rotate, only stretches."
            ),
        }

    def compute(self, a1=1.5, a2=0.5, v=None):
        A = np.array([[a1, 0.0], [0.0, a2]], dtype=float)
        v = np.array(v if v is not None else [0.40, 0.60], dtype=float)
        Av = A @ v
        return {
            "A": A, "v": v, "Av": Av,
            "a1": a1, "a2": a2,
            "norm_v": float(np.linalg.norm(v)),
            "norm_Av": float(np.linalg.norm(Av)),
            "det": float(a1 * a2),
        }

    def visualize(self, a1=1.5, a2=0.5, v=None):
        r = self.compute(a1, a2, v)
        vec_v, vec_Av = r["v"], r["Av"]
        fig = go.Figure()

        # original unit square (dotted) vs transformed rectangle (solid) —
        # visually shows how the whole space stretches, not just one vector
        fig.add_trace(go.Scatter(
            x=[0, 1, 1, 0, 0], y=[0, 0, 1, 1, 0], mode="lines",
            line=dict(color=theme.TEXT_MUTED, width=1, dash="dot"),
            name="Original space", showlegend=True,
        ))
        fig.add_trace(go.Scatter(
            x=[0, a1, a1, 0, 0], y=[0, 0, a2, a2, 0], mode="lines",
            line=dict(color=theme.CALCULUS, width=2),
            name="Transformed space", showlegend=True,
        ))

        def arrow(vec, color, label):
            fig.add_annotation(x=vec[0], y=vec[1], ax=0, ay=0, xref="x", yref="y",
                                axref="x", ayref="y", showarrow=True, arrowhead=3,
                                arrowsize=1.4, arrowwidth=3, arrowcolor=color)
            fig.add_trace(go.Scatter(x=[vec[0]], y=[vec[1]], mode="markers+text",
                                      marker=dict(size=1, color=color), text=[label],
                                      textposition="top center", showlegend=False,
                                      textfont=dict(color=color, size=13)))

        arrow(vec_v, theme.LINEAR_ALGEBRA, "v (before)")
        arrow(vec_Av, theme.QUANT_FINANCE, "Av (after)")

        max_range = max(2.2, float(np.max(np.abs(np.concatenate([vec_v, vec_Av])))) + 0.5)
        fig.update_layout(template="quant_dark",
                           xaxis=dict(range=[-0.2, max_range], title="Tech Weight"),
                           yaxis=dict(range=[-0.2, max_range], title="Gold Weight"),
                           height=420, margin=dict(l=10, r=10, t=20, b=10))
        return fig

    def quiz(self) -> list:
        return [
            {
                "question": "A linear transformation always sends the origin (0, 0) to...",
                "options": ["A random point", "The origin (0, 0) — it never moves",
                            "Infinity", "It depends on the matrix"],
                "correct": 1,
                "explanation": "Keeping the origin fixed is part of the definition of linear — a rule that moves the origin is called 'affine' instead, not linear.",
            },
            {
                "question": "If T(u+v) = T(u)+T(v) and T(cv) = cT(v) both hold for a rule T, what do we call T?",
                "options": ["A scalar", "A linear transformation", "A vector", "An eigenvalue"],
                "correct": 1,
                "explanation": "Those two properties — additivity and homogeneity — are exactly the definition of a linear transformation.",
            },
            {
                "question": "The columns of a transformation matrix A tell you...",
                "options": ["The eigenvalues of A", "Where each standard basis vector ends up after the transformation",
                            "The determinant of A", "Nothing useful"],
                "correct": 1,
                "explanation": "Each column of A is literally T applied to the corresponding standard basis vector — that's why the columns alone define the whole transformation.",
            },
        ]
