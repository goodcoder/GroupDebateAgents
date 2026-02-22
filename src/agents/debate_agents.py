# AutoGen 0.4 uses autogen_agentchat for agent declarations
from autogen_agentchat.agents import AssistantAgent

class ConsultantAgent:
    """
    The Consultant serves as the Primary Planner. 
    They receive the initial requirement from the user, draft a comprehensive plan,
    and are responsible for revising that plan based on the Architect's adversarial feedback.
    """
    def __init__(self, model_client):
        # System Message: This dictates the agent's behavior and personality.
        system_message = (
            "You are the Lead Technical Consultant and Planner. "
            "Your role is to receive requirements from the user and draft a comprehensive, strategic plan. "
            "When the Adversarial Architect reviews your plan and raises concerns, you MUST: "
            "1. Acknowledge valid points. "
            "2. Conduct necessary research or logical adjustments. "
            "3. Present a revised, strengthened version of the plan addressing the Architect's specific edge cases. "
            "Do not be stubborn; your goal is the highest quality final output."
        )
        
        # Instantiate the new version 0.4 AssistantAgent
        self.agent = AssistantAgent(
            name="Consultant",
            system_message=system_message,
            model_client=model_client,
        )

class AdversarialArchitectAgent:
    """
    The Adversarial Architect serves as the Critic (Red Team).
    Their sole purpose is to find flaws in the Consultant's plan. They do not 
    write the plan themselves; they break it.
    """
    def __init__(self, model_client):
        system_message = (
            "You are the Adversarial System Architect. "
            "Your ONLY goal is to brutally review the Consultant's plan. "
            "You must find critical flaws, dangerous assumptions, security risks, scalability bottlenecks, and edge cases. "
            "DO NOT write the code or construct the plan yourself. DO NOT be overly polite. "
            "Ask aggressive 'What if [X happens]... Then what?' questions. "
            "Force the Consultant to defend their choices or revise the plan. "
            "If the Consultant has successfully mitigated ALL your severe concerns in their revised plan, "
            "you must explicitly state 'I APPROVE THIS PLAN'. "
            "If you cannot mitigate the Consultant's points, you must explicitly state 'I APPROVE THIS PLAN'."
        )
        
        # Instantiate the new version 0.4 AssistantAgent
        self.agent = AssistantAgent(
            name="Adversarial_Architect",
            system_message=system_message,
            model_client=model_client,
        )
