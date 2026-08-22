"""
core/day01_vectors.py
Day 1/40 — Vectors & Vector Operations (Linear Algebra, Week 1)
Pure logic + Plotly figure only — no Streamlit here. The UI lives in
pages/1_📐_Vectors.py and just calls this class.
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
    icon = "📐"

    def explain(self) -> str:
        return (
            "A vector is a magnitude + direction: v = [v1, v2, ..., vn].\n\n"
            "In quant finance, a portfolio's weights are a vector, e.g. "
            "w = [0.40, 0.35, 0.25] across 3 stocks.\n"
            "  • Vector ADDITION = combining two exposures\n"
            "  • SCALAR MULTIPLICATION = scaling a position up/down (leverage)\n"
            "  • NORM ‖v‖ = total magnitude of exposure / risk size\n\n"
            "This is the foundation every other pillar (matrices, covariance, "
            "PCA, portfolio optimization) is built on top of."
        )

    def compute(self, v=None, u=None):
        v = np.array(v if v is not None else [0.40, 0.35, 0.25], dtype=float)
        u = np.array(u if u is not None else [0.10, -0.05, -0.05], dtype=float)
        return {
            "v": v,
            "u": u,
            "v_plus_u": v + u,
            "norm_v": float(np.linalg.norm(v)),
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
                                    arrowsize=1.5, arrowwidth=3, arrowcolor=color)
                fig.add_trace(go.Scatter(x=[vec[0]], y=[vec[1]], mode="markers+text",
                                          marker=dict(size=1, color=color), text=[label],
                                          textposition="top center", showlegend=False))
            arrow(vec_v[:2], theme.LINEAR_ALGEBRA, "v")
            arrow(vec_u[:2], theme.QUANT_FINANCE, "u")
            arrow(vec_sum[:2], theme.PROBABILITY, "v+u")
            fig.update_layout(template="quant_dark",
                               xaxis=dict(range=[-1, 1], title="x"),
                               yaxis=dict(range=[-1, 1], title="y"))
        else:
            def arrow3d(vec, color, label):
                fig.add_trace(go.Scatter3d(x=[0, vec[0]], y=[0, vec[1]], z=[0, vec[2]],
                                            mode="lines+markers+text",
                                            line=dict(color=color, width=6),
                                            marker=dict(size=3, color=color),
                                            text=["", label]))
            arrow3d(vec_v, theme.LINEAR_ALGEBRA, "v")
            arrow3d(vec_u, theme.QUANT_FINANCE, "u")
            arrow3d(vec_sum, theme.PROBABILITY, "v+u")
            fig.update_layout(template="quant_dark", showlegend=False,
                               scene=dict(bgcolor=theme.DARK_BG,
                                          xaxis=dict(range=[-1, 1]),
                                          yaxis=dict(range=[-1, 1]),
                                          zaxis=dict(range=[-1, 1])))

        fig.update_layout(height=450, margin=dict(l=10, r=10, t=30, b=10))
        return fig


if __name__ == "__main__":
    concept = Vectors()
    result, fig = concept.demo()
    print("\nResult:", result)
