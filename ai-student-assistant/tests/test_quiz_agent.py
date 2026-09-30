import unittest
from unittest.mock import patch

from quiz_agent import QuizAgent


class QuizAgentTests(unittest.TestCase):
    def test_run_strips_numbering_and_returns_clean_questions(self) -> None:
        agent = QuizAgent()
        expected = [
            "What is photosynthesis?",
            "What does chlorophyll do?",
            "Where does it happen?",
            "Why is it important?",
        ]

        with patch("quiz_agent.BaseAgent.run", return_value="1. What is photosynthesis?\n2. What does chlorophyll do?\n3. Where does it happen?\n4. Why is it important?"):
            questions = agent.run("Photosynthesis is how plants make food.", "Biology", "Beginner")

        self.assertEqual(expected, questions)


if __name__ == "__main__":
    unittest.main()
