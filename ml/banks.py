"""
SarfAI V2 — Bank Catalog and Per-Bank Scoring

Based on real data scraped from bank.uz (March 2026).
"""
import numpy as np

# ── Bank catalog ─────────────────────────────────────────────────────────────
# Based on real data scraped from bank.uz (March 2026 session)

BANK_PRODUCTS = [
    # ── Microloans / Consumer ────────────────────────────────────────────────
    {
        "bank_id": 1,
        "bank_name": "Kapitalbank",
        "bank_slug": "kapitalbank",
        "product_name": "Mikroqarz",
        "loan_purpose": ["consumer", "computer_equipment", "education"],
        "rate_min": 24.0,
        "rate_max": 28.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 500_000,
        "max_term_months": 60,
        "min_term_months": 3,
        "collateral_required": False,
        "salary_project_banks": ["kapitalbank"],
        "score_modifier": +0.03,
        "notes": "Onlayn ariza, tez ko'rib chiqish",
    },
    {
        "bank_id": 2,
        "bank_name": "Hamkorbank",
        "bank_slug": "hamkorbank",
        "product_name": "Mikroqarz (Ta'minotli)",
        "loan_purpose": ["consumer", "business", "computer_equipment"],
        "rate_min": 25.99,
        "rate_max": 30.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 1,
        "collateral_required": False,
        "salary_project_banks": ["hamkorbank"],
        "score_modifier": +0.01,
        "notes": "",
    },
    {
        "bank_id": 3,
        "bank_name": "Hamkorbank",
        "bank_slug": "hamkorbank",
        "product_name": "Maosh loyihasi",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 22.0,
        "rate_max": 26.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 1,
        "collateral_required": False,
        "salary_project_banks": ["hamkorbank"],
        "employment_types_required": ["employed_state", "employed_private"],
        "score_modifier": +0.05,
        "notes": "Faqat maosh loyihasi mijozlari uchun",
    },
    {
        "bank_id": 4,
        "bank_name": "Ipoteka Bank",
        "bank_slug": "ipoteka_bank",
        "product_name": "Mikrokredit",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 24.0,
        "rate_max": 26.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 2_000_000,
        "max_term_months": 60,
        "min_term_months": 36,
        "collateral_required": False,
        "salary_project_banks": ["ipoteka_bank"],
        "score_modifier": +0.02,
        "notes": "Minimum muddat 36 oy",
    },
    {
        "bank_id": 5,
        "bank_name": "Xalq Banki",
        "bank_slug": "xalq_banki",
        "product_name": "Onlayn mikroqarz",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 25.0,
        "rate_max": 32.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 500_000,
        "max_term_months": 48,
        "min_term_months": 1,
        "collateral_required": False,
        "employment_types_preferred": ["employed_state"],
        "salary_project_banks": ["xalq_banki"],
        "score_modifier": +0.02,
        "notes": "Byudjet xodimlari uchun afzal",
    },
    {
        "bank_id": 6,
        "bank_name": "Ipak Yo'li Bank",
        "bank_slug": "ipak_yoli",
        "product_name": "Garov asosida kredit",
        "loan_purpose": ["consumer", "business", "auto"],
        "rate_min": 21.9,
        "rate_max": 24.9,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 60,
        "min_term_months": 12,
        "collateral_required": True,
        "salary_project_banks": ["ipak_yoli"],
        "score_modifier": +0.04,
        "notes": "Garov talab qilinadi — past stavka",
    },
    {
        "bank_id": 7,
        "bank_name": "Ipak Yo'li Bank",
        "bank_slug": "ipak_yoli",
        "product_name": "Maosh loyihasi",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 24.9,
        "rate_max": 27.9,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 12,
        "collateral_required": False,
        "employment_types_required": ["employed_state", "employed_private"],
        "salary_project_banks": ["ipak_yoli"],
        "score_modifier": +0.04,
        "notes": "Faqat maosh loyihasi",
    },
    {
        "bank_id": 8,
        "bank_name": "Asakabank",
        "bank_slug": "asakabank",
        "product_name": "Mikroqarz",
        "loan_purpose": ["consumer", "auto", "computer_equipment"],
        "rate_min": 24.0,
        "rate_max": 28.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 3,
        "collateral_required": False,
        "salary_project_banks": ["asakabank"],
        "score_modifier": +0.01,
        "notes": "",
    },
    {
        "bank_id": 9,
        "bank_name": "Orient Finans",
        "bank_slug": "orient_finans",
        "product_name": "Maosh loyihasi",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 22.0,
        "rate_max": 26.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 500_000,
        "max_term_months": 36,
        "min_term_months": 3,
        "collateral_required": False,
        "employment_types_required": ["employed_state", "employed_private"],
        "salary_project_banks": ["orient_finans"],
        "score_modifier": +0.04,
        "notes": "Maosh loyihasi — past stavka",
    },
    {
        "bank_id": 10,
        "bank_name": "NBU",
        "bank_slug": "nbu",
        "product_name": "Mikroqarz",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 24.0,
        "rate_max": 28.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 500_000,
        "max_term_months": 60,
        "min_term_months": 1,
        "collateral_required": False,
        "salary_project_banks": ["nbu"],
        "score_modifier": +0.02,
        "notes": "",
    },
    {
        "bank_id": 11,
        "bank_name": "MKBank",
        "bank_slug": "mkbank",
        "product_name": "Mikroqarz",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 25.0,
        "rate_max": 29.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 500_000,
        "max_term_months": 60,
        "min_term_months": 1,
        "collateral_required": False,
        "salary_project_banks": ["mkbank"],
        "score_modifier": +0.01,
        "notes": "",
    },
    {
        "bank_id": 12,
        "bank_name": "MKBank",
        "bank_slug": "mkbank",
        "product_name": "Byudjet xodimlari",
        "loan_purpose": ["consumer", "education", "computer_equipment"],
        "rate_min": 22.0,
        "rate_max": 26.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 500_000,
        "max_term_months": 60,
        "min_term_months": 1,
        "collateral_required": False,
        "employment_types_required": ["employed_state"],
        "salary_project_banks": ["mkbank"],
        "score_modifier": +0.05,
        "notes": "Byudjet xodimlari uchun maxsus",
    },
    {
        "bank_id": 13,
        "bank_name": "Trastbank",
        "bank_slug": "trastbank",
        "product_name": "Ta'lim/Sog'liqni saqlash",
        "loan_purpose": ["consumer", "education"],
        "rate_min": 22.0,
        "rate_max": 27.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 12,
        "collateral_required": False,
        "profession_categories_preferred": ["education", "healthcare"],
        "salary_project_banks": ["trastbank"],
        "score_modifier": +0.03,
        "notes": "O'qituvchi va tibbiyot xodimlariga qulay",
    },
    {
        "bank_id": 14,
        "bank_name": "Agrobank",
        "bank_slug": "agrobank",
        "product_name": "Qishloq xo'jaligi krediti",
        "loan_purpose": ["business", "consumer"],
        "rate_min": 14.0,
        "rate_max": 18.0,
        "max_loan_uzs": 200_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 6,
        "collateral_required": False,
        "employment_types_required": ["farmer", "self_employed", "entrepreneur"],
        "salary_project_banks": ["agrobank"],
        "score_modifier": +0.05,
        "notes": "Fermerlar uchun imtiyozli stavka",
    },
    # ── Mortgage ─────────────────────────────────────────────────────────────
    {
        "bank_id": 15,
        "bank_name": "Ipoteka Bank",
        "bank_slug": "ipoteka_bank",
        "product_name": "Ipoteka (birlamchi bozor)",
        "loan_purpose": ["mortgage"],
        "rate_min": 18.0,
        "rate_max": 22.0,
        "max_loan_uzs": 600_000_000,
        "min_loan_uzs": 50_000_000,
        "max_term_months": 240,
        "min_term_months": 60,
        "collateral_required": True,
        "down_payment_pct": 25.0,
        "salary_project_banks": ["ipoteka_bank"],
        "score_modifier": +0.02,
        "notes": "Boshlang'ich to'lov 25%",
    },
    {
        "bank_id": 16,
        "bank_name": "NBU",
        "bank_slug": "nbu",
        "product_name": "Qulay ipoteka",
        "loan_purpose": ["mortgage"],
        "rate_min": 18.5,
        "rate_max": 19.0,
        "max_loan_uzs": 800_000_000,
        "min_loan_uzs": 50_000_000,
        "max_term_months": 240,
        "min_term_months": 60,
        "collateral_required": True,
        "down_payment_pct": 25.0,
        "salary_project_banks": ["nbu"],
        "score_modifier": +0.03,
        "notes": "Boshlang'ich to'lov 25%",
    },
    {
        "bank_id": 17,
        "bank_name": "Xalq Banki",
        "bank_slug": "xalq_banki",
        "product_name": "O'qituvchilar ipotekasi",
        "loan_purpose": ["mortgage"],
        "rate_min": 14.0,
        "rate_max": 16.0,
        "max_loan_uzs": 400_000_000,
        "min_loan_uzs": 30_000_000,
        "max_term_months": 240,
        "min_term_months": 60,
        "collateral_required": True,
        "down_payment_pct": 5.0,
        "profession_categories_required": ["education"],
        "salary_project_banks": ["xalq_banki"],
        "score_modifier": +0.06,
        "notes": "Faqat o'qituvchilar uchun, boshlang'ich to'lov 5%",
    },
    {
        "bank_id": 18,
        "bank_name": "MKBank",
        "bank_slug": "mkbank",
        "product_name": "Arzon ipoteka (Mahalla)",
        "loan_purpose": ["mortgage"],
        "rate_min": 14.0,
        "rate_max": 16.0,
        "max_loan_uzs": 300_000_000,
        "min_loan_uzs": 20_000_000,
        "max_term_months": 240,
        "min_term_months": 60,
        "collateral_required": True,
        "down_payment_pct": 15.0,
        "salary_project_banks": ["mkbank"],
        "score_modifier": +0.04,
        "notes": "Mahalla tavsiyasi talab qilinadi",
    },
    {
        "bank_id": 19,
        "bank_name": "Agrobank",
        "bank_slug": "agrobank",
        "product_name": "Qishloq ipotekasi",
        "loan_purpose": ["mortgage"],
        "rate_min": 14.0,
        "rate_max": 17.0,
        "max_loan_uzs": 300_000_000,
        "min_loan_uzs": 20_000_000,
        "max_term_months": 240,
        "min_term_months": 60,
        "collateral_required": True,
        "down_payment_pct": 20.0,
        "employment_types_preferred": ["farmer"],
        "salary_project_banks": ["agrobank"],
        "score_modifier": +0.03,
        "notes": "Qishloq joylari uchun",
    },
    # ── Auto ─────────────────────────────────────────────────────────────────
    {
        "bank_id": 20,
        "bank_name": "Asakabank",
        "bank_slug": "asakabank",
        "product_name": "Avtokredit 2.5 (GM)",
        "loan_purpose": ["auto"],
        "rate_min": 5.5,
        "rate_max": 20.5,
        "max_loan_uzs": 1_000_000_000,
        "min_loan_uzs": 10_000_000,
        "max_term_months": 84,
        "min_term_months": 12,
        "collateral_required": True,
        "salary_project_banks": ["asakabank"],
        "score_modifier": +0.04,
        "notes": "GM UzAuto avtomobillari uchun maxsus",
    },
    {
        "bank_id": 21,
        "bank_name": "Ipak Yo'li Bank",
        "bank_slug": "ipak_yoli",
        "product_name": "Avtokredit (UzAuto Motors)",
        "loan_purpose": ["auto"],
        "rate_min": 16.99,
        "rate_max": 23.99,
        "max_loan_uzs": 950_000_000,
        "min_loan_uzs": 10_000_000,
        "max_term_months": 84,
        "min_term_months": 12,
        "collateral_required": True,
        "salary_project_banks": ["ipak_yoli"],
        "score_modifier": +0.03,
        "notes": "UzAuto Motors partnyori",
    },
    {
        "bank_id": 22,
        "bank_name": "Xalq Banki",
        "bank_slug": "xalq_banki",
        "product_name": "Avtokredit-Milliy",
        "loan_purpose": ["auto"],
        "rate_min": 24.0,
        "rate_max": 27.0,
        "max_loan_uzs": 600_000_000,
        "min_loan_uzs": 5_000_000,
        "max_term_months": 60,
        "min_term_months": 12,
        "collateral_required": True,
        "salary_project_banks": ["xalq_banki"],
        "score_modifier": +0.02,
        "notes": "",
    },
    # ── Business ─────────────────────────────────────────────────────────────
    {
        "bank_id": 23,
        "bank_name": "Hamkorbank",
        "bank_slug": "hamkorbank",
        "product_name": "Biznes kredit (KMKB)",
        "loan_purpose": ["business"],
        "rate_min": 22.0,
        "rate_max": 28.0,
        "max_loan_uzs": 500_000_000,
        "min_loan_uzs": 10_000_000,
        "max_term_months": 60,
        "min_term_months": 6,
        "collateral_required": True,
        "employment_types_required": ["entrepreneur", "self_employed", "business_owner"],
        "salary_project_banks": ["hamkorbank"],
        "score_modifier": +0.02,
        "notes": "Kichik va o'rta biznes",
    },
    {
        "bank_id": 24,
        "bank_name": "MKBank",
        "bank_slug": "mkbank",
        "product_name": "Yoshlar tadbirkorligi (pilot)",
        "loan_purpose": ["business"],
        "rate_min": 14.0,
        "rate_max": 14.0,
        "max_loan_uzs": 40_500_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 6,
        "collateral_required": False,
        "employment_types_required": ["entrepreneur", "self_employed"],
        "salary_project_banks": ["mkbank"],
        "score_modifier": +0.07,
        "notes": "Faqat 35 yoshgacha tadbirkorlar, 2025-2026 pilot",
    },
    {
        "bank_id": 25,
        "bank_name": "Xalq Banki",
        "bank_slug": "xalq_banki",
        "product_name": "HAMROKH (Ayol tadbirkorlar)",
        "loan_purpose": ["business", "consumer"],
        "rate_min": 22.0,
        "rate_max": 24.0,
        "max_loan_uzs": 100_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 36,
        "min_term_months": 6,
        "collateral_required": False,
        "gender_required": "female",
        "employment_types_required": ["entrepreneur", "self_employed"],
        "salary_project_banks": ["xalq_banki"],
        "score_modifier": +0.06,
        "notes": "Faqat ayol tadbirkorlar uchun, garovsiz",
    },
    # ── Education ────────────────────────────────────────────────────────────
    {
        "bank_id": 26,
        "bank_name": "MKBank",
        "bank_slug": "mkbank",
        "product_name": "Ta'lim krediti",
        "loan_purpose": ["education"],
        "rate_min": 14.0,
        "rate_max": 14.0,
        "max_loan_uzs": 50_000_000,
        "min_loan_uzs": 500_000,
        "max_term_months": 60,
        "min_term_months": 6,
        "collateral_required": False,
        "salary_project_banks": ["mkbank"],
        "score_modifier": +0.05,
        "notes": "Subsidiyalangan stavka",
    },
    # ── Green energy ─────────────────────────────────────────────────────────
    {
        "bank_id": 27,
        "bank_name": "Aloqabank",
        "bank_slug": "aloqabank",
        "product_name": "Yashil energiya krediti",
        "loan_purpose": ["green_energy"],
        "rate_min": 15.0,
        "rate_max": 20.0,
        "max_loan_uzs": 50_000_000,
        "min_loan_uzs": 1_000_000,
        "max_term_months": 60,
        "min_term_months": 6,
        "collateral_required": False,
        "salary_project_banks": ["aloqabank"],
        "score_modifier": +0.04,
        "notes": "Quyosh paneli va yashil texnologiyalar",
    },
]


