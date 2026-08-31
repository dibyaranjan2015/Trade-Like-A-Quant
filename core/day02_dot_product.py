"""
core/day02_dot_product.py
Day 2 — Dot Product & Geometry (Linear Algebra, Week 1)
Pure logic + Plotly figure only. UI lives in pages/2_Dot_Product.py.
"""

import math

import numpy as np
import plotly.graph_objects as go

from core.base import QuantConcept
from core import theme


class DotProduct(QuantConcept):
    name = "Dot Product & Geometry"
    day = 2
    pillar = "Linear Algebra"
    week = 1

    def content(self) -> dict:
        return {
            "tagline": "One calculation that tells you if two strategies are actually working together, or fighting each other.",
            "definition": (
                "A dot product combines two vectors into one number to show if they are pointing the same way."
                "You just multiply their matching parts and add them up. A big positive number means they agree,"
                "zero means they have nothing in common, and a negative number means they are going in opposite directions."
            ),
            "formulas": [
                ("Dot product, component form (Ex: How much do your book and the benchmark actually agree, number by number?)",
                 r"\mathbf{v} \cdot \mathbf{u} = v_1 u_1 + v_2 u_2 + \cdots + v_n u_n"),
                ("Dot product, geometric form (Ex: Translating that agreement into an angle you can actually picture)",
                 r"\mathbf{v} \cdot \mathbf{u} = \lVert \mathbf{v} \rVert\, \lVert \mathbf{u} \rVert \cos\theta"),
                ("Angle between two vectors (Ex: Are you hugging the benchmark, or making a real bet against it?)",
                 r"\cos\theta = \frac{\mathbf{v} \cdot \mathbf{u}}{\lVert \mathbf{v} \rVert\, \lVert \mathbf{u} \rVert}"),
                ("Projection of v onto u (Ex: The part of your book that's really just the benchmark in disguise)",
                 r"\text{proj}_{\mathbf{u}}\,\mathbf{v} = \frac{\mathbf{v} \cdot \mathbf{u}}{\lVert \mathbf{u} \rVert^2}\, \mathbf{u}"),
            ],
            "example": [
                ("text", "Say your book is tilted toward tech and financials — that's "
                          "a vector, v — while the benchmark you're measured against "
                          "sits at a different weighting, u:"),
                ("latex", r"v = [0.60,\ 0.30], \quad u = [0.40,\ 0.50]"),
                ("text", "The dot product multiplies the matching weights and adds "
                          "them up:"),
                ("latex", r"v \cdot u = (0.60)(0.40) + (0.30)(0.50) = 0.39"),
                ("text", "Divide that by the two vectors' lengths and it turns into "
                          "something you can actually picture — an angle:"),
                ("latex", r"\cos\theta = \frac{0.39}{\lVert v \rVert \lVert u \rVert} \approx 0.91 \ \Rightarrow\ \theta \approx 25^\circ"),
                ("text", "Your book isn't a carbon copy of the benchmark, but it's "
                          "pointing in a similar direction — a tight tracking error, "
                          "not an active bet against it. That 25° is the number a "
                          "portfolio manager would actually watch."),
            ],
            "application": (
                "Every alignment question in quantitative finance reduces to a "
                "dot product.</p>"
                "<ul>"
                "<li><strong>Tracking a benchmark</strong> = the angle between your "
                "book and the index</li>"
                "<li><strong>Factor exposure</strong> = the dot product between a "
                "stock's returns and a factor's returns</li>"
                "<li><strong>Signal strength</strong> = cosine similarity between a "
                "predicted-return vector and what actually happened</li>"
                "</ul>"
                "<p><strong>The Bottom Line:</strong> Every correlation coefficient, "
                "every beta, every \"how similar are these two strategies\" question "
                "you'll ever ask as a quant is the dot product wearing a different "
                "name."
            ),
        }

    def compute(self, v=None, u=None):
        v = np.array(v if v is not None else [0.60, 0.30], dtype=float)
        u = np.array(u if u is not None else [0.40, 0.50], dtype=float)

        dot = float(np.dot(v, u))
        norm_v = float(np.linalg.norm(v))
        norm_u = float(np.linalg.norm(u))
        denom = norm_v * norm_u
        cos_theta = dot / denom if denom > 1e-9 else 0.0
        cos_theta = max(-1.0, min(1.0, cos_theta))
        angle_deg = math.degrees(math.acos(cos_theta))

        proj = (dot / (norm_u ** 2)) * u if norm_u > 1e-9 else np.zeros_like(u)

        return {
            "v": v, "u": u,
            "dot": dot,
            "norm_v": norm_v, "norm_u": norm_u,
            "cos_theta": cos_theta,
            "angle_deg": angle_deg,
            "projection": proj,
        }

    def visualize(self, v=None, u=None, mode="2D"):
        r = self.compute(v, u)
        vec_v, vec_u, proj = r["v"], r["u"], r["projection"]
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

            # dashed projection line from v's tip to the projection point on u
            fig.add_trace(go.Scatter(
                x=[vec_v[0], proj[0]], y=[vec_v[1], proj[1]],
                mode="lines", line=dict(color=theme.TEXT_MUTED, width=1.5, dash="dot"),
                showlegend=False,
            ))
            arrow(vec_v[:2], theme.LINEAR_ALGEBRA, "Your Book")
            arrow(vec_u[:2], theme.QUANT_FINANCE, "Benchmark")
            arrow(proj[:2], theme.PROBABILITY, "Projection")

            fig.update_layout(template="quant_dark",
                               xaxis=dict(range=[-0.1, 1], title="Tech Sector Weight"),
                               yaxis=dict(range=[-0.1, 1], title="Financials Sector Weight"))
        else:
            def arrow3d(vec, color, label):
                fig.add_trace(go.Scatter3d(x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2] if len(vec) > 2 else 0],
                                            mode="lines+markers+text",
                                            line=dict(color=color, width=6),
                                            marker=dict(size=3, color=color),
                                            text=["", label],
                                            textfont=dict(color=color, size=13)))
            arrow3d(vec_v, theme.LINEAR_ALGEBRA, "Your Book")
            arrow3d(vec_u, theme.QUANT_FINANCE, "Benchmark")
            fig.update_layout(template="quant_dark", showlegend=False,
                               scene=dict(bgcolor="rgba(0,0,0,0)",
                                          xaxis=dict(range=[-0.1, 1], backgroundcolor="rgba(0,0,0,0)"),
                                          yaxis=dict(range=[-0.1, 1], backgroundcolor="rgba(0,0,0,0)"),
                                          zaxis=dict(range=[-0.1, 1], backgroundcolor="rgba(0,0,0,0)")))

        fig.update_layout(height=420, margin=dict(l=10, r=10, t=20, b=10))
        return fig

    def quiz(self) -> list:
        return [
            {
                "question": "If v · u = 0 for two nonzero vectors, what does that mean?",
                "options": ["They point in the same direction", "They are orthogonal (unrelated)",
                            "They have the same length", "One of them is the zero vector"],
                "correct": 1,
                "explanation": "A dot product of zero means the vectors are perpendicular — orthogonal, carrying no shared direction.",
            },
            {
                "question": "cos θ between your book and the benchmark is close to 1. What does that say?",
                "options": ["Very different positioning", "Nearly identical direction",
                            "Perfectly negatively correlated", "Nothing can be concluded"],
                "correct": 1,
                "explanation": "cos θ near 1 means the angle is near 0° — the two vectors point almost the same way.",
            },
            {
                "question": "Which is the geometric form of the dot product?",
                "options": ["v·u = ‖v‖ + ‖u‖", "v·u = ‖v‖‖u‖cos θ", "v·u = ‖v‖ / ‖u‖", "v·u = ‖v‖ - ‖u‖"],
                "correct": 1,
                "explanation": "v·u = ‖v‖‖u‖cos θ links the algebraic dot product to the angle between the two vectors.",
            },
        ]
