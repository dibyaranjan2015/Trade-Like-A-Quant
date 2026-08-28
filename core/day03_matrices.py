"""
core/day03_matrices.py
Day 3 — Matrices & Matrix Operations (Linear Algebra, Week 1)
Pure logic + Plotly figure only. UI lives in pages/3_Matrices.py.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from core.base import QuantConcept
from core import theme

TICKERS = ["Apple", "Microsoft", "Amazon"]
DAYS = ["Day 1", "Day 2", "Day 3", "Day 4"]

# Daily returns: rows = days, columns = stocks
RETURNS = np.array([
    [0.010, -0.005, 0.020],
    [-0.008, 0.012, 0.005],
    [0.015, 0.000, -0.010],
    [0.002, 0.008, 0.011],
])


class Matrices(QuantConcept):
    name = "Matrices & Matrix Operations"
    day = 3
    pillar = "Linear Algebra"
    week = 1

    def content(self) -> dict:
        return {
            "tagline": "A grid of numbers that turns a table of returns into one multiply.",
            "definition": (
                "A matrix is a rectangular grid of numbers, arranged in rows and columns. "
                "It can hold a table of data — like every stock's return on every day — or "
                "describe an operation, like a rotation or a rebalance, applied all at once. "
                "The single most useful operation is multiplying a matrix by a vector: it "
                "takes a whole table and collapses it into one new vector in a single step."
            ),
            "formulas": [
                ("A matrix with m rows and n columns", r"A \in \mathbb{R}^{m \times n}, \quad A = \begin{bmatrix} a_{11} & \cdots & a_{1n} \\ \vdots & \ddots & \vdots \\ a_{m1} & \cdots & a_{mn} \end{bmatrix}"),
                ("Matrix addition", r"(A + B)_{ij} = a_{ij} + b_{ij}"),
                ("Matrix-vector multiplication", r"(A\mathbf{w})_i = \sum_{j=1}^{n} a_{ij} w_j"),
                ("Transpose", r"(A^T)_{ij} = a_{ji}"),
            ],
            "example": [
                ("text", "Take four days of returns for three stocks — Apple, Microsoft "
                          "and Amazon — and lay them out as a table, one row per day and "
                          "one column per stock. This table is a matrix:"),
                ("latex", r"R = \begin{bmatrix} 0.010 & -0.005 & 0.020 \\ -0.008 & 0.012 & 0.005 \\ 0.015 & 0.000 & -0.010 \\ 0.002 & 0.008 & 0.011 \end{bmatrix}"),
                ("text", "Now say the portfolio is weighted 50% Apple, 30% Microsoft and "
                          "20% Amazon. That weighting is a vector:"),
                ("latex", r"w = [0.50,\ 0.30,\ 0.20]"),
                ("text", "Multiplying the matrix by the vector turns every single day's "
                          "row of returns into one portfolio return for that day, all in "
                          "one step. For day one:"),
                ("latex", r"(0.010)(0.50) + (-0.005)(0.30) + (0.020)(0.20) = 0.0075"),
                ("text", "The same multiplication repeats automatically for every other "
                          "row, producing one portfolio return per day without writing a "
                          "loop. This is exactly how a risk system turns a table of raw "
                          "stock returns into a single portfolio return series, every "
                          "single day."),
            ],
            "application": (
                "Every returns series, factor-loading table, and risk model in quantitative "
                "finance is stored as a matrix, and R w — a returns matrix times a weights "
                "vector — is literally how a portfolio's daily P&L gets computed at scale. "
                "The same mechanic, X^T X, is the core of linear regression, and matrix "
                "multiplication is the operation every later pillar (transformations, "
                "covariance, PCA, factor models) builds directly on top of."
            ),
        }

    def compute(self, weights=None):
        w = np.array(weights if weights is not None else [0.50, 0.30, 0.20], dtype=float)
        portfolio_returns = RETURNS @ w
        return {
            "R": RETURNS,
            "w": w,
            "portfolio_returns": portfolio_returns,
            "weight_sum": float(w.sum()),
            "mean_return": float(portfolio_returns.mean()),
            "volatility": float(portfolio_returns.std()),
        }

    def visualize(self, weights=None):
        r = self.compute(weights)
        R, port = r["R"], r["portfolio_returns"]

        fig = make_subplots(
            rows=2, cols=1, row_heights=[0.55, 0.45],
            subplot_titles=("Returns matrix R", "Portfolio returns = R · w"),
            vertical_spacing=0.18,
        )

        fig.add_trace(
            go.Heatmap(
                z=R, x=TICKERS, y=DAYS,
                colorscale=[[0, theme.QUANT_FINANCE], [0.5, "#111827"], [1, theme.LINEAR_ALGEBRA]],
                zmid=0, showscale=False,
                text=np.round(R, 3), texttemplate="%{text}",
                textfont=dict(size=12, color=theme.TEXT_PRIMARY),
            ),
            row=1, col=1,
        )

        colors = [theme.PROBABILITY if v >= 0 else theme.QUANT_FINANCE for v in port]
        fig.add_trace(
            go.Bar(x=DAYS, y=port, marker_color=colors,
                   text=[f"{v:.3f}" for v in port], textposition="outside"),
            row=2, col=1,
        )

        fig.update_layout(template="quant_dark", height=560, showlegend=False,
                           margin=dict(l=10, r=10, t=50, b=10))
        return fig

    def quiz(self) -> list:
        return [
            {
                "question": "A returns matrix R is 4x3 (4 days, 3 stocks). What does R multiplied by a 3-element weight vector produce?",
                "options": ["A 3-element vector", "A 4-element vector — one portfolio return per day",
                            "A 4x3 matrix", "A single number"],
                "correct": 1,
                "explanation": "Each of the 4 rows gets collapsed into one number by the multiply — the result is a 4-element vector, one return per day.",
            },
            {
                "question": "What is (A + B)_ij, the ij-th entry of A + B?",
                "options": ["a_ij × b_ij", "a_ij + b_ij", "a_ji + b_ij", "a_ij - b_ji"],
                "correct": 1,
                "explanation": "Matrix addition is entrywise — you add the matching position in each matrix.",
            },
            {
                "question": "Why use matrix multiplication instead of a for-loop over each day?",
                "options": ["It's the only way to add numbers", "It expresses the same computation compactly, and every numerical library is built to optimise exactly this operation",
                            "It changes the result", "It avoids needing weights"],
                "correct": 1,
                "explanation": "The math is identical to a loop — matrix notation is just the compact, standard, and heavily-optimised way to express it.",
            },
        ]