def is_bank_eligible(product: dict, profile: dict) -> tuple[bool, list[str]]:
    """
    Check hard eligibility rules for a bank product.
    Returns (eligible: bool, reasons: list[str])
    """
    reasons = []

    # Loan purpose
    if profile.get("loan_purpose") not in product.get("loan_purpose", []):
        reasons.append(f"Kredit maqsadi mos emas ({profile.get('loan_purpose')})")

    # Loan amount
    loan = float(profile.get("loan_amount_requested_uzs", 0))
    if loan > product["max_loan_uzs"]:
        reasons.append(f"So'm miqdori haddan oshib ketgan (maks. {product['max_loan_uzs']:,})")
    if loan < product.get("min_loan_uzs", 0):
        reasons.append(f"So'm miqdori juda kam (min. {product.get('min_loan_uzs', 0):,})")

    # Loan term
    term = float(profile.get("loan_term_months", 0))
    if term > product["max_term_months"]:
        reasons.append(f"Muddat juda uzun (maks. {product['max_term_months']} oy)")
    if term < product.get("min_term_months", 0):
        reasons.append(f"Muddat juda qisqa (min. {product.get('min_term_months', 0)} oy)")

    # Collateral requirement
    if product.get("collateral_required") and not profile.get("has_collateral"):
        reasons.append("Garov talab qilinadi")

    # Employment type restriction
    req_emp = product.get("employment_types_required")
    if req_emp and profile.get("employment_type") not in req_emp:
        reasons.append(f"Ish turi mos emas (talab: {', '.join(req_emp)})")

    # Gender restriction (HAMROKH etc.)
    req_gender = product.get("gender_required")
    if req_gender and profile.get("gender") != req_gender:
        reasons.append("Jinsi mos emas")

    # Profession category restriction
    req_prof_cat = product.get("profession_categories_required")
    if req_prof_cat and profile.get("profession_category") not in req_prof_cat:
        reasons.append(f"Kasb toifasi mos emas (talab: {', '.join(req_prof_cat)})")

    # Credit history hard block
    if profile.get("credit_history_status") == "overdue":
        reasons.append("Muddati o'tgan qarz mavjud")

    return (len(reasons) == 0), reasons


