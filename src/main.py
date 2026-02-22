from src.orchestrator import DebateOrchestrator
import os
import sys
import asyncio
from dotenv import load_dotenv

async def main():
    load_dotenv()
    # Basic check to ensure the user has set the required environment variable
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY is not set in the environment.", file=sys.stderr)
        print("Please export it or add it to a .env file in the root directory.", file=sys.stderr)
        sys.exit(1)

    # Example Topic
    # We choose something complex enough that requires scrutiny and logic
    sample_requirement = (
        "We need to migrate our monolith legacy banking application (which processes 10,000 Transactions Per Second) "
        "to a microservices architecture on AWS. Create a 3-phase strategic high-level plan for how "
        "we transition the database and handle user traffic without zero downtime."
    )
    
    # Initialize the orchestrator.
    # Set max turns to 6 (Consultant -> Arch -> Consultant -> Arch -> Consultant -> Arch)
    orchestrator = DebateOrchestrator(
        requirement_topic=sample_requirement,
        max_rounds=6
    )
    
    # Run the conversational loop (Async)
    await orchestrator.start_debate()

if __name__ == "__main__":
    # In AutoGen 0.4, everything must be run via the asyncio event loop
    asyncio.run(main())
