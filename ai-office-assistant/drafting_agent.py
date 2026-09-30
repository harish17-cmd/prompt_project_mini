"""Agent 2: Drafting Agent.

Takes the structured brief produced by the Intake Agent and writes
the first full draft of the requested content (email, report, memo,
etc.).
"""

from agents.base_agent import BaseAgent

DRAFTING_SYSTEM_PROMPT = """\
You are an Office Content Writer. You take a structured task brief
(task type, purpose, audience, key points, tone) and write a complete
first draft that satisfies it.

Rules:
- Match the requested Task Type's format exactly (e.g. an Email needs
  a Subject line and greeting; a Memo needs a header; a Report needs
  section headings).
- Cover every point listed under "Key Points" in the brief.
- Match the requested Tone.
- Write the full draft only -- no meta-commentary about what you did.
"""


class DraftingAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Drafting Agent",
            system_prompt=DRAFTING_SYSTEM_PROMPT,
            temperature=0.7,
        )

    def run(self, brief: str) -> str:
        prompt = (
            f"Here is the task brief:\n\n{brief}\n\n"
            "Write the full first draft now."
        )
        return super().run(prompt)
