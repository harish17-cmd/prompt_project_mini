"""Minimal LLM client wrapper around the Groq API.

Exactly like the office-workflow project, this is the ONLY place in
this app that talks to an LLM provider. FastAPI here is a *web*
framework (for exposing HTTP endpoints) -- it has nothing to do with
agent orchestration. There is still no agent framework: agents are
plain Python classes (see app/agents/base_agent.py) and orchestration
is a plain Python function (see app/orchestrator.py).
"""

import os
from typing import Optional

from groq import Groq

_client: Optional[Groq] = None


def _get_client() -> Groq:
    """Create (once) and return the Groq client."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and "
                "add your key before running this project."
            )
        _client = Groq(api_key=api_key)
    return _client


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Send one chat completion request to Groq and return the reply text."""
    client = _get_client()
    model = os.environ.get("MODEL", "llama-3.3-70b-versatile")

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()