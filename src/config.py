import os
from dotenv import load_dotenv

# In AutoGen 0.4, we use the OpenAIChatCompletionClient for models 
# that offer OpenAI-compatible endpoint structures, including Gemini.
from autogen_ext.models.openai import OpenAIChatCompletionClient

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

