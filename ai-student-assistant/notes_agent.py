"""Agent 4: Notes Agent.

Condenses the tutor's explanation into short, scannable revision
notes the student can review later.
"""

from app.agents.base_agent import BaseAgent

NOTES_SYSTEM_PROMPT = """\
You are a Study Notes Assistant. Given an explanation of a concept,
condense it into concise revision notes: 5 to 8 short bullet points
covering only the most important facts, definitions, and takeaways.
No introductions or conclusions -- bullet points only.
"""


class NotesAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Notes Agent",
            system_prompt=NOTES_SYSTEM_PROMPT,
            temperature=0.4,
        )

    def run(self, explanation: str) -> str:
        prompt = f"Explanation to condense into revision notes:\n\n{explanation}"
        return super().run(prompt)
