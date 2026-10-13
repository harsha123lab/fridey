import logging

from app.actions.desktop import handle_desktop_command
from app.brain.ollama_client import OllamaClient
from app.brain.vercel_gateway_client import VercelGatewayClient
from app.brain.web_search import looks_time_sensitive, search_web
from app.core.config import settings

logger = logging.getLogger(__name__)


class AssistantService:
    def __init__(self) -> None:
        self.local_model = OllamaClient()
        self.cloud_model = VercelGatewayClient()

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
                logger.exception("Allowlisted desktop action failed")
                return {
                    "action": "desktop_action",
                    "reply": "That desktop action failed. Check the app or folder and try again.",
                }

        context = search_web(text) if settings.enable_web_search and looks_time_sensitive(text) else ""
        provider_mode = settings.ai_provider.strip().lower()
        if provider_mode not in {"auto", "cloud", "local"}:
            logger.warning("Unknown FRIDEY_AI_PROVIDER=%s; using auto", provider_mode)
            provider_mode = "auto"

        # Cloud-first when credentials are present. Any cloud error falls back
        # to local Ollama; local mode deliberately skips the cloud provider.
        if provider_mode != "local" and self.cloud_model.is_configured:
            try:
                reply = await self.cloud_model.chat(text, context=context)
                return {"action": "chat", "reply": reply, "provider": "vercel-ai-gateway"}
            except Exception as exc:
                logger.warning("Vercel AI Gateway failed; falling back to Ollama: %s", exc)

        try:
            reply = await self.local_model.chat(text, context=context)
            if looks_time_sensitive(text) and not context:
                reply += (
                    "\n\nNote: I couldn't retrieve fresh web results, so this answer "
                    "may not reflect the latest information."
                )
            return {"action": "chat", "reply": reply, "provider": "ollama"}
        except Exception as exc:
                logger.exception("Local Ollama fallback failed")
                if provider_mode != "local" and not self.cloud_model.is_configured:
                    detail = (
                        "No Vercel AI Gateway key is configured and local Ollama is "
                        "unavailable. Configure AI_GATEWAY_API_KEY or start Ollama."
                    )
                else:
                    detail = (
                        "Both the cloud request and local Ollama fallback failed. "
                        "Check your Vercel AI Gateway credentials/network and that "
                        "Ollama is running with the configured model."
                    )
                raise RuntimeError(detail) from exc
