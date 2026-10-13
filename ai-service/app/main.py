from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.core.config import settings
from app.services.assistant import AssistantService

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="FRIDEY local AI assistant API",
)
assistant = AssistantService()


class CommandRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


class CommandResponse(BaseModel):
    assistant: str = "FRIDEY"
    action: str = "chat"
    reply: str


@app.get("/")
async def root() -> dict[str, str]:
    return {"assistant": "FRIDEY", "service": settings.app_name, "status": "running"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "model": settings.ollama_model,
        "model_provider": "ollama",
    }


@app.post("/command", response_model=CommandResponse)
async def command(request: CommandRequest) -> CommandResponse:
    try:
        reply = await assistant.respond(request.text)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="The assistant model is unavailable. Check Ollama and the configured model.",
        ) from exc
    return CommandResponse(reply=reply)
