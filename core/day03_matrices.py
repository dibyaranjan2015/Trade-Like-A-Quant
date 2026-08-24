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

TICKERS = ["Stock A", "Stock B", "Stock C"]
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
            "example": (
                "Lay out four days of returns for three stocks as a 4×3 matrix R — one row "
                "per day, one column per stock. Multiply R by a weights vector "
                "w = [0.50, 0.30, 0.20] and every row turns into a single portfolio return "
                "for that day in one operation: day one becomes "
                "(0.010)(0.50) + (−0.005)(0.30) + (0.020)(0.20) = 0.0075, and the same "
                "multiply repeats automatically for every other day. That's the whole "
                "point of matrix multiplication — collapsing a table into a vector without "
                "writing a loop."
            ),
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
