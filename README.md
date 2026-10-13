# FRIDEY AI

FRIDEY is a personal assistant project built around a local Ollama model, with a Windows-first Python API and voice client.

## Start the AI service

1. Install Python 3.11 or 3.12 and Ollama.
2. In a terminal, download the model with `ollama pull qwen2.5:3b`.
3. Open the `ai-service` folder and follow [the AI service setup guide](ai-service/README.md).
4. Start `run_api.bat`, then test `http://127.0.0.1:8000/health`.
5. Start `run_voice.bat` in a second terminal and say “Friday”.

## Current v1 capabilities

- Local chat using Ollama and `qwen2.5:3b`
- Fixed, allowlisted Windows app and website actions
- Best-effort DuckDuckGo snippets for questions likely to need current information
- Speech recognition and text-to-speech through a separate voice client
- FastAPI health endpoint and command endpoint

## Important limitations

This is a working-code starting point, not a finished all-platform assistant. Online speech recognition needs internet access; current web search is best-effort. Persistent personal memory, automatic startup, offline wake-word detection, Android, dashboard, Java backend integration, and IoT controls are still future work. Code has been committed, but tests have not been run on the user's Windows computer.

See [architecture](docs/ARCHITECTURE.md) and [development notes](docs/DEVELOPMENT.md).
