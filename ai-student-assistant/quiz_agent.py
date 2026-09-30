"""Agent 3: Quiz Agent.

Generates a short set of practice questions based on the tutor's
explanation, to help the student self-test their understanding.
"""

import re
from typing import List

from app.agents.base_agent import BaseAgent

QUIZ_SYSTEM_PROMPT = """\
You are a Quiz Generator for students. Given an explanation of a
concept, write exactly 4 short practice questions that test whether
the student understood it. Vary the difficulty slightly (start
easier, end harder).

Output format rules (strict):
- Output ONLY the 4 questions, nothing else.
- One question per line.
- Each line must start with "1. ", "2. ", "3. ", or "4. ".
- Do not include answers, headers, or any commentary.
"""


class QuizAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Quiz Agent",
            system_prompt=QUIZ_SYSTEM_PROMPT,
            temperature=0.7,
        )

    def run(self, explanation: str, subject: str, level: str) -> List[str]:
        prompt = (
            f"Subject: {subject}\n"
            f"Student level: {level}\n\n"
            f"Explanation the questions should test:\n{explanation}\n\n"
            "Write the 4 practice questions now, following the output "
            "format rules exactly."
        )
        raw = super().run(prompt)

        # Parse the numbered list into a clean list of strings. This
        # keeps the API response structured (a real List[str]) rather
        # than dumping raw text on the client.
        questions = []
        for line in raw.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            cleaned = re.sub(r"^\s*\d+[.)]\s*", "", stripped)
            questions.append(cleaned)
        return questions