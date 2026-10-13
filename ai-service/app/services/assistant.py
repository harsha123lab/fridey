from app.actions.desktop import handle_desktop_command
from app.brain.ollama_client import OllamaClient
from app.brain.web_search import looks_time_sensitive, search_web
from app.core.config import settings


class AssistantService:
    def __init__(self) -> None:
        self.model = OllamaClient()

    async def process(self, user_text: str) -> dict[str, str]:
        text = user_text.strip()
        if not text:
            raise ValueError("Message cannot be empty")
        if settings.allow_desktop_actions:
            try:
                action_result = handle_desktop_command(text)
                if action_result:
                    return action_result
            except Exception:
                return {"action": "desktop_action", "reply": "That desktop action failed. Check the app or folder and try again."}
        context = search_web(text) if looks_time_sensitive(text) else ""
        reply = await self.model.chat(text, context=context)
        if looks_time_sensitive(text) and not context:
            reply += "\n\nNote: I couldn't retrieve fresh web results, so this answer may not reflect the latest information."
        return {"action": "chat", "reply": reply}
