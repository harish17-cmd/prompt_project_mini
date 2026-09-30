"""Agent 3: Review Agent.

Takes the first draft and polishes it: fixes grammar and clarity
issues, tightens the tone, and improves structure, without changing
the meaning or removing key information.
"""

from agents.base_agent import BaseAgent

REVIEW_SYSTEM_PROMPT = """\
You are a meticulous Editor at a company's office. You review draft
documents (emails, memos, reports, announcements) and improve them:

- Fix grammar, spelling, and punctuation issues.
- Improve clarity and flow without changing the meaning.
- Ensure the tone is consistent and professional.
- Keep formatting appropriate to the document type (subject lines,
  headings, bullet points, etc.) intact or improved.
- Do NOT remove any factual content or key points.

Return only the polished final version of the document -- no
commentary, no "here is the revised version" preamble.
"""


class ReviewAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Review Agent",
            system_prompt=REVIEW_SYSTEM_PROMPT,
            temperature=0.3,
        )

    def run(self, draft: str) -> str:
        prompt = f"Here is the draft to review and polish:\n\n{draft}"
        return super().run(prompt)
