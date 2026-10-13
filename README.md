# FRIDEY AI

FRIDEY is a personal AI assistant project designed for natural English and Thanglish input, local language-model responses, voice interaction, and carefully controlled desktop actions.

## Project layout

- `ai-service/` — Python FastAPI service and assistant logic.
- `backend/` — Java/Spring backend integration placeholder.
- `android-app/` — Android client placeholder.
- `web-dashboard/` — browser dashboard placeholder.
- `database/` — SQL schema and persistence notes.
- `iot-firmware/` — future device/firmware integration placeholder.
- `docs/` — architecture and development notes.

## Quick start: AI service

Requires Python 3.11+ and Ollama for local model responses.

From Windows PowerShell:

    cd ai-service
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Copy-Item .env.example .env
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Check `http://127.0.0.1:8000/health`; API docs are at `http://127.0.0.1:8000/docs`.

Configure Ollama in `ai-service/.env`. The default model is `qwen2.5:3b`.

## API

- `GET /` — service welcome.
- `GET /health` — API configuration status.
- `POST /command` — send text and receive an assistant reply.

Example request: `{"text":"Explain AI in simple words"}`.

## Status and safety

This is a starter scaffold, not a finished voice assistant. Voice capture, speech-to-text, text-to-speech, Android, dashboard, Spring backend, and desktop automation remain separate future tasks. Desktop actions must use an explicit allowlist and confirmations for sensitive actions. Never commit .env files, API keys, passwords, virtual environments, or personal data.
