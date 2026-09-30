"""Base class for every agent in this project.

This is the entire "agent framework" -- about 20 lines. An agent is
just a name, a system prompt that defines its persona/role, and a
`run()` method that sends a prompt to the LLM. Subclasses override
`run()` to shape their specific input into a good prompt, but they
all ultimately call `super().run(prompt)` to actually talk to the
model via llm_client.call_llm().
"""

from llm_client import call_llm


class BaseAgent:
    def __init__(self, name: str, system_prompt: str, temperature: float = 0.7) -> None:
        self.name = name
        self.system_prompt = system_prompt
        self.temperature = temperature

    def run(self, user_prompt: str) -> str:
        """Send `user_prompt` to the LLM using this agent's persona.

        Subclasses typically override this method to accept more
        specific arguments, build a tailored prompt string, and then
        call `super().run(prompt)` to perform the actual LLM call.
        """
        print(f"  -> [{self.name}] thinking...")
        output = call_llm(self.system_prompt, user_prompt, self.temperature)
        print(f"  -> [{self.name}] done.")
        return output
    
    