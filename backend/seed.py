"""
SarfAI V2 — Database Seeder

Run once after alembic upgrade head:
    python seed.py

Creates:
  - All 27 bank products in bank_products table
  - An admin user (credentials from .env or defaults)
"""
from ml.banks import BANK_PRODUCTS as ML_BANK_PRODUCTS
from app.services.auth import hash_password
from app.database import Base
from app.models import User, FinancialProfile, Prediction, BankProduct
from app.database import engine, SessionLocal
from dotenv import load_dotenv
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

load_dotenv()


# Import the hardcoded bank catalog from ML module
ML_DIR = os.path.join(os.path.dirname(__file__), "ml")
sys.path.insert(0, ML_DIR)


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")


def seed_banks(db):
    existing = db.query(BankProduct).count()
    if existing > 0:
        print(f"  Bank products already seeded ({existing} rows) — skipping")
        return

    for bp in ML_BANK_PRODUCTS:
        product = BankProduct(
            bank_name=bp["bank_name"],
            bank_slug=bp["bank_slug"],
            product_name=bp["product_name"],
            is_active=True,
            loan_purposes=bp.get("loan_purpose", []),
            rate_min=bp["rate_min"],
            rate_max=bp["rate_max"],
            max_loan_uzs=bp["max_loan_uzs"],
            min_loan_uzs=bp.get("min_loan_uzs", 500_000),
            max_term_months=bp["max_term_months"],
            min_term_months=bp.get("min_term_months", 1),
            collateral_required=bp.get("collateral_required", False),
            employment_types_required=bp.get("employment_types_required", []),
            employment_types_preferred=bp.get(
                "employment_types_preferred", []),
            profession_categories_required=bp.get(
                "profession_categories_required", []),
            profession_categories_preferred=bp.get(
                "profession_categories_preferred", []),
            gender_required=bp.get("gender_required"),
            salary_project_banks=bp.get("salary_project_banks", []),
            down_payment_pct=bp.get("down_payment_pct"),
            score_modifier=bp.get("score_modifier", 0.0),
            notes=bp.get("notes", ""),
        )
        db.add(product)

    db.commit()
    print(f"✓ Seeded {len(ML_BANK_PRODUCTS)} bank products")


def seed_admin(db):
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "fadmin@2026")

    existing = db.query(User).filter(User.username == admin_username).first()
    if existing:
        print(f"  Admin user '{admin_username}' already exists — skipping")
        return

    from datetime import datetime
    admin = User(
        username=admin_username,
        hashed_password=hash_password(admin_password),
        is_admin=True,
        created_at=datetime.utcnow(),
        last_active_at=datetime.utcnow(),
    )
    db.add(admin)
    db.commit()
    print(f"✓ Admin user created: username='{admin_username}'")
    print(f"  Password: '{admin_password}' — CHANGE THIS IN PRODUCTION")


def main():
    print("\n── SarfAI V2 Database Seed ──────────────────────────")
    create_tables()

    db = SessionLocal()
    try:
        seed_banks(db)
        seed_admin(db)
    finally:
        db.close()

    print("── Done ─────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
