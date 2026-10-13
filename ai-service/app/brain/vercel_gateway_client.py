import os

import httpx

from app.brain.prompts import SYSTEM_PROMPT, build_user_prompt
from app.core.config import settings


class VercelGatewayClient:
    """Qwen chat client for Vercel AI Gateway's OpenAI-compatible API."""

    def __init__(self) -> None:
        self.base_url = settings.vercel_gateway_base_url.rstrip("/")
        self.model = settings.vercel_model
        self.timeout = settings.request_timeout_seconds

    @property
    def api_key(self) -> str:
        # VERCEL_OIDC_TOKEN is available to supported Vercel deployments;
        # AI_GATEWAY_API_KEY is convenient for local development.
        return os.getenv("AI_GATEWAY_API_KEY", "").strip() or os.getenv(
            "VERCEL_OIDC_TOKEN", ""
        ).strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def chat(self, user_text: str, context: str = "") -> str:
        api_key = self.api_key
        if not api_key:
            raise RuntimeError("Vercel AI Gateway credentials are not configured")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(user_text, context)},
            ],
            "temperature": 0.3,
            "stream": False,
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        choices = data.get("choices", [])
        content = choices[0].get("message", {}).get("content") if choices else None
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Vercel AI Gateway returned an empty response")
        return content.strip()
