# FRIDEY Architecture

## Request flow

1. A voice interface, Android app, or web dashboard captures user input.
2. The client sends text to the FastAPI AI service.
3. The assistant service validates the request and calls the configured local Ollama model.
4. The reply is returned to the client.
5. Future desktop actions must pass through a trusted, validated action registry. Model output must never execute arbitrary shell commands.

## Components

- AI service: Python, FastAPI, Pydantic Settings, HTTPX.
- Local model: Ollama chat API, configured using environment variables.
- Speech: planned speech-to-text and text-to-speech adapters.
- Desktop actions: planned allowlisted handlers, isolated from model prompting.
- Spring backend: reserved for application APIs if needed.
- Android app and web dashboard: future user interfaces.
- Database: starter SQL schema; persistence is not connected yet.
- IoT firmware: future hardware integration.

## Security

Keep credentials in ignored .env files. Bind development services to loopback unless remote access is secured. Validate and limit inputs. Add authentication, authorization, audit logs, and user confirmation before exposing sensitive actions.
