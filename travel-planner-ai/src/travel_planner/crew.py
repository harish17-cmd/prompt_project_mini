"""Crew definition for the Travel Planner AI project.

This module wires together four collaborating agents and four
context-chained tasks using CrewAI's modern @CrewBase class-based
syntax, and configures the Groq-hosted llama-3.3-70b-versatile model
as the LLM used by every agent.

Pipeline:
    1. Destination Researcher      -> researches attractions/culture/weather
    2. Budget & Logistics Planner  -> budget breakdown + hotels + transport
    3. Itinerary Planner           -> day-by-day schedule (uses 1 + 2)
    4. Local Experience Consultant -> food/tips/packing + final report
                                       (uses 1 + 2 + 3)
"""

import os

from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class TravelPlannerCrew:
    """Travel Planner crew.

    Loads agent and task definitions from the YAML files in the
    `config` directory and assembles them into a runnable Crew made
    up of four specialized agents working in sequence.
    """

    # Paths to the YAML configuration files (relative to this file),
    # used automatically by the @CrewBase decorator.
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        # Read the Groq API key from the environment. python-dotenv
        # loads the .env file before this class is instantiated
        # (see main.py), so os.environ already contains the key here.
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Please add it to your .env "
                "file before running the crew."
            )

        # Allow the model name to be overridden via the environment,
        # but default to the required Groq model.
        model_name = os.environ.get("MODEL", "groq/llama-3.3-70b-versatile")

        # Configure the LLM that all agents in this crew will use.
        # CrewAI's LLM class uses LiteLLM under the hood, so the
        # "groq/" prefix routes the request to the Groq API.
        self.llm = LLM(
            model=model_name,
            api_key=groq_api_key,
            temperature=0.7,
        )

    # ------------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------------

    @agent
    def destination_researcher(self) -> Agent:
        """Researches attractions, culture, and weather for the destination."""
        return Agent(
            config=self.agents_config["destination_researcher"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def budget_logistics_planner(self) -> Agent:
        """Builds the budget breakdown and recommends hotels/transport."""
        return Agent(
            config=self.agents_config["budget_logistics_planner"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def itinerary_planner(self) -> Agent:
        """Builds the day-by-day itinerary from research + budget context."""
        return Agent(
            config=self.agents_config["itinerary_planner"],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def local_experience_consultant(self) -> Agent:
        """Adds food/tips/packing and compiles the final Markdown report."""
        return Agent(
            config=self.agents_config["local_experience_consultant"],
            llm=self.llm,
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    @task
    def research_destination(self) -> Task:
        """Task 1: gather destination research (no dependencies)."""
        return Task(
            config=self.tasks_config["research_destination"],
        )

    @task
    def plan_budget_and_stay(self) -> Task:
        """Task 2: budget + hote
