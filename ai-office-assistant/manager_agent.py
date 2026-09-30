"""Agent 4: Manager Agent.

Takes the final, polished document and produces a short executive
summary plus a clear list of action items / next steps, as a manager
skimming the final output would want.
"""

from agents.base_agent import BaseAgent

MANAGER_SYSTEM_PROMPT = """\
You are an Office Manager reviewing a finished document before it
goes out. Produce a short executive summary of the document plus a
list of concrete action items / next steps implied by it (who should
do what, if applicable).

Format your response in Markdown exactly like this:

## Executive Summary
<2-3 sentence summary>

## Action Items
- <action item 1>
- <action item 2>
(add as many as are genuinely implied, at least 1)
"""


class ManagerAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Manager Agent",
            system_prompt=MANAGER_SYSTEM_PROMPT,
            temperature=0.4,
        )

    def run(self, polished_document: str) -> str:
        prompt = f"Here is the finished document:\n\n{polished_document}"
        return super().run(prompt)
