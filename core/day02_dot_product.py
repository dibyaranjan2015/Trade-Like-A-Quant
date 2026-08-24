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
            "tagline": "One number that measures how closely two vectors point the same way.",
            "definition": (
                "The dot product takes two vectors and returns a single number. "
                "Multiply the vectors component by component and add the results — "
                "that number tells you how much two vectors move together. A large "
                "positive dot product means they point the same way; a value near "
                "zero means they're unrelated; a negative value means they point "
                "in opposite directions."
            ),
            "formulas": [
                ("Dot product, component form", r"\mathbf{v} \cdot \mathbf{u} = v_1 u_1 + v_2 u_2 + \cdots + v_n u_n"),
                ("Dot product, geometric form", r"\mathbf{v} \cdot \mathbf{u} = \lVert \mathbf{v} \rVert\, \lVert \mathbf{u} \rVert \cos\theta"),
                ("Angle between two vectors", r"\cos\theta = \frac{\mathbf{v} \cdot \mathbf{u}}{\lVert \mathbf{v} \rVert\, \lVert \mathbf{u} \rVert}"),
                ("Projection of v onto u", r"\text{proj}_{\mathbf{u}}\,\mathbf{v} = \frac{\mathbf{v} \cdot \mathbf{u}}{\lVert \mathbf{u} \rVert^2}\, \mathbf{u}"),
            ],
            "example": (
                "Say your book is tilted v = [0.60, 0.30] across two sectors, and the "
                "benchmark you're measured against sits at u = [0.40, 0.50]. The dot "
                "product is (0.60 × 0.40) + (0.30 × 0.50) = 0.39. Dividing by the two "
                "vectors' lengths gives cos θ ≈ 0.91, which puts the angle between them "
                "at about 25°. Your book isn't identical to the benchmark, but it's "
                "pointing in a similar direction — a tight tracking error, not a bet "
                "against it."
            ),
            "application": (
                "Cosine similarity between return vectors is exactly this calculation, "
                "and it's how factor models measure how much a stock 'loads' onto a "
                "factor, how tracking error against a benchmark gets quantified, and "
                "how recommendation and clustering systems in quant research measure "
                "similarity between assets. The projection formula is also the first "
                "step toward least-squares regression, which shows up constantly from "
                "here on."
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
            arrow(vec_v[:2], theme.LINEAR_ALGEBRA, "v")
            arrow(vec_u[:2], theme.QUANT_FINANCE, "u")
            arrow(proj[:2], theme.PROBABILITY, "proj")

            fig.update_layout(template="quant_dark",
                               xaxis=dict(range=[-0.1, 1], title="Sector 1 weight"),
                               yaxis=dict(range=[-0.1, 1], title="Sector 2 weight"))
        else:
            def arrow3d(vec, color, label):
                fig.add_trace(go.Scatter3d(x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2] if len(vec) > 2 else 0],
                                            mode="lines+markers+text",
                                            line=dict(color=color, width=6),
                                            marker=dict(size=3, color=color),
                                            text=["", label],
                                            textfont=dict(color=color, size=13)))
            arrow3d(vec_v, theme.LINEAR_ALGEBRA, "v")
            arrow3d(vec_u, theme.QUANT_FINANCE, "u")
            fig.update_layout(template="quant_dark", showlegend=False,
                               scene=dict(bgcolor="rgba(0,0,0,0)",
                                          xaxis=dict(range=[-0.1, 1], backgroundcolor="rgba(0,0,0,0)"),
                                          yaxis=dict(range=[-0.1, 1], backgroundcolor="rgba(0,0,0,0)"),
                                          zaxis=dict(range=[-0.1, 1], backgroundcolor="rgba(0,0,0,0)")))

        fig.update_layout(height=420, margin=dict(l=10, r=10, t=20, b=10))
        return fig
