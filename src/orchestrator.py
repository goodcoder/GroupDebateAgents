import traceback
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMessageTermination, MaxMessageTermination

from src.config import get_llm_model_client
from src.agents.debate_agents import (
    ConsultantAgent, 
    AdversarialArchitectAgent, 
)

class DebateOrchestrator:
    """
    This Orchestrator class ties the agents together using AutoGen 0.4's 
    `RoundRobinGroupChat` team primitive.
    """
    def __init__(self, requirement_topic: str, max_rounds: int = 6):
        self.topic = requirement_topic
        self.max_rounds = max_rounds
        
        # Instantiate the 0.4 Model Client
        self.model_client = get_llm_model_client()
        
        # Instantiate our custom agent wrapper classes
        self.consultant_wrapper = ConsultantAgent(self.model_client)
        self.architect_wrapper = AdversarialArchitectAgent(self.model_client)
        
        # Extract the underlying AutoGen 0.4 AssistantAgents
        self.consultant = self.consultant_wrapper.agent
        self.architect = self.architect_wrapper.agent

    async def start_debate(self):
        """
        Configures the GroupChat and initiates the continuous conversation loop entirely as an Async task.
        In AutoGen 0.4, most core systems are asynchronous.
        """
        print("\n" + "="*60)
        print("STARTING DEBATE ORCHESTRATION (AutoGen 0.4)")
        print(f"Topic: {self.topic}")
        print(f"Max Turns Allowed: {self.max_rounds}")
        print("="*60 + "\n")

        # 1. Define Termination Conditions (New to AutoGen 0.4)
        # Terminate if the Architect says they approve
        text_termination = TextMessageTermination("I APPROVE THIS PLAN")
        
        # Or terminate if we exceed the safety mechanism of max messages
        max_message_termination = MaxMessageTermination(max_messages=self.max_rounds)
        
        # Combine the conditions (OR logic)
        termination_condition = text_termination | max_message_termination

        # 2. Create the Team (GroupChat)
        # Using the RoundRobinGroupChat enforces sequential turn-taking natively
        team = RoundRobinGroupChat(
            participants=[self.consultant, self.architect],
            termination_condition=termination_condition
        )

        initial_prompt = (
            f"REQUIREMENT:\n{self.topic}\n\n"
            "Consultant, please draft the initial plan. "
            "Adversarial_Architect, review the plan completely once submitted and raise concerns if any. "
            "Consultant, revise based on the Architect's feedback."
        )

        # 3. Stream the interaction loop
        try:
            # We use `run_stream` to iterate over the responses as they occur
            async for message in team.run_stream(task=initial_prompt):
                
                # Check if it is a standard agent message or a state transition message
                if hasattr(message, "source") and hasattr(message, "content"):
                    print(f"\n[{message.source.upper()}]:\n{message.content}")
                else:
                    # Some internal state streaming payloads don't have those exact fields
                    pass
                    
        except Exception as e:
             print(f"Encountered an error in the debate structure: {e}")
             traceback.print_exc()
        finally:
             print("\n" + "="*60)
             print("DEBATE CONCLUDED")
             print("="*60 + "\n")
