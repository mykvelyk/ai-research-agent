from ai_research_agent.config import parse_allowlist


def is_allowed(telegram_user_id: int, raw_allowlist: str) -> bool:
    """FR2 / J7: empty allowlist is open; otherwise membership required."""
    allowed = parse_allowlist(raw_allowlist)
    if not allowed:
        return True
    return telegram_user_id in allowed
