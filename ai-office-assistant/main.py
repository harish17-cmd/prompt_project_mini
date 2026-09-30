"""Main entry point for the AI Office Workflow.

Run the full pipeline from a raw employee request to an executive
summary.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

from dotenv import load_dotenv

from drafting_agent import DraftingAgent
from intake_agent import IntakeAgent
from llm_client import call_llm
from manager_agent import ManagerAgent
from review_agent import ReviewAgent


def run_workflow(raw_request: str) -> Dict[str, str]:
    """Run the office workflow end-to-end for a single request."""
    intake_agent = IntakeAgent()
    drafting_agent = DraftingAgent()
    review_agent = ReviewAgent()
    manager_agent = ManagerAgent()

    print("Starting workflow...")
    task_brief = intake_agent.run(raw_request)
    draft = drafting_agent.run(task_brief)
    polished_document = review_agent.run(draft)
    executive_summary = manager_agent.run(polished_document)

    return {
        "brief": task_brief,
        "draft": draft,
        "polished_document": polished_document,
        "executive_summary": executive_summary,
    }


def main() -> int:
    """Parse arguments and run the workflow or answer a direct question."""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Run the AI office workflow or ask a freeform question interactively."
    )
    parser.add_argument(
        "request",
        nargs="*",
        help="The question or office request to process. If omitted, you will be prompted to enter one."
    )
    parser.add_argument(
        "--workflow",
        action="store_true",
        help="Run the full office workflow instead of answering a question."
    )
    args = parser.parse_args()

    request_text = " ".join(args.request).strip()
    if not request_text:
        request_text = input("Enter your question: ").strip()

    if not request_text:
        print("No input provided. Exiting.")
        return 1

    if args.workflow:
        result = run_workflow(request_text)

        print("\n=== Task Brief ===")
        print(result["brief"])
        print("\n=== Draft ===")
        print(result["draft"])
        print("\n=== Polished Document ===")
        print(result["polished_document"])
        print("\n=== Executive Summary ===")
        print(result["executive_summary"])

        return 0

    answer = call_llm(
        "You are a helpful assistant. Answer the user's question clearly and concisely.",
        request_text,
        temperature=0.3,
    )
    print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
