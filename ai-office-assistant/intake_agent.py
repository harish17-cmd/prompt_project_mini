"""Agent 1: Intake Agent.

Takes a raw, possibly messy request from an employee and turns it
into a clear, structured task brief that the rest of the pipeline can
work from.
"""

from agents.base_agent import BaseAgent

INTAKE_SYSTEM_PROMPT = """\
You are an Office Intake Assistant. Your job is to read a raw request
from an employee and turn it into a short, structured task brief for
the rest of the office team to act on.

Your brief must include:
- Task Type: (e.g. Email, Report, Memo, Announcement, Meeting Notes)
- Purpose: one sentence on why this is needed
- Audience: who will read/receive this
- Key Points: a short bullet list of the essential information that
  MUST be included
- Tone: the appropriate tone (e.g. formal, friendly, urgent)

Be concise. Do not write the actual content yet -- only the brief.
"""


class IntakeAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Intake Agent",
            system_prompt=INTAKE_SYSTEM_PROMPT,
            temperature=0.3,
        )

    def run(self, raw_request: str) -> str:
        prompt = (
            f"Raw request from an employee:\n\n\"{raw_request}\"\n\n"
            "Produce the structured task brief described in your instructions."
        )
        return super().run(prompt)
