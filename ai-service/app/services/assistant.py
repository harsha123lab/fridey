import logging, re
from app.actions.desktop import handle_desktop_command
from app.brain.ollama_client import OllamaClient
from app.brain.vercel_gateway_client import VercelGatewayClient
from app.brain.web_search import looks_time_sensitive, search_web
from app.core.config import settings
from app.services import store

logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self):
        self.local_model, self.cloud_model = OllamaClient(), VercelGatewayClient()

    async def process(self, user_text: str) -> dict[str, str]:
        text = user_text.strip()
        if not text: raise ValueError("Message cannot be empty")
        m = re.match(r"^(?:please )?remember that\s+(.+)$", text, re.I)
        if m:
            item = store.remember(m.group(1))
            return {"action":"memory_saved","reply":f"I saved this to memory: {item['content']}"}
        if re.fullmatch(r"(?:what do you remember about me|show my memories|list my memories)", text, re.I):
            items = store.list_memories()
            return {"action":"memory_list","reply":"Here is what I remember:\n" + "\n".join(f"- [ID {x['id']}] {x['content']}" for x in items[:20]) if items else "I have no saved memories yet. Say: remember that I prefer simple English."}
        m = re.match(r"^(?:please )?forget memory (\d+)$", text, re.I)
        if m:
            ok = store.forget(int(m.group(1)))
            return {"action":"memory_deleted","reply":"Memory deleted." if ok else "I couldn't find that memory ID."}
        if settings.allow_desktop_actions:
            try:
                action = handle_desktop_command(text)
                if action: return action
            except Exception:
                logger.exception("Desktop action failed")
                return {"action":"desktop_action","reply":"That desktop action failed. Check the app or folder and try again."}
        current = looks_time_sensitive(text)
        web_context = search_web(text) if current and settings.enable_web_search else ""
        if current and not web_context:
            return {"action":"current_fact_unverified","reply":"I couldn't verify this current fact from live search, so I won't guess. Please check a reliable up-to-date source and try again."}
        context = "\n\n".join(x for x in (web_context,store.memory_context()) if x)
        mode = settings.ai_provider.strip().lower()
        if mode not in {"auto","cloud","local"}: mode = "auto"
        if mode != "local" and self.cloud_model.is_configured:
            try: return {"action":"chat","reply":await self.cloud_model.chat(text,context=context),"provider":"vercel-ai-gateway"}
            except Exception as exc: logger.warning("Cloud failed; falling back to Ollama: %s",exc)
        try: return {"action":"chat","reply":await self.local_model.chat(text,context=context),"provider":"ollama"}
        except Exception as exc:
            logger.exception("Ollama failed")
            raise RuntimeError("FRIDEY could not reach its AI provider. Check Gateway credentials/network or start Ollama with the configured model.") from exc
