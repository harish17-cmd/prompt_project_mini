"""Pydantic request/response models for the FastAPI endpoints.

Keeping these separate from main.py mirrors how a real production
FastAPI app is organized, and gives students a clear example of how
FastAPI validates request bodies and documents response shapes
automatically (visible at /docs).
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="The student's question or topic they need help with.",
        examples=["Can you explain what photosynthesis is?"],
    )
    subject: Optional[str] = Field(
        default="General",
        description="Subject area, e.g. Biology, Math, History.",
    )
    level: Optional[str] = Field(
        default="Beginner",
        description="Student's level: Beginner, Intermediate, or Advanced.",
    )


class AskResponse(BaseModel):
    intent: str = Field(..., description="Classified intent of the question.")
    explanation: str = Field(..., description="The tutor's explanation.")
    quiz: List[str] = Field(..., description="Practice questions to self-test.")
    notes: str = Field(..., description="Condensed revision notes.")