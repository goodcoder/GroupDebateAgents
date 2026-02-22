from src.orchestrator import DebateOrchestrator
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
    "How to process messages in parallel ( or in batches) for best performance? Assume, all messages are isolated, but many can belong to same ClientID and there may be duplicates!"
    "Create a robust  architecture plan of how to architect this in Springboot application deployed on On-premesis PCF/Red Hat Openshift)"
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
    print(f"\n  Topic:\n  {SAMPLE_REQUIREMENT[:120]}...")
    print(f"\n  Max Rounds : 6")
    print("\n  Press ENTER to begin the debate, or Ctrl+C to abort.\n")
    try:
        input("  → ")
    except KeyboardInterrupt:
        print("\n\nAborted by user. No API calls were made.")
        sys.exit(0)

    # Initialize the orchestrator
    orchestrator = DebateOrchestrator(
        requirement_topic=SAMPLE_REQUIREMENT,
        max_rounds=6
    )

    # Run the conversational loop (Async)
    await orchestrator.start_debate()

if __name__ == "__main__":
    # In AutoGen 0.4, everything must be run via the asyncio event loop
    asyncio.run(main())
