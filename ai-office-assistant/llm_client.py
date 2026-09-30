"""Minimal LLM client wrapper around the Groq API.

This is intentionally the ONLY place in the project that talks to an
LLM provider. Every agent goes through the `call_llm()` function
below. There is no agent framework anywhere in this project -- an
"agent" is just a Python class with a system prompt (see
agents/base_agent.py), and "multi-agent orchestration" is just plain
Python functions calling those classes in a particular order (see
orchestrator.py).
"""

import os
from typing import Optional

from groq import Groq

# Lazily-created singleton client so importing this module doesn't
# require GROQ_API_KEY to already be set (it gets loaded from .env in
# main.py before any agent actually runs).
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
    """Send one chat completion request to Groq and return the reply text.

    Args:
        system_prompt: Defines the agent's role/persona/instructions.
        user_prompt: The specific input for this call.
        temperature: Sampling temperature (0 = deterministic, 1 = creative).

    Returns:
        The model's reply as a plain string, with leading/trailing
        whitespace stripped.
    """
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