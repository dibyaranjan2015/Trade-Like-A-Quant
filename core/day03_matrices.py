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
            "tagline": "A grid of numbers that turns a table of returns into one calculation.",
            "definition": (
                "A matrix is a rectangular grid of numbers, arranged in rows and columns. "
                "It's the way you store a table of data — like every stock's return on every day — "
                "all at once. The single most useful operation is multiplying a matrix by a vector: "
                "it takes a whole table and collapses it into one new vector in a single step, "
                "without writing a loop."
            ),
            "formulas": [
                ("A matrix with m rows and n columns (Ex: four days of returns for three stocks)",
                 r"A \in \mathbb{R}^{m \times n}, \quad A = \begin{bmatrix} a_{11} & \cdots & a_{1n} \\ \vdots & \ddots & \vdots \\ a_{m1} & \cdots & a_{mn} \end{bmatrix}"),
                ("Matrix addition (Ex: combining two portfolios' holdings into one)",
                 r"(A + B)_{ij} = a_{ij} + b_{ij}"),
                ("Matrix-vector multiplication (Ex: computing portfolio returns for all days in one step)",
                 r"(A\mathbf{w})_i = \sum_{j=1}^{n} a_{ij} w_j"),
                ("Transpose (Ex: flipping a returns table from 'rows=days, columns=stocks' to 'rows=stocks, columns=days')",
                 r"(A^T)_{ij} = a_{ji}"),
            ],
            "example": [
                ("text", "Lay out four days of returns for three stocks — Apple, Microsoft, "
                          "and Amazon — as a matrix, one row per day and one column per stock:"),
                ("latex", r"R = \begin{bmatrix} 0.010 & -0.005 & 0.020 \\ -0.008 & 0.012 & 0.005 \\ 0.015 & 0.000 & -0.010 \\ 0.002 & 0.008 & 0.011 \end{bmatrix}"),
                ("text", "Now say your portfolio is weighted 50% Apple, 30% Microsoft, and 20% Amazon. "
                          "That weighting is a vector:"),
                ("latex", r"w = [0.50,\ 0.30,\ 0.20]"),
                ("text", "Multiply the matrix by the vector and every single day's row gets collapsed into "
                          "one portfolio return for that day, all in one operation. For day one:"),
                ("latex", r"(0.010)(0.50) + (-0.005)(0.30) + (0.020)(0.20) = 0.0075"),
                ("text", "The same multiplication repeats automatically for every other row — no loop needed. "
                          "This is exactly how a risk system turns a table of raw stock returns into a "
                          "single portfolio return series, every day in production."),
            ],
            "application": (
                "Every returns series, factor-loading table, and risk model in quantitative "
                "finance is stored as a matrix.</p>"
                "<ul>"
                "<li><strong>Computing portfolio returns</strong> = matrix times vector (R w, exactly what we just did)</li>"
                "<li><strong>Linear regression</strong> = matrix multiplication, XᵀX, solving for beta</li>"
                "<li><strong>Covariance matrices</strong> = Day 9, rows and columns are the same stocks, entries are pairwise correlations</li>"
                "<li><strong>Factor models</strong> = the core of every quantitative strategy, built on matrix operations</li>"
                "</ul>"
                "<p><strong>The Bottom Line:</strong> Matrix multiplication is the operation every later pillar "
                "(transformations, eigenvalues, covariance, PCA, factor models) builds directly on top of."
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
                colorscale=[[0, theme.QUANT_FINANCE], [0.5, "#131a2a"], [1, theme.LINEAR_ALGEBRA]],
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
                "question": "A returns matrix R is 4×3 (4 days, 3 stocks). What does R multiplied by a 3-element weight vector produce?",
                "options": ["A 3-element vector", "A 4-element vector — one portfolio return per day",
                            "A 4×3 matrix", "A single number"],
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