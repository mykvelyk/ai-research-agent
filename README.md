# AI Research & Monitoring Agent

Apache-2.0 open-source research and monitoring agent. Telegram is the initial interface.

The same codebase supports:

1. **Self-host** — run your own instance with your Telegram bot token and API keys (optional user allowlist).
2. **Hosted** — talk to the public bot; `/start` creates your account. Always-on; you do not need to run Docker.

Research, monitoring, and Telegram handlers are not wired yet. The repo currently has package layout, configuration, a health endpoint, and a worker stub.

## Requirements

- Python 3.12+
- Docker (optional; PostgreSQL via Compose)

## Setup

```text
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
pytest
```

On Unix, activate with `source .venv/bin/activate` and copy with `cp .env.example .env`.

Health process (no Telegram required):

```text
research-agent-interface
```

Then `GET http://127.0.0.1:8000/health`.

PostgreSQL and migrations:

```text
docker compose up postgres -d
alembic upgrade head
```

## License

Copyright 2026 ai-research-agent contributors.

Licensed under the [Apache License 2.0](LICENSE).
