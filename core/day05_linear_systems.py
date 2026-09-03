import numpy as np
import plotly.graph_objects as go

from core.base import QuantConcept
from core import theme


class LinearSystems(QuantConcept):
    name = "Systems of Linear Equations"
    day = 5
    pillar = "Linear Algebra"
    week = 1

    def content(self) -> dict:
        return {
            "tagline": "Multiple constraints, one unknown vector — solve them all at once.",
            "definition": (
                "A system of linear equations is a set of constraints that all have "
                "to be true at the same time — and matrix notation lets you write "
                "every single one of them as one equation, Ax = b, instead of a page "
                "of separate lines. Solving the system means finding the one vector "
                "x that satisfies every constraint simultaneously: the exact "
                "portfolio, the exact trade, the exact answer that makes every "
                "equation balance."
            ),
            "formulas": [
                ("A linear system, matrix form (Ex: Packing dozens of simultaneous trade rules into a single compact line)",
                 r"A\mathbf{x} = \mathbf{b}"),
                ("The augmented matrix (Ex: the compact way to write down every constraint and target at once, ready to solve)",
                 r"[A \mid \mathbf{b}]"),
                ("The unique solution, when it exists (Ex: the one portfolio that satisfies every constraint — solved directly)",
                 r"\mathbf{x} = A^{-1}\mathbf{b}, \quad \text{when } A \text{ is invertible}"),
                ("Consistency condition (Ex: is there one right portfolio, none at all, or a whole range of equally valid ones?)",
                 r"\text{rank}(A) = \text{rank}([A \mid \mathbf{b}]) \iff \text{a solution exists}"),
            ],
            "example": [
                ("text", "Say you want a two-stock portfolio that hits an exact 8% "
                          "target return, while staying fully invested (weights sum "
                          "to 1). Stock A returns 12%, Stock B returns 4%. That's two "
                          "constraints on two unknowns:"),
                ("latex", r"0.12\,w_A + 0.04\,w_B = 0.08 \qquad w_A + w_B = 1"),
                ("text", "Write it as a single matrix equation, Ax = b:"),
                ("latex", r"\begin{bmatrix} 0.12 & 0.04 \\ 1 & 1 \end{bmatrix}\begin{bmatrix} w_A \\ w_B \end{bmatrix} = \begin{bmatrix} 0.08 \\ 1 \end{bmatrix}"),
                ("text", "Solving this system gives you the one weighting that "
                          "satisfies both constraints at once:"),
                ("latex", r"w_A = 0.50, \quad w_B = 0.50"),
                ("text", "Half in each stock hits exactly 8% return, using every "
                          "dollar of capital — no guessing, no trial and error. "
                          "That's what solving a system of equations does: it finds "
                          "the one answer that makes every constraint true "
                          "simultaneously."),
            ],
            "application": (
                "Every time you need a portfolio that satisfies more than one exact "
                "requirement at once, you're solving a system of equations.</p>"
                "<ul>"
                "<li><strong>Target return + full investment</strong> = exactly "
                "today's example, two equations, two unknowns</li>"
                "<li><strong>Factor-neutral portfolios</strong> = solving for "
                "weights that hit zero exposure to several risk factors "
                "simultaneously</li>"
                "<li><strong>Hedging</strong> = solving for the exact hedge ratio "
                "that offsets a position's risk completely</li>"
                "</ul>"
                "<p><strong>The Bottom Line:</strong> Ax = b is one equation, but it "
                "can represent dozens of simultaneous constraints. Day 6 (matrix "
                "inverse) gives you the tool that actually solves it, and Day 7 "
                "(rank) tells you whether a solution exists at all."
            ),
        }

    def compute(self, target_return=0.08, return_a=0.12, return_b=0.04):
        A = np.array([[return_a, return_b], [1.0, 1.0]])
        b = np.array([target_return, 1.0])
        det = float(np.linalg.det(A))
        solvable = abs(det) > 1e-9
        if solvable:
            x = np.linalg.solve(A, b)
        else:
            x = np.array([np.nan, np.nan])
        return {
            "A": A, "b": b, "x": x, "det": det, "solvable": solvable,
            "w_a": float(x[0]), "w_b": float(x[1]),
            "target_return": target_return, "return_a": return_a, "return_b": return_b,
        }

    def visualize(self, target_return=0.08, return_a=0.12, return_b=0.04):
        r = self.compute(target_return, return_a, return_b)
        fig = go.Figure()

        w_range = np.linspace(-1.0, 2.0, 100)

        # Line 1: return_a * w_a + return_b * w_b = target_return
        if abs(return_b) > 1e-9:
            line1_y = (target_return - return_a * w_range) / return_b
            fig.add_trace(go.Scatter(x=w_range, y=line1_y, mode="lines",
                                      line=dict(color=theme.LINEAR_ALGEBRA, width=3),
                                      name="Target return constraint"))

        # Line 2: w_a + w_b = 1
        line2_y = 1.0 - w_range
        fig.add_trace(go.Scatter(x=w_range, y=line2_y, mode="lines",
                                  line=dict(color=theme.QUANT_FINANCE, width=3),
                                  name="Fully invested constraint"))

        if r["solvable"]:
            fig.add_trace(go.Scatter(x=[r["w_a"]], y=[r["w_b"]], mode="markers+text",
                                      marker=dict(size=14, color=theme.PROBABILITY,
                                                  line=dict(color=theme.TEXT_PRIMARY, width=2)),
                                      text=["Solution"], textposition="top center",
                                      textfont=dict(color=theme.PROBABILITY, size=13),
                                      name="Solution"))

        fig.update_layout(template="quant_dark",
                           xaxis=dict(range=[-0.6, 1.6], title="Stock A Weight"),
                           yaxis=dict(range=[-0.6, 1.6], title="Stock B Weight"),
                           height=440, margin=dict(l=10, r=10, t=20, b=10),
                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
        return fig

    def quiz(self) -> list:
        return [
            {
                "question": "A system of linear equations Ax = b has a unique solution when...",
                "options": ["A has more rows than columns", "A is invertible (has full rank)",
                            "b is the zero vector", "x is the identity matrix"],
                "correct": 1,
                "explanation": "When A is invertible, there's exactly one x that satisfies Ax = b — you can solve for it directly as x = A⁻¹b.",
            },
            {
                "question": "In the portfolio example, what do the two equations represent?",
                "options": ["Two different stocks' individual returns", "Two constraints the same portfolio must satisfy simultaneously",
                            "Two separate portfolios", "The determinant of A"],
                "correct": 1,
                "explanation": "One equation is the target-return constraint, the other is the fully-invested constraint — both apply to the exact same portfolio at once.",
            },
            {
                "question": "Writing several equations as one matrix equation Ax = b is useful because...",
                "options": ["It changes the answer", "It lets you solve dozens of simultaneous constraints with the same tools, regardless of how many there are",
                            "It only works for two equations", "It removes the need for a solution"],
                "correct": 1,
                "explanation": "The matrix form scales — whether you have 2 constraints or 200, Ax = b is solved the same way.",
            },
        ]
