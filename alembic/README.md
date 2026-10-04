# Alembic

```text
docker compose up postgres -d
alembic upgrade head
```

`DATABASE_URL` in `.env` uses `postgresql+asyncpg://...`. Alembic converts it to `postgresql+psycopg://...`.
