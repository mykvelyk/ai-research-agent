"""Initial tenant-scoped schema.

Revision ID: 0001
Revises:
Create Date: 2026-10-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_user_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("telegram_user_id"),
    )
    op.create_index("ix_users_telegram_user_id", "users", ["telegram_user_id"])

    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=False, server_default=""),
        sa.Column("mode", sa.String(16), nullable=False, server_default="hybrid"),
        sa.Column("timezone", sa.String(64), nullable=False, server_default="UTC"),
        sa.Column("cadence", sa.String(16), nullable=False, server_default="daily"),
        sa.Column("paused", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_topics_owner_id", "topics", ["owner_id"])
    op.create_index("ix_topics_next_run_at", "topics", ["next_run_at"])

    op.create_table(
        "sources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("content_hash", sa.String(64), nullable=True),
        sa.Column("last_fetched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_sources_owner_id", "sources", ["owner_id"])
    op.create_index("ix_sources_topic_id", "sources", ["topic_id"])

    op.create_table(
        "research_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("public_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("topics.id", ondelete="CASCADE"), nullable=True),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("logical_key", sa.String(200), nullable=False),
        sa.Column("state", sa.String(16), nullable=False, server_default="scheduled"),
        sa.Column("notify_status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("question", sa.Text(), nullable=True),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("result_json", postgresql.JSONB(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("attempt", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("logical_key", name="uq_research_runs_logical_key"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index("ix_research_runs_owner_id", "research_runs", ["owner_id"])
    op.create_index("ix_research_runs_topic_id", "research_runs", ["topic_id"])
    op.create_index("ix_research_runs_state", "research_runs", ["state"])

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "run_id",
            sa.Integer(),
            sa.ForeignKey("research_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(300), nullable=False, server_default=""),
        sa.Column("summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("body_markdown", sa.Text(), nullable=False, server_default=""),
        sa.Column("model_json", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("run_id"),
    )
    op.create_index("ix_reports_owner_id", "reports", ["owner_id"])

    op.create_table(
        "quota_usage",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("utc_day", sa.Date(), nullable=False),
        sa.Column("one_shot_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("monitor_run_count", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("owner_id", "utc_day", name="uq_quota_owner_day"),
    )
    op.create_index("ix_quota_usage_owner_id", "quota_usage", ["owner_id"])


def downgrade() -> None:
    op.drop_table("quota_usage")
    op.drop_table("reports")
    op.drop_table("research_runs")
    op.drop_table("sources")
    op.drop_table("topics")
    op.drop_table("users")
