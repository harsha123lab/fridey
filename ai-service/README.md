# FRIDEY AI Service

Windows-first personal assistant with allowlisted desktop actions, optional fresh web-search snippets, voice input/output, and two Qwen providers: Vercel AI Gateway cloud Qwen first, then local Ollama as fallback.

## Requirements

- Windows 10/11 and Python 3.11 or 3.12
- Ollama installed and running for local fallback
- A Vercel AI Gateway API key for cloud Qwen (optional but recommended)
- Run `ollama pull qwen2.5:3b` once for the local model

## Install

Open Command Prompt in this folder:

1. `py -m venv .venv`
2. `.venv\Scripts\activate`
3. `python -m pip install --upgrade pip`
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` if needed.
6. For cloud Qwen, create an API key in the Vercel AI Gateway dashboard and add `AI_GATEWAY_API_KEY=your_key` to `.env`. Never commit the real key. On supported Vercel deployments, `VERCEL_OIDC_TOKEN` can be used instead.

## Provider behavior

- Default `FRIDEY_AI_PROVIDER=auto`: if a Gateway credential exists, FRIDEY tries Vercel AI Gateway model `alibaba/qwen-3-30b` first.
- If the cloud request fails (network, provider, rate limit, or credentials), FRIDEY logs the issue and tries local Ollama `qwen2.5:3b`.
- If no Gateway credential exists, FRIDEY uses local Ollama directly.
- Set `FRIDEY_AI_PROVIDER=local` to disable cloud calls and use only Ollama. `cloud` means cloud-first with local fallback.
- Change `FRIDEY_VERCEL_MODEL` to another Qwen model ID available in Vercel AI Gateway if desired. Gateway model IDs are provider-qualified, for example `alibaba/qwen-3-30b`.

## Start and test

- Run `run_api.bat` or `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` from this folder.
- Test `http://127.0.0.1:8000/health`; API docs are at `http://127.0.0.1:8000/docs`.
- In a second terminal, run `run_voice.bat`. Say “Friday” or “Fridey”.
- Example request: `curl -X POST http://127.0.0.1:8000/command -H "Content-Type: application/json" -d "{\"text\":\"Explain AI in simple English\"}"`

## Desktop actions and safety

Open Chrome, Notepad, Calculator, VS Code, File Explorer, Downloads; open YouTube; search Google; search YouTube; open a website using “open website example.com”; type exact text into the focused window using “type this: ...”. The type command types into whichever window currently has focus, so use carefully. Actions use a fixed allowlist and never run arbitrary model-generated commands.

Current-information questions use best-effort DuckDuckGo snippets. If fresh results cannot be retrieved, FRIDEY warns that the answer may be outdated. Speech recognition uses Google's service and requires internet access; text-to-speech uses Windows voices through pyttsx3.

## Important limitations

Cloud Qwen can answer from a hosted model but cannot directly open apps on your Windows PC by itself; desktop actions still run on the local Windows service. The cloud provider requires internet and may incur usage charges. Persistent personal memory, guaranteed real-time knowledge, Android, dashboard, Java backend integration, offline speech recognition, automatic startup, and IoT controls are not implemented yet. Tests have not been run on the user's Windows computer.
