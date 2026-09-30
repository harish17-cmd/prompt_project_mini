"""FastAPI entry point for the AI Student Assistant.

This exposes the student-assistant workflow as a small web API.
"""

from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from classifier_agent import ClassifierAgent
from notes_agent import NotesAgent
from quiz_agent import QuizAgent
from schema import AskRequest, AskResponse
from tutor_agent import TutorAgent

load_dotenv()

app = FastAPI(
    title="AI Student Assistant",
    description="A FastAPI service that explains concepts, creates quiz questions, and summarizes notes.",
    version="1.0.0",
)

classifier_agent = ClassifierAgent()
tutor_agent = TutorAgent()
quiz_agent = QuizAgent()
notes_agent = NotesAgent()


def run_assistant_pipeline(request: AskRequest) -> AskResponse:
    """Run the full student-assistant workflow for one request."""
    subject = request.subject or "General"
    level = request.level or "Beginner"

    intent = classifier_agent.run(request.question)
    explanation = tutor_agent.run(request.question, subject, level)
    quiz = quiz_agent.run(explanation, subject, level)
    notes = notes_agent.run(explanation)

    return AskResponse(
        intent=intent,
        explanation=explanation,
        quiz=quiz,
        notes=notes,
    )


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "AI Student Assistant API is running"}


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    """Process a student question and return explanation, quiz, and notes."""
    try:
        return run_assistant_pipeline(request)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
