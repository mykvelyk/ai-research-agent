from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OwnerContext:
    """Tenant scope. Repositories must filter by telegram_user_id."""

    telegram_user_id: int
