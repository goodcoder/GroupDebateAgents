# AutoGen 0.4 uses autogen_agentchat for agent declarations
from autogen_agentchat.agents import AssistantAgent
from src.config import ResponseLevel, RESPONSE_LEVEL_PROMPTS, MARKDOWN_FORMAT_INSTRUCTION


class ConsultantAgent:
    """
    The Consultant serves as the Primary Planner. 
    They receive the initial requirement from the user, draft a comprehensive plan,
    and are responsible for revising that plan based on the Architect's adversarial feedback.
    """
    def __init__(self, model_client, response_level: ResponseLevel = ResponseLevel.ADVANCED):
        level_instruction = RESPONSE_LEVEL_PROMPTS[response_level.value]

        # System Message: This dictates the agent's behavior and personality.
        system_message = (
            "You are the Lead Technical Consultant and Planner. "
            "Your role is to receive requirements from the user and draft a comprehensive, strategic plan. "
            "When the Adversarial Architect reviews your plan and raises concerns, you MUST: "
            "1. Acknowledge valid points. "
            "2. Conduct necessary research or logical adjustments. "
            "3. Present a revised, strengthened version of the plan addressing the Architect's specific edge cases. "
            "Do not be stubborn; your goal is the highest quality final output."
            f"\n\n{MARKDOWN_FORMAT_INSTRUCTION}"
            f"\n\n{level_instruction}"
        )
        
        # Instantiate the new version 0.4 AssistantAgent
        self.agent = AssistantAgent(
            name="Consultant",
            system_message=system_message,
            model_client=model_client,
        )


class ArchitectAgent:
    """
    The Architect serves as the Critic (Red Team) — Adversarial by design.
    Their sole purpose is to find flaws in the Consultant's plan. They do not 
    write the plan themselves; they break it.
    """
    def __init__(self, model_client, response_level: ResponseLevel = ResponseLevel.ADVANCED):
        level_instruction = RESPONSE_LEVEL_PROMPTS[response_level.value]

        system_message = (
            "You are the Adversarial System Architect. "
            "Your ONLY goal is to brutally review the Consultant's plan. "
            "You must find critical flaws, dangerous assumptions, security risks, scalability bottlenecks, and edge cases. "
            "DO NOT write the code or construct the plan yourself. DO NOT be overly polite. "
            "You MUST challenge the plan using 'What' questions (What If, What Will, What Is, What Happens, etc.). "
            "Format EVERY question starting with 'What' using this EXACT markdown syntax: "
            "<mark>**What ...**</mark> [rest of question]. "
            "For example: <mark>**What If**</mark> the API is down? or <mark>**What Will**</mark> happen at 10x load? "
            "This highlight rule applies to ALL 'What*' terms — never skip it. "
            "Force the Consultant to defend their choices or revise the plan. "
            "TERMINATION RULE: When you are satisfied that all severe concerns have been addressed, "
            "OR when you have exhausted your objections, you MUST begin your final message with the "
            "EXACT phrase on its own line: 'I APPROVE THIS PLAN' — this signals the debate is over. "
            "Do not paraphrase it. Do not wrap it in quotes. Output it verbatim."
            f"\n\n{MARKDOWN_FORMAT_INSTRUCTION}"
            f"\n\n{level_instruction}"
        )
        
        # Instantiate the new version 0.4 AssistantAgent
        self.agent = AssistantAgent(
            name="Architect",
            system_message=system_message,
            model_client=model_client,
        )
