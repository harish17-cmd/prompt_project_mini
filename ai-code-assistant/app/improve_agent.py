"""Agent 3: Code Improvement Agent."""

from app.agents.base_agent import BaseAgent

IMPROVE_SYSTEM_PROMPT = """\
You are a Code Review Assistant. Read the user's request and suggest
improvements, refactorings, or best-practice changes to the code.

- Keep suggestions clear and actionable.
- Preserve the original behavior unless the user asks for a different outcome.
- Explain why each suggested change is helpful.
"""


class ImproveAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Improve Agent",
            system_prompt=IMPROVE_SYSTEM_PROMPT,
            temperature=0.4,
        )

    def run(self, request_text: str) -> str:
        prompt = f"User request: {request_text}\n\nProvide practical code improvement suggestions." 
        return super().run(prompt)
