from ai_research_agent.persistence.db import alembic_sync_url


def test_asyncpg_url_becomes_psycopg() -> None:
    url = alembic_sync_url(
        "postgresql+asyncpg://research:research@localhost:5432/research"
    )
    assert url.startswith("postgresql+psycopg://")
