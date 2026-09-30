"""Orchestrates the AI Code Assistant workflow."""

from app.classify_agent import ClassifyAgent
from app.debug_agent import DebugAgent
from app.explain_agent import ExplainAgent
from app.improve_agent import ImproveAgent


class CodeAssistant:
    def __init__(self) -> None:
        self.classifier = ClassifyAgent()
        self.explainer = ExplainAgent()
        self.improver = ImproveAgent()
        self.debugger = DebugAgent()

    def run(self, request_text: str) -> dict[str, str]:
        intent = self.classifier.run(request_text)

        if intent == "explain_code":
            answer = self.explainer.run(request_text)
        elif intent == "debug_code":
            answer = self.debugger.run(request_text)
        elif intent == "improve_code":
            answer = self.improver.run(request_text)
        else:
            answer = self.explainer.run(request_text)

        return {
            "intent": intent,
            "answer": answer,
        }
