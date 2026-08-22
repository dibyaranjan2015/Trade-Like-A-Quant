"""
core/base.py
Shared interface for every daily QuantConcept class. content() replaces the
old single-paragraph explain() — it returns separate sections (definition,
formulas, worked example, real-world use) so each page can render them as
distinct, well-typeset panels instead of a wall of text.
"""

from abc import ABC, abstractmethod


class QuantConcept(ABC):

    name: str = "Unnamed Concept"
    day: int = 0
    pillar: str = ""
    week: int = 0

    @abstractmethod
    def content(self) -> dict:
        """
        Returns:
        {
            "tagline": short one-line summary for nav cards,
            "definition": plain-language definition, 2-4 sentences,
            "formulas": [(label, latex_string), ...]  # latex without $ delimiters
            "example": a fully worked numeric example, with real figures,
            "application": how this shows up in real quant/trading work,
        }
        """
        raise NotImplementedError

    @abstractmethod
    def compute(self, *args, **kwargs):
        """Runs the underlying math on user-adjustable or default inputs."""
        raise NotImplementedError

    @abstractmethod
    def visualize(self, *args, **kwargs):
        """Returns a Plotly figure using the shared 'quant_dark' template."""
        raise NotImplementedError
