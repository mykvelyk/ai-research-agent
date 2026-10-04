from datetime import UTC, datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    def now_utc(self) -> datetime: ...


@runtime_checkable
class Llm(Protocol):
    async def complete_json(self, *, system: str, user: str, data: str) -> dict: ...


@runtime_checkable
class Search(Protocol):
    async def search(self, query: str, *, max_results: int) -> list[str]: ...


@runtime_checkable
class Fetch(Protocol):
    async def get_text(self, url: str) -> str: ...


@runtime_checkable
class PdfRenderer(Protocol):
    def render_html(self, html: str) -> bytes: ...


class SystemClock:
    def now_utc(self) -> datetime:
        return datetime.now(UTC)
