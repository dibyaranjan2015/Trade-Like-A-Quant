"""
core/day01_vectors.py
Day 1 — Vectors & Vector Operations (Linear Algebra, Week 1)
Pure logic + Plotly figure only. UI lives in pages/1_Vectors.py.
"""

import numpy as np
import plotly.graph_objects as go

from core.base import QuantConcept
from core import theme


class Vectors(QuantConcept):
    name = "Vectors & Vector Operations"
    day = 1
    pillar = "Linear Algebra"
    week = 1

    def content(self) -> dict:
        return {
            "tagline": "Magnitude, direction, and how a portfolio is really just a list of numbers.",
            "definition": (
                "A vector is an ordered list of numbers that captures both a size and a "
                "direction. Written out, a vector with n entries looks like this, and each "
                "entry is called a component."
            ),
            "formulas": [
                ("A vector with n components", r"\mathbf{v} = [v_1,\ v_2,\ \ldots,\ v_n]"),
                ("Vector addition", r"\mathbf{v} + \mathbf{u} = [v_1+u_1,\ v_2+u_2,\ \ldots,\ v_n+u_n]"),
                ("Scalar multiplication", r"c\,\mathbf{v} = [c v_1,\ c v_2,\ \ldots,\ c v_n]"),
                ("Norm (length) of a vector", r"\lVert \mathbf{v} \rVert = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}"),
            ],
            "example": (
                "Take a three-stock portfolio holding Apple, Microsoft and Amazon. The weight or the holding percentage of each stock"
                "is 40%, 35% and 25% respectively. This stock allocation is the vector can be written as v = [0.40, 0.35, 0.25]. "
                "The length of the vector or Norm is √(0.40² + 0.35² + 0.25²) ≈ 0.587 — a single number that summarises "
                "how concentrated the position is. Now suppose we want to rebalance the portfolio holding, for example we want" 
                "to increase the Apple holding by 10%, "
                "by trimming the holding of Microsoft and Alphabet by 5% each. This rebalance/trade is also a vector"
                "u = [0.10, −0.05, −0.05]. To find the new allocation post trade we can simply add these two vectors" 
                "and the new allocation is simply v + u = [0.50, 0.30, 0.20]. This is how the porfolio managers balance there portfolio after each trade."
            ),
            "application": (
                "Every portfolio, factor exposure, and return series in quantitative finance is "
                "stored and manipulated as a vector. Rebalancing a book is vector addition. "
                "Leveraging a position is scalar multiplication. Measuring how much risk a "
                "portfolio carries in aggregate starts with its norm. Every technique later in "
                "this series — covariance matrices, PCA, mean-variance optimisation — is built "
                "directly on top of these three operations."
            ),
        }

    def compute(self, v=None, u=None):
        v = np.array(v if v is not None else [0.40, 0.35, 0.25], dtype=float)
        u = np.array(u if u is not None else [0.10, -0.05, -0.05], dtype=float)
        return {
            "v": v,
            "u": u,
            "v_plus_u": v + u,
            "norm_v": float(np.linalg.norm(v)),
            "norm_v_plus_u": float(np.linalg.norm(v + u)),
            "dot_v_u": float(np.dot(v, u)),
        }

    def visualize(self, v=None, u=None, mode="2D"):
        r = self.compute(v, u)
        vec_v, vec_u, vec_sum = r["v"], r["u"], r["v_plus_u"]
        fig = go.Figure()

        if mode == "2D":
            def arrow(vec, color, label):
                fig.add_annotation(x=vec[0], y=vec[1], ax=0, ay=0, xref="x", yref="y",
                                    axref="x", ayref="y", showarrow=True, arrowhead=3,
                                    arrowsize=1.4, arrowwidth=3, arrowcolor=color)
                fig.add_trace(go.Scatter(x=[vec[0]], y=[vec[1]], mode="markers+text",
                                          marker=dict(size=1, color=color), text=[label],
                                          textposition="top center", showlegend=False,
                                          textfont=dict(color=color, size=13)))
            arrow(vec_v[:2], theme.LINEAR_ALGEBRA, "v")
            arrow(vec_u[:2], theme.QUANT_FINANCE, "u")
            arrow(vec_sum[:2], theme.PROBABILITY, "v + u")
            fig.update_layout(template="quant_dark",
                               xaxis=dict(range=[-1, 1], title="Asset 1 weight"),
                               yaxis=dict(range=[-1, 1], title="Asset 2 weight"))
        else:
            def arrow3d(vec, color, label):
                fig.add_trace(go.Scatter3d(x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]],
                                            mode="lines+markers+text",
                                            line=dict(color=color, width=6),
                                            marker=dict(size=3, color=color),
                                            text=["", label],
                                            textfont=dict(color=color, size=13)))
            arrow3d(vec_v, theme.LINEAR_ALGEBRA, "v")
            arrow3d(vec_u, theme.QUANT_FINANCE, "u")
            arrow3d(vec_sum, theme.PROBABILITY, "v + u")
            fig.update_layout(template="quant_dark", showlegend=False,
                               scene=dict(bgcolor="rgba(0,0,0,0)",
                                          xaxis=dict(range=[-1, 1], backgroundcolor="rgba(0,0,0,0)"),
                                          yaxis=dict(range=[-1, 1], backgroundcolor="rgba(0,0,0,0)"),
                                          zaxis=dict(range=[-1, 1], backgroundcolor="rgba(0,0,0,0)")))

        fig.update_layout(height=420, margin=dict(l=10, r=10, t=20, b=10))
        return fig
