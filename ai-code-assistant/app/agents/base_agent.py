"""Base classes for AI Code Assistant agents."""

from app.llm_client import call_llm


class BaseAgent:
    def __init__(self, name: str, system_prompt: str, temperature: float = 0.7) -> None:
        self.name = name
        self.system_prompt = system_prompt
        self.temperature = temperature

    def run(self, user_prompt: str) -> str:
        print(f"  -> [{self.name}] thinking...")
        output = call_llm(self.system_prompt, user_prompt, self.temperature)
        print(f"  -> [{self.name}] done.")
        return output
