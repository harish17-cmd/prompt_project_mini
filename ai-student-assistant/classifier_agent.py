"""Agent 1: Classifier Agent.

Reads the student's raw question and classifies it into one of a
small set of known intents, so downstream agents (and the eventual
UI) know what kind of help is being requested.
"""

from app.agents.base_agent import BaseAgent

CLASSIFIER_SYSTEM_PROMPT = """\
You are a Question Classifier for a student assistant tool. Read the
student's question and classify it into EXACTLY ONE of these labels:

- concept_explanation: the student wants a concept, topic, or term explained
- practice_help: the student wants help solving a specific problem or exercise
- study_plan: the student wants help planning how/when to study
- general: anything else

Respond with ONLY the single label text (e.g. "concept_explanation").
Do not add punctuation, explanation, or any other words.
"""

VALID_INTENTS = {"concept_explanation", "practice_help", "study_plan", "general"}


class ClassifierAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Classifier Agent",
            system_prompt=CLASSIFIER_SYSTEM_PROMPT,
            temperature=0.0,
        )

    def run(self, question: str) -> str:
        raw = super().run(f"Student question: \"{question}\"")
        label = raw.strip().lower().replace(" ", "_").strip(".")

        # Defensive parsing: the model should return exactly one of
        # VALID_INTENTS, but in case it adds extra words, check for a
        # substring match before falling back to a safe default.
        for intent in VALID_INTENTS:
            if intent in label:
                return intent
        return "concept_explanation"
