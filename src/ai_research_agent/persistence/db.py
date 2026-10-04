from sqlalchemy.engine.url import make_url


def alembic_sync_url(async_url: str) -> str:
    """Alembic uses a sync driver; the app uses asyncpg."""
    url = make_url(async_url)
    if url.drivername.startswith("postgresql+asyncpg"):
        return str(url.set(drivername="postgresql+psycopg"))
    return async_url
