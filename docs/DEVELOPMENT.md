# Development

From the ai-service directory in Windows PowerShell:

    py -m venv .venv
    .venv\\Scripts\\Activate.ps1
    pip install -r requirements.txt
    Copy-Item .env.example .env
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Install and start Ollama separately, then pull the configured model (default: qwen2.5:3b).

Run tests from ai-service with `pytest`. Health tests do not require Ollama. The /command endpoint requires Ollama and the configured model. Local .env files are ignored by Git.
