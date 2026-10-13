import httpx

from app.core.config import settings

SYSTEM_PROMPT = (
    "You are FRIDEY, a helpful personal AI assistant. "
    "Understand natural English and Tamil-English mixed speech (Thanglish) where possible. "
    "Reply clearly in the style the user uses. "
    "Never claim a computer action happened unless a trusted action handler confirms it. "
    "Never execute model-generated shell commands."
)


class OllamaClient:
    def __init__(self) -> None:
        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.ollama_model
        self.timeout = settings.request_timeout_seconds

    async def chat(self, user_text: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()

        content = data.get("message", {}).get("content")
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Ollama returned an empty response")
        return content.strip()
