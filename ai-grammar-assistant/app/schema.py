"""Pydantic request/response models for the AI Grammar Assistant."""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    text: str = Field(
        ..., 
        min_length=1,
        description="The text to correct and improve.",
        examples=["This is a sentence with bad grammer."],
    )


class AskResponse(BaseModel):
    answer: str = Field(..., description="The corrected and improved text.")
