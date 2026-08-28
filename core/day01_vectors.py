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
                "A vector is simply an organized list of numbers that gives you two things: "
                "magnitude(Size of your bet) and direction (the strategy you are executing). Whether you're plotting coordinates on a graph or"
                "balancing a multi-asset portfolio, vectors are the ultimate tool for tracking multiple "
                "moving parts at once. Each individual piece of that list is called a component."
            ),
            "formulas": [
                ("A vector with n components (Ex: The weights of n stocks in your Portfolio)", r"\mathbf{v} = [v_1,\ v_2,\ \ldots,\ v_n]"),
                ("Vector addition (Ex: Balancing your Portfolio weight after each trade)", r"\mathbf{v} + \mathbf{u} = [v_1+u_1,\ v_2+u_2,\ \ldots,\ v_n+u_n]"),
                ("Scalar multiplication (Ex: Scaling up or cashing out. You multiply every position by the same amount.)", r"c\,\mathbf{v} = [c v_1,\ c v_2,\ \ldots,\ c v_n]"),
                ("Norm/Length of a vector (Ex: Measuring the absolute size (or magnitude) of your total risk in the market.)", r"\lVert \mathbf{v} \rVert = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}"),
            ],
            "example": [
                ("text", "Take a three-asset portfolio holding Apple, Tesla and "
                          "Gold. The weight, or holding percentage, of each stock is "
                          "40%, 35% and 25% respectively. This allocation can be written "
                          "as the vector:"),
                ("latex", r"v = [0.40,\ 0.35,\ 0.25]"),
                ("text", "The length of the vector, or its norm, is:"),
                ("latex", r"\lVert v \rVert = \sqrt{0.40^2 + 0.35^2 + 0.25^2} \approx 0.587"),
                ("text", "That single number summarises how concentrated the position "
                          "is. Now suppose the plan is to rebalance the portfolio — "
                          "increase the Apple holding by 10%, funded by trimming "
                          "Tesla and Gold by 5% each. This trade is also a vector:"),
                ("latex", r"u = [0.10,\ -0.05,\ -0.05]"),
                ("text", "To find the new allocation after the trade, simply add the "
                          "two vectors:"),
                ("latex", r"v + u = [0.50,\ 0.30,\ 0.20]"),
                ("text", "This is exactly how portfolio managers rebalance a trading book "
                          "after every trade."),
            ],
            "application": (
                "Every portfolio, factor exposure, and return series in quantitative finance is just a vector." 
                "Here is the translation key between textbook math and Wall Street:"
                "<ul>"
                    "<li><strong>Rebalancing a book</strong> = Vector Addition</li>"
                    "<li><strong>Leveraging a position</strong> = Scalar Multiplication</li>"
                    "<li><strong>Measuring total risk</strong> = The Vector Norm</li>"
                "</ul>"
                "<p><strong>The Bottom Line:</strong> Every advanced technique later in this series — "
                "covariance matrices, PCA, and mean-variance optimization — is built directly on top of" 
                "these three basic operations."
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

    def quiz(self) -> list:
        return [
            {
                "question": "You hold v = [0.5, 0.5] and add a trade u = [-0.5, -0.5]. What is the norm of the resulting portfolio?",
                "options": ["0", "0.5", "1.0", "0.71"],
                "correct": 0,
                "explanation": "v + u = [0, 0] — the zero vector. Its norm is 0: you've fully closed the position.",
            },
            {
                "question": "Which operation changes a vector's magnitude but never its direction?",
                "options": ["Vector addition", "Scalar multiplication", "Taking the norm", "Dot product"],
                "correct": 1,
                "explanation": "Multiplying by a positive scalar c stretches or shrinks a vector along the same line — direction never changes.",
            },
            {
                "question": "A portfolio vector has a large norm. What does that tell you on its own?",
                "options": ["The portfolio is profitable", "The portfolio has large total exposure",
                            "The portfolio is well diversified", "The portfolio has low risk"],
                "correct": 1,
                "explanation": "The norm only measures magnitude of exposure — nothing about direction, diversification, or profitability.",
            },
        ]
