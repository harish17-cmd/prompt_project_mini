"""Pydantic request/response models for the AI Code Assistant."""

from pydantic import BaseModel, Field, model_validator


class AskRequest(BaseModel):
    question: str = Field(
        default="",
        description="The user's code-related question or request.",
        examples=["Explain what this Python function does."],
    )
    url: str | None = Field(
        default=None,
        description="Optional URL to analyze alongside the question.",
        examples=["https://example.com"],
    )

    @model_validator(mode="after")
    def validate_content(self) -> "AskRequest":
        combined = " ".join(
            part for part in [self.question.strip(), self.url.strip() if self.url else ""] if part
        )
        if not combined:
            raise ValueError(
                "Please enter code, a programming-language-related request, or a URL."
            )
        return self


class AskResponse(BaseModel):
    intent: str = Field(..., description="Classified code assistant intent.")
    answer: str = Field(..., description="The assistant's response.")
