"""Agent 1: Code Intent Classifier."""

from app.agents.base_agent import BaseAgent

CLASSIFY_SYSTEM_PROMPT = """\
You are a Code Assistant intent classifier. Read the user's request and
choose exactly one of these labels:

- explain_code: the user wants an explanation of existing code
- debug_code: the user wants help finding or fixing a bug
- improve_code: the user wants code improvement or refactoring suggestions
- general: any other developer question

Respond with ONLY the single label text (e.g. "explain_code"). Do not add
any punctuation, explanation, or extra words.
"""

VALID_INTENTS = {"explain_code", "debug_code", "improve_code", "general"}


class ClassifyAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Classify Agent",
            system_prompt=CLASSIFY_SYSTEM_PROMPT,
            temperature=0.0,
        )

    def run(self, request_text: str) -> str:
        raw = super().run(f"User request: \"{request_text}\"")
        label = raw.strip().lower().replace(" ", "_").strip(".")
        for intent in VALID_INTENTS:
            if intent in label:
                return intent
        return "general"
