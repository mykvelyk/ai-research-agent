from ai_research_agent.identity.allowlist import is_allowed


def test_empty_allowlist_is_open() -> None:
    assert is_allowed(1, "") is True
    assert is_allowed(1, "  ") is True


def test_allowlist_membership() -> None:
    raw = "100, 200"
    assert is_allowed(100, raw) is True
    assert is_allowed(200, raw) is True
    assert is_allowed(300, raw) is False
