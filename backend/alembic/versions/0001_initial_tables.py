"""initial tables

Revision ID: 0001
Revises:
Create Date: 2026-03-13
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id",              sa.Integer(),     primary_key=True),
        sa.Column("username",        sa.String(64),    nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(128),   nullable=False),
        sa.Column("is_admin",        sa.Boolean(),     nullable=False, default=False),
        sa.Column("created_at",      sa.DateTime(),    nullable=False),
        sa.Column("last_active_at",  sa.DateTime(),    nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"])

    op.create_table(
        "financial_profiles",
        sa.Column("id",         sa.Integer(), primary_key=True),
        sa.Column("user_id",    sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("updated_at", sa.DateTime()),
        # Demographics
        sa.Column("age",              sa.Integer(), nullable=False),
        sa.Column("gender",           sa.String(10), nullable=False),
        sa.Column("region",           sa.String(64)),
        sa.Column("marital_status",   sa.String(20)),
        sa.Column("dependents_count", sa.Integer(), default=0),
        sa.Column("is_young_family",  sa.Boolean(), default=False),
        # Employment
        sa.Column("employment_type",        sa.String(32), nullable=False),
        sa.Column("profession_category",    sa.String(32)),
        sa.Column("profession_role",        sa.String(48)),
        sa.Column("salary_bank",            sa.String(32), default="none"),
        sa.Column("work_experience_months", sa.Integer(), default=0),
        # Income
        sa.Column("monthly_income_uzs",    sa.Float(), nullable=False),
        sa.Column("has_additional_income", sa.Boolean(), default=False),
        sa.Column("additional_income_uzs", sa.Float(), default=0),
        sa.Column("income_proof_type",     sa.String(32), default="none"),
        # Financial profile
        sa.Column("existing_debt_monthly_uzs", sa.Float(), default=0),
        sa.Column("credit_history_status",     sa.String(16), default="none"),
        sa.Column("has_collateral",            sa.Boolean(), default=False),
        sa.Column("collateral_type",           sa.String(20), default="none"),
        sa.Column("collateral_value_uzs",      sa.Float(), default=0),
        sa.Column("has_guarantor",             sa.Boolean(), default=False),
        sa.Column("savings_uzs",               sa.Float(), default=0),
        # Loan request
        sa.Column("loan_purpose",              sa.String(32)),
        sa.Column("loan_amount_requested_uzs", sa.Float()),
        sa.Column("loan_term_months",          sa.Integer()),
        sa.Column("preferred_currency",        sa.String(4), default="uzs"),
        # Special program flags
        sa.Column("is_student",              sa.Boolean(), default=False),
        sa.Column("is_mahalla_low_income",   sa.Boolean(), default=False),
        sa.Column("is_women_entrepreneur",   sa.Boolean(), default=False),
        sa.Column("is_youth_entrepreneur",   sa.Boolean(), default=False),
        sa.Column("is_farmer",               sa.Boolean(), default=False),
        sa.Column("teacher_qualification_category", sa.String(20), default="none"),
        sa.Column("teacher_experience_years",       sa.Integer(), default=0),
    )

    op.create_table(
        "predictions",
        sa.Column("id",         sa.Integer(), primary_key=True),
        sa.Column("user_id",    sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), index=True),
        sa.Column("global_prob",  sa.Float(), nullable=False),
        sa.Column("dti_ratio",    sa.Float(), nullable=False),
        sa.Column("approved",     sa.Integer(), nullable=False),
        sa.Column("loan_purpose",              sa.String(32)),
        sa.Column("loan_amount_requested_uzs", sa.Float()),
        sa.Column("loan_term_months",          sa.Integer()),
        sa.Column("monthly_income_uzs",        sa.Float()),
        sa.Column("employment_type",           sa.String(32)),
        sa.Column("credit_history_status",     sa.String(16)),
        sa.Column("top_bank_slug",             sa.String(32)),
        sa.Column("top_bank_score",            sa.Float()),
        sa.Column("programs_triggered",        sa.JSON()),
        sa.Column("eligible_bank_count",       sa.Integer(), default=0),
    )

    op.create_table(
        "bank_products",
        sa.Column("id",           sa.Integer(), primary_key=True),
        sa.Column("bank_name",    sa.String(64), nullable=False),
        sa.Column("bank_slug",    sa.String(32), nullable=False, index=True),
        sa.Column("product_name", sa.String(128), nullable=False),
        sa.Column("is_active",    sa.Boolean(), nullable=False, default=True),
        sa.Column("loan_purposes",   sa.JSON(), nullable=False),
        sa.Column("rate_min",        sa.Float(), nullable=False),
        sa.Column("rate_max",        sa.Float(), nullable=False),
        sa.Column("max_loan_uzs",    sa.Float(), nullable=False),
        sa.Column("min_loan_uzs",    sa.Float(), default=500_000),
        sa.Column("max_term_months", sa.Integer(), nullable=False),
        sa.Column("min_term_months", sa.Integer(), default=1),
        sa.Column("collateral_required",              sa.Boolean(), default=False),
        sa.Column("employment_types_required",        sa.JSON(), default=list),
        sa.Column("employment_types_preferred",       sa.JSON(), default=list),
        sa.Column("profession_categories_required",   sa.JSON(), default=list),
        sa.Column("profession_categories_preferred",  sa.JSON(), default=list),
        sa.Column("gender_required",                  sa.String(10)),
        sa.Column("salary_project_banks",             sa.JSON(), default=list),
        sa.Column("down_payment_pct",                 sa.Float()),
        sa.Column("score_modifier", sa.Float(), default=0.0),
        sa.Column("notes",          sa.String(256), default=""),
    )


def downgrade():
    op.drop_table("bank_products")
    op.drop_table("predictions")
    op.drop_table("financial_profiles")
    op.drop_table("users")
