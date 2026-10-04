from ai_research_agent.adapters.http.app import create_app
from ai_research_agent.config import Settings
from ai_research_agent.observability import configure_logging


def main() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    import uvicorn

    uvicorn.run(
        create_app(),
        host=settings.http_host,
        port=settings.http_port,
    )
