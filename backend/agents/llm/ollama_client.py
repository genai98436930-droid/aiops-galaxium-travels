import httpx

class OllamaClient:
    def __init__(self, model="llama3"):
        self.model = model
        self.base_url = "http://localhost:11434"

    def chat(self, prompt: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json().get("response", "")