# FRIDEY AI Service

First runnable Windows-focused version: local chat through Ollama, allowlisted desktop actions, optional DuckDuckGo snippets for current questions, and a separate microphone voice client.

## Requirements

- Windows 10/11 and Python 3.11 or 3.12
- Ollama installed and running
- Run `ollama pull qwen2.5:3b` once

## Install

Open Command Prompt in this folder:

1. `py -m venv .venv`
2. `\.venv\Scripts\activate`
3. `python -m pip install --upgrade pip`
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` if needed, then ensure `ollama list` includes `qwen2.5:3b`.

## Start

- Run `run_api.bat` or `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` from this folder.
- Test `http://127.0.0.1:8000/health`; API docs are at `http://127.0.0.1:8000/docs`.
- In a second terminal, run `run_voice.bat`. Say “Friday” or “Fridey”.

## Actions

Open Chrome, Notepad, Calculator, VS Code, File Explorer, Downloads; open YouTube; search Google; search YouTube; open a website using “open website example.com”; type exact text into the focused window using “type this: ...”. The type command types into whichever window currently has focus, so use carefully.

Actions use a fixed allowlist and never run arbitrary model-generated commands. Time-sensitive prompts trigger a best-effort DuckDuckGo search; if unavailable, FRIDEY warns that the answer may be outdated. Speech recognition uses Google's service and requires internet access. Text-to-speech uses Windows voices through pyttsx3.

Android, Spring backend integration, dashboard, persistent memory, always-on startup, offline speech recognition, and IoT controls are not implemented yet. Tests have been added but have not been run on a Windows machine.
