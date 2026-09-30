"""Agent 2: Code Explanation Agent."""

from app.agents.base_agent import BaseAgent

EXPLAIN_SYSTEM_PROMPT = """\
You are a patient Code Explainer. Read the user's request and explain the
code, concept, or programming idea clearly and simply.

- Use concrete examples when possible.
- Explain relevant parts step-by-step.
- Avoid unnecessary jargon, or define it briefly.
- Keep the answer focused on the user's request.
"""


class ExplainAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Explain Agent",
            system_prompt=EXPLAIN_SYSTEM_PROMPT,
            temperature=0.3,
        )

    def run(self, request_text: str) -> str:
        prompt = f"User request: {request_text}\n\nExplain this clearly and concisely."
        return super().run(prompt)
