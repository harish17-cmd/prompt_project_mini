"""Orchestrates the AI Grammar Assistant workflow."""

from app.grammar_agent import GrammarAgent


class GrammarAssistant:
    def __init__(self) -> None:
        self.grammar_agent = GrammarAgent()

    def run(self, text: str) -> dict[str, str]:
        corrected = self.grammar_agent.run(text)
        return {
            "answer": corrected,
        }
