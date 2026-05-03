import os
from agents.llm.openai_client import OpenAIClient
from agents.llm.ollama_client import OllamaClient

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "openai":
        return OpenAIClient()

    return OllamaClient()