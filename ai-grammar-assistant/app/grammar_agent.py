"""Agent: Grammar & Writing Assistant."""

from app.agents.base_agent import BaseAgent

GRAMMAR_SYSTEM_PROMPT = """\
You are an expert English Grammar and Writing Assistant. Improve the user's
text by correcting grammar, punctuation, spelling, style, and clarity.

- Rewrite the text to be clear, natural, and professional.
- Preserve the original meaning.
- Fix all grammar mistakes and awkward phrasing.
- Provide the corrected text only, without explanation.
"""


class GrammarAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Grammar Agent",
            system_prompt=GRAMMAR_SYSTEM_PROMPT,
            temperature=0.2,
        )

    def run(self, text: str) -> str:
        prompt = f"Original text:\n{text}\n\nImprove and correct this text. Return only the corrected version."
        return super().run(prompt)
