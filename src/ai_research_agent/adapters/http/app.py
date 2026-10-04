from fastapi import FastAPI

from ai_research_agent import __version__


def create_app() -> FastAPI:
    app = FastAPI(title="ai-research-agent", version=__version__)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.post("/telegram/webhook")
    def telegram_webhook() -> dict[str, str]:
        # Wired in a later increment (secret check + application handlers).
        return {"status": "not_implemented"}

    return app
