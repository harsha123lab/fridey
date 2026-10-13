# FRIDEY AI Service

Windows-first assistant: Qwen via Vercel AI Gateway with local Ollama fallback, persistent memory, reminder storage, file understanding, optional WhatsApp Cloud API and SMTP email, responsive dashboard, desktop actions, best-effort current web search and voice.

## Setup
1. Install Python 3.11/3.12 and Ollama.
2. In this folder run `py -m venv .venv`, then `.venv\\Scripts\\activate`.
3. Run `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`; put secrets only in .env.
5. Run `ollama pull qwen2.5:3b` for fallback. Add `AI_GATEWAY_API_KEY=your_key` for cloud Qwen.
6. Run `run_api.bat`. Open http://127.0.0.1:8000/dashboard. API docs: http://127.0.0.1:8000/docs.
7. In a second terminal run `run_voice.bat` and say Friday/Fridey.

## Features
- **Persistent memory:** dashboard or POST /memory with `{"content":"I prefer simple English"}`; GET /memory; DELETE /memory/{id}. Say “Remember that I prefer simple English” or “What do you remember about me”. Stored in ai-service/data/fridey.db and survives restarts.
- **Reminders:** dashboard or POST /reminders with title and optional ISO-8601 due_at. GET /reminders; POST /reminders/{id}/complete. This version stores reminders but has no background scheduler/notification delivery yet.
- **Current facts:** best-effort DuckDuckGo search for time-sensitive questions; if search fails, FRIDEY refuses to guess. This is not a guarantee of correctness; verify important facts using reliable sources.
- **File understanding:** TXT, MD, CSV, JSON, LOG, PDF and DOCX. Scanned PDFs needing OCR are not supported. Document text is sent to configured AI provider; avoid sensitive documents unless acceptable.
- **WhatsApp:** requires Meta WhatsApp Cloud API token, phone number ID, and recipient opt-in. Configure WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID.
- **Email:** configure FRIDEY_SMTP_HOST, FRIDEY_SMTP_PORT, FRIDEY_SMTP_USERNAME, FRIDEY_SMTP_PASSWORD and FRIDEY_EMAIL_FROM. Prefer an app password. Sending occurs only when Send is clicked.
- **Offline voice:** default uses online Google speech recognition. Optional experimental offline mode: install `pip install vosk`, download/extract a Vosk model, set VOSK_MODEL_PATH and FRIDEY_OFFLINE_VOICE=true in local .env. Small English models may not understand Tamil/Thanglish reliably. TTS uses installed Windows voices.
- **Mobile/dashboard:** responsive web dashboard and manifest can be installed as a PWA from a supported browser, but this is not a native Android app. API stays on localhost by default; secure remote access/authentication is not implemented.

Do not expose this unauthenticated API publicly. Never commit API keys. Integrations need real provider credentials and have not been tested on your PC.
