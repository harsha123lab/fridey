from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="FRIDEY_", extra="ignore")
    app_name: str = "FRIDEY AI Service"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:3b"
    request_timeout_seconds: float = 90.0
    enable_web_search: bool = True
    allow_desktop_actions: bool = True


settings = Settings()
