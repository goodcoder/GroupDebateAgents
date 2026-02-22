import os
from enum import Enum
from dotenv import load_dotenv

# In AutoGen 0.4, we use the OpenAIChatCompletionClient for models 
# that offer OpenAI-compatible endpoint structures, including Gemini.
from autogen_ext.models.openai import OpenAIChatCompletionClient


# ── Response Verbosity Level ───────────────────────────────────────────────────
class ResponseLevel(Enum):
    """Controls how verbose / detailed the agents' responses are."""
    SIMPLE       = "simple"
    INTERMEDIATE = "intermediate"
    ADVANCED     = "advanced"
    EXPERT       = "expert"


# Shared formatting instruction injected into every agent at every level.
# Keeps output consistently structured as Markdown regardless of verbosity.
MARKDOWN_FORMAT_INSTRUCTION = (
    "FORMAT RULES (apply always): "
    "Format ALL your responses in clean Markdown. "
    "Use ## for main section headings (e.g. '## 🏗️ Architecture Overview'). "
    "Use ### for sub-sections. "
    "Use relevant emojis in headings (🏗️ 🔒 ⚡ 📦 🔄 🛡️ 📊 ⚠️ ✅ ❌ 🤔 🔍). "
    "Use **bold** for key terms. "
    "HIGHLIGHT RULE: Whenever you write ANY question or phrase that starts with 'What' "
    "(e.g. What If, What Is, What Will, What Happens, What About, What When), "
    "format that 'What' word using this EXACT HTML syntax: <mark>**What**</mark> "
    "so it stands out with bold + yellow highlight. Example: <mark>**What If**</mark> the queue fills up... then what? "
    "Never output plain unstructured text — always use headings and formatting."
)

# These strings are appended to each agent's system prompt at runtime.
RESPONSE_LEVEL_PROMPTS: dict[ResponseLevel, str] = {
    ResponseLevel.SIMPLE: (
        "RESPONSE STYLE — SIMPLE: "
        "Output ONLY main ## headings for each major topic section. "
        "Under EACH heading, write ONE short intro sentence then 3-5 concise bullet points. "
        "Prefix each bullet with a relevant icon (e.g. 🔄 ⚙️ ✅ 🔒 📦 ⚡ 🛡️ 🔍 📊). "
        "Each bullet must be ONE short line only — no run-on sentences. "
        "NO sub-bullets. NO numbered lists. NO ### sub-sections. "
        "Consultant: max 4 headings total. "
        "Architect: max 2 headings total, each with one short intro sentence and 3-5 bullet critiques. "
        "Each Architect section MUST end with a challenge question bullet starting with 'What' "
        "(e.g. What If, What Will, What Happens). Format it EXACTLY as: "
        "- <mark>**What ...**</mark> [your scenario/question]. "
        "Keep the overall response tight and scannable."
    ),
    ResponseLevel.INTERMEDIATE: (
        "RESPONSE STYLE — INTERMEDIATE: "
        "Use ## headings for each major section. "
        "Under each heading, use a short intro sentence then up to 4 bullet points max. "
        "Each bullet: one sentence only, no sub-bullets. "
        "Consultant: max 5 sections. "
        "Architect: max 3 critique sections with up to 3 bullets each. "
        "No lengthy prose paragraphs."
    ),
    ResponseLevel.ADVANCED: (
        "RESPONSE STYLE — ADVANCED: "
        "Use ## and ### headings to organise your response clearly. "
        "Consultant: up to 7 sections, each with bullet points, brief rationale, and trade-offs. "
        "Sub-bullets are allowed sparingly. "
        "Architect: up to 5 critique areas, each with impact analysis and follow-up questions. "
        "Short prose paragraphs are acceptable alongside lists."
    ),
    ResponseLevel.EXPERT: (
        "RESPONSE STYLE — EXPERT: "
        "Provide exhaustive, deeply technical responses with full depth. "
        "Consultant: cover all phases, alternatives, risk mitigations, edge cases, and technical specifics. "
        "Use nested sections and detailed sub-bullets. "
        "Architect: perform a rigorous red-team review covering security, scalability, resilience, "
        "cost, observability, and compliance. Use industry references and precise technical reasoning. "
        "No length restriction — completeness is the goal."
    ),
}

def get_llm_model_client() -> OpenAIChatCompletionClient:
    """
    Creates and returns the AutoGen 0.4 model client required by the agents.
    We configure it to use the Gemini model via its OpenAI-compatible API layer.
    """
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it in a .env file.")

    # In AutoGen 0.4, we instantiate a Client object instead of a config dictionary.
    # The 'google-genai' SDK maps Gemini 2.5 flash endpoints identically to standard completions.
    return OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        api_key=api_key,
        # Without base_url, AutoGen defaults to OpenAI's servers and rejects the Gemini key.
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        # AutoGen requires explicit model_info for any non-OpenAI model name.
        # Without this, it raises: "model_info is required when model name is not a valid OpenAI model"
        model_info={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        }
    )

