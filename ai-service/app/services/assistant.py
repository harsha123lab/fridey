from app.brain.ollama_client import OllamaClient


class AssistantService:
    """Orchestrates assistant requests; action execution stays separate."""

    def __init__(self) -> None:
        self.model = OllamaClient()

    async def respond(self, user_text: str) -> str:
        if not user_text.strip():
            raise ValueError("Message cannot be empty")
        return await self.model.chat(user_text.strip())
