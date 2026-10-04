from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment configuration. Secrets stay in the environment, not in code."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://research:research@localhost:5432/research"

    allowed_telegram_user_ids: str = ""

    telegram_bot_token: str = ""
    telegram_webhook_secret: str = ""
    telegram_mode: str = "polling"

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    tavily_api_key: str = ""

    http_host: str = "0.0.0.0"
    http_port: int = 8000


def parse_allowlist(raw: str) -> frozenset[int]:
    """Empty string means open registration. Otherwise Telegram user ids."""
    if not raw.strip():
        return frozenset()
    return frozenset(int(part.strip()) for part in raw.split(",") if part.strip())
