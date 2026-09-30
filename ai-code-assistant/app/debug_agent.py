"""Agent 4: Code Debugging Assistant."""

from app.agents.base_agent import BaseAgent

DEBUG_SYSTEM_PROMPT = """\
You are a Debugging Assistant. Read the user's request and help identify
and fix bugs in the code.

- Analyze the code and the problem description carefully.
- Explain the root cause of the bug.
- Provide a concise fix or debugging recommendation.
"""


class DebugAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Debug Agent",
            system_prompt=DEBUG_SYSTEM_PROMPT,
            temperature=0.3,
        )

    def run(self, request_text: str) -> str:
        prompt = f"User request: {request_text}\n\nPlease identify the bug and suggest a fix."
        return super().run(prompt)
