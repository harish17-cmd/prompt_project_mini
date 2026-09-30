"""Agent 2: Tutor Agent.

Provides a clear, level-appropriate explanation of the student's
question, with a simple example.
"""

from app.agents.base_agent import BaseAgent

TUTOR_SYSTEM_PROMPT = """\
You are a patient, encouraging tutor. Explain concepts clearly and
simply, matching the student's stated level. Always include one short,
concrete example to illustrate the idea. Avoid unnecessary jargon; if
you must use a technical term, briefly define it. Keep your answer
focused and well-organized, using short paragraphs or bullet points.
"""


class TutorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Tutor Agent",
            system_prompt=TUTOR_SYSTEM_PROMPT,
            temperature=0.6,
        )

    def run(self, question: str, subject: str, level: str) -> str:
        prompt = (
            f"Subject: {subject}\n"
            f"Student level: {level}\n"
            f"Question: {question}\n\n"
            "Explain this clearly, with one simple example."
        )
        return super().run(prompt)
