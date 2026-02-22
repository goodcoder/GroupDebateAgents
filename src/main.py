from src.orchestrator import DebateOrchestrator
from src.config import ResponseLevel
import os
import sys
import asyncio
from dotenv import load_dotenv

# ── Debate Topic ───────────────────────────────────────────────────────────────
# Edit this freely. The debate will NOT auto-start when you save this file.
# You must run the script and confirm at the prompt below.
# SAMPLE_REQUIREMENT = (
#     "We need to migrate our monolith legacy banking application (which processes 10,000 Transactions Per Second) "
#     "to a microservices architecture on AWS. Create a 3-phase strategic high-level plan for how "
#     "we transition the database and handle user traffic without zero downtime."
# )

SAMPLE_REQUIREMENT = (
    "Our app receives millions of records on JMS Queue. Millions of JMS messages are arriving to one of the queue. Each message have 80% part which is basic parsing, but 20% is some Rest API call. so 20% part blocks remaining 80% part!"
    "How to process messages in parallel ( one-by-one or in batches!) for best performance? Assume, all messages are isolated, but many can belong to same ClientID and there may be duplicates!"
    "Create a robust architecture plan of how to architect this in a Springboot application deployed on On-premesis (PCF/Red Hat Openshift)."
)

async def main():
    load_dotenv()

    # Basic check to ensure the user has set the required environment variable
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY is not set in the environment.", file=sys.stderr)
        print("Please export it or add it to a .env file in the root directory.", file=sys.stderr)
        sys.exit(1)

    # ── FIX 2: Confirmation Gate ───────────────────────────────────────────────
    # Prevents the debate from auto-starting when this file is saved, imported,
    # or re-executed by an IDE. You must explicitly press ENTER to proceed.
    print("\n" + "=" * 62)
    print("  GROUP DEBATE AGENTS  —  AutoGen 0.4")
    print("=" * 62)
    print(f"\n  Topic:\n  {SAMPLE_REQUIREMENT[:120]}...\n")

    # ── Solutions & Rounds Selection ───────────────────────────────────────────
    try:
        ns_input = input("  How many initial solutions should the Consultant propose? (1-3) [Default: 1]: ").strip()
        num_solutions = int(ns_input) if ns_input.isdigit() else 1
        num_solutions = max(1, min(3, num_solutions))  # Clamp between 1-3
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(0)

    max_rounds = 8 if num_solutions > 1 else 6
    print(f"  → Generating {num_solutions} solution(s) in Round 1.")
    print(f"  → Max Rounds set to: {max_rounds}")

    # ── Response Level Selection ───────────────────────────────────────────────
    level_map = {
        "1": ResponseLevel.SIMPLE,
        "2": ResponseLevel.INTERMEDIATE,
        "3": ResponseLevel.ADVANCED,
        "4": ResponseLevel.EXPERT,
    }
    print("\n  Response Level:")
    print("    1) Simple       — headings + one paragraph only  [default]")
    print("    2) Intermediate — headings + up to 4 bullets")
    print("    3) Advanced     — thorough with trade-offs")
    print("    4) Expert       — exhaustive, deeply technical")
    try:
        choice = input("\n  Enter choice (1-4) or press ENTER for Simple: ").strip()
    except KeyboardInterrupt:
        print("\n\nAborted by user. No API calls were made.")
        sys.exit(0)
    response_level = level_map.get(choice, ResponseLevel.SIMPLE)
    print(f"  → Using response level: {response_level.value.upper()}\n")
    # Initialize the orchestrator
    orchestrator = DebateOrchestrator(
        requirement_topic=SAMPLE_REQUIREMENT,
        max_rounds=max_rounds,
        response_level=response_level,
        num_solutions=num_solutions
    )

    # Run the conversational loop (Async)
    await orchestrator.start_debate()

if __name__ == "__main__":
    # In AutoGen 0.4, everything must be run via the asyncio event loop
    asyncio.run(main())
