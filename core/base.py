"""
core/base.py
Shared interface for every daily QuantConcept class in the #ThefacelessQuant series.
No Streamlit imports here on purpose — core/ is pure logic, pages/ is UI only.
"""

from abc import ABC, abstractmethod


class QuantConcept(ABC):
    """Base class every daily concept implements."""

    name: str = "Unnamed Concept"
    day: int = 0
    pillar: str = ""          # "Linear Algebra" | "Calculus" | "Probability & Stats" | "Quant Finance"
    week: int = 0
    icon: str = "📊"           # used on Home.py cards + sidebar page label

    @abstractmethod
    def explain(self) -> str:
        """One-paragraph intuition + formula + why it matters. Doubles as IG caption."""
        raise NotImplementedError

    @abstractmethod
    def compute(self, *args, **kwargs):
        """Core math, run on real or synthetic market data. Returns a dict/result."""
        raise NotImplementedError

    @abstractmethod
    def visualize(self, *args, **kwargs):
        """Returns a Plotly figure, styled with the shared brand theme (core/theme.py)."""
        raise NotImplementedError

    def demo(self):
        """Quick local test: explain -> compute -> visualize (no Streamlit needed)."""
        print(f"Day {self.day}: {self.name}\n")
        print(self.explain())
        result = self.compute()
        fig = self.visualize()
        return result, fig
