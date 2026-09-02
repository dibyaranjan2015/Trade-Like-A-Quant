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

    def quiz(self) -> list:
        """
        Optional 3-question end-of-day check, each item:
        {"question": str, "options": [str, str, str, str],
         "correct": int (index into options), "explanation": str}
        Returns [] if a day hasn't defined one yet.
        """
        return []
