from ai_research_agent.persistence.models import Base, QuotaUsage, User


TENANT_TABLES = frozenset(
    {"topics", "sources", "research_runs", "reports", "quota_usage"}
)


def test_tenant_tables_have_owner_id() -> None:
    for name, table in Base.metadata.tables.items():
        if name in TENANT_TABLES:
            assert "owner_id" in table.c, name


def test_users_identified_by_telegram() -> None:
    assert "telegram_user_id" in User.__table__.c
    assert User.__table__.c.telegram_user_id.unique


def test_run_logical_key_unique() -> None:
    names = {c.name for c in Base.metadata.tables["research_runs"].constraints}
    assert "uq_research_runs_logical_key" in names


def test_quota_unique_per_day() -> None:
    names = {c.name for c in QuotaUsage.__table__.constraints}
    assert "uq_quota_owner_day" in names
