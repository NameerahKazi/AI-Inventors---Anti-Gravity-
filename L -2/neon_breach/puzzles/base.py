"""
Abstract Base Class for NEON BREACH Puzzles
"""
from abc import ABC, abstractmethod

class Puzzle(ABC):
    def __init__(self, difficulty: str = "CYBERPUNK"):
        self.difficulty = difficulty
        self.title = "GENERIC PUZZLE"
        self.description = ""
        self.solution = ""
        self.hints = []

    @abstractmethod
    def generate(self):
        """Generate random puzzle components based on difficulty."""
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        """Return formatted prompt for the terminal interface."""
        pass

    @abstractmethod
    def evaluate(self, user_input: str) -> bool:
        """Check if user submission matches solution."""
        pass

    def get_hint(self, level: int = 1) -> str:
        """Get progressive hint based on level (1, 2, or 3)."""
        idx = max(0, min(level - 1, len(self.hints) - 1))
        if self.hints:
            return self.hints[idx]
        return "No diagnostic data available for this puzzle."

    def get_explanation(self) -> str:
        """Return solution explanation for post-attempt feedback."""
        return f"Correct solution payload was: {self.solution}"
