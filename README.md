# FRIDEY AI

FRIDEY is a Windows-first personal assistant using Qwen via Vercel AI Gateway and local Ollama fallback.

## Run locally
1. Install Python 3.11/3.12 and Ollama; run `ollama pull qwen2.5:3b`.
2. Follow [AI service setup](ai-service/README.md).
3. Add `AI_GATEWAY_API_KEY` to `ai-service/.env` for cloud Qwen. Never commit secrets.
4. Run `ai-service/run_api.bat`, then visit http://127.0.0.1:8000/dashboard.
5. Run `ai-service/run_voice.bat` in another terminal.

## Included
- Cloud Qwen and local Ollama fallback
- SQLite persistent memory
- Reminder storage/completion (no notifications yet)
- File Q&A for TXT, MD, CSV, JSON, LOG, PDF, DOCX
- Optional WhatsApp Cloud API and SMTP email
- Responsive mobile-friendly dashboard/PWA manifest
- Best-effort live web snippets; fail-closed when current facts cannot be verified
- Optional Vosk offline voice recognition

## Limits
No guaranteed current facts. WhatsApp/email require provider credentials. Offline voice requires a downloaded Vosk model and Thanglish recognition is not guaranteed. Reminders are stored but not scheduled/notified. Dashboard is not a native Android app; remote access/authentication is not included. Keep the local API private.