def score_per_bank(
    global_prob: float,
    profile: dict,
    eligible_program_ids: list[str],
) -> list[dict]:
    """
    Compute per-bank approval scores.

    For each product:
    1. Check hard eligibility rules
    2. Apply bank-specific modifier
    3. Apply salary-bank bonus if applicable
    4. Apply special program bonus if applicable
    5. Clip to [0.02, 0.97]

    Returns list of bank score dicts, sorted by score descending.
    """
    results = []

    for product in BANK_PRODUCTS:
        eligible, reasons = is_bank_eligible(product, profile)

        # Base score
        score = global_prob + product["score_modifier"]

        # Salary bank bonus
        user_salary_bank = profile.get("salary_bank", "none")
        if user_salary_bank in product.get("salary_project_banks", []):
            score += 0.08

        # Special program bonus
        matched_programs = [
            pid for pid in eligible_program_ids
            if product["bank_slug"] in _program_bank_slugs(pid)
        ]
        if matched_programs:
            score += 0.07

        # Preferred employment bonus (softer than required)
        pref_emp = product.get("employment_types_preferred", [])
        if pref_emp and profile.get("employment_type") in pref_emp:
            score += 0.04

        # Preferred profession bonus
        pref_prof = product.get("profession_categories_preferred", [])
        if pref_prof and profile.get("profession_category") in pref_prof:
            score += 0.04

        # Ineligible products get a hard penalty
        if not eligible:
            score = min(score, 0.15)

        score = float(np.clip(score, 0.02, 0.97))

        # Recommended rate (midpoint, adjusted for program discount)
        rate = (product["rate_min"] + product["rate_max"]) / 2

        results.append({
            "bank_id":          product["bank_id"],
            "bank_name":        product["bank_name"],
            "bank_slug":        product["bank_slug"],
            "product_name":     product["product_name"],
            "score":            round(score, 3),
            "eligible":         eligible,
            "ineligible_reasons": reasons,
            "rate_min":         product["rate_min"],
            "rate_max":         product["rate_max"],
            "rate_midpoint":    round(rate, 2),
            "max_loan_uzs":     product["max_loan_uzs"],
            "max_term_months":  product["max_term_months"],
            "collateral_required": product.get("collateral_required", False),
            "matched_programs": matched_programs,
            "notes":            product.get("notes", ""),
        })

    results.sort(key=lambda x: (x["eligible"], x["score"]), reverse=True)
    return results


def _program_bank_slugs(program_id: str) -> list[str]:
    """Map program_id -> list of applicable bank slugs."""
    MAP = {
        "hamrokh":              ["xalq_banki"],
        "teacher_mortgage":     ["xalq_banki"],
        "youth_entrepreneur":   ["mkbank"],
        "mahalla_low_income":   ["mkbank"],
        "agriculture":          ["agrobank"],
        "rural_mortgage":       ["agrobank"],
        "budget_salary_project":["hamkorbank", "ipak_yoli", "orient_finans", "mkbank", "nbu"],
        "education_loan":       ["mkbank", "nbu", "xalq_banki"],
        "green_energy":         ["aloqabank"],
        "women_ifc":            ["ipak_yoli"],
    }
    return MAP.get(program_id, [])
