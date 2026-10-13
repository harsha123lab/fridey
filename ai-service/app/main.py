from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator
from app.core.config import settings
from app.services.assistant import AssistantService

app = FastAPI(title=settings.app_name, version="1.0.0", description="FRIDEY local AI assistant API")
assistant = AssistantService()


class CommandRequest(BaseModel):
    text: str | None = Field(default=None, min_length=1, max_length=4000)
    command: str | None = Field(default=None, min_length=1, max_length=4000)

    @model_validator(mode="after")
    def require_text_or_command(self):
        if not (self.text or self.command):
            raise ValueError("Provide a non-empty 'text' or 'command' field")
        return self

    def user_text(self) -> str:
        return (self.text or self.command or "").strip()


class CommandResponse(BaseModel):
    assistant: str = "FRIDEY"
    action: str
    reply: str


@app.get("/")
async def root() -> dict[str, str]:
    return {"assistant": "FRIDEY", "service": settings.app_name, "status": "running"}


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {"status": "ok", "service": settings.app_name, "model": settings.ollama_model, "model_provider": "ollama", "web_search_enabled": settings.enable_web_search, "desktop_actions_enabled": settings.allow_desktop_actions}


@app.post("/command", response_model=CommandResponse)
async def command(request: CommandRequest) -> CommandResponse:
    try:
        result = await assistant.process(request.user_text())
    except Exception as exc:
        raise HTTPException(status_code=503, detail="FRIDEY couldn't get a response. Make sure Ollama is running and the configured model is installed.") from exc
    return CommandResponse(action=result["action"], reply=result["reply"])
