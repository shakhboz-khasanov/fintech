"""
SarfAI V2 — Special Program Eligibility Detection

Each program returns a dict with:
  - eligible: bool
  - program_name: str (Uzbek display name)
  - benefit: str (human-readable benefit)
  - applicable_banks: list[str]
  - rate_discount_pct: float (reduction vs standard rate)
  - max_loan_uzs: int | None
"""

def check_all_programs(profile: dict) -> list[dict]:
    """
    Run all program checks and return a list of eligible programs.
    """
    results = []
    for checker in ALL_PROGRAMS:
        result = checker(profile)
        if result["eligible"]:
            results.append(result)
    return results


# ── Individual program checkers ──────────────────────────────────────────────

def check_hamrokh(p: dict) -> dict:
    """
    HAMROKH — Women entrepreneurs, unsecured up to 100M UZS, rate -2%.
    Launched May 2025 by Xalq Banki.
    """
    eligible = (
        p.get("gender") == "female"
        and p.get("employment_type") in ("entrepreneur", "self_employed")
        and p.get("loan_amount_requested_uzs", 0) <= 100_000_000
        and p.get("loan_purpose") in ("business", "consumer")
    )
    return {
        "eligible": eligible,
        "program_id": "hamrokh",
        "program_name": "HAMROKH dasturi",
        "benefit": "Garovsiz 100M UZS gacha, stavka -2% chegirma",
        "applicable_banks": ["xalq_banki"],
        "rate_discount_pct": 2.0,
        "max_loan_uzs": 100_000_000,
        "collateral_required": False,
    }


def check_teacher_mortgage(p: dict) -> dict:
    """
    O'qituvchilar ipotekasi — Teachers top-category + 15yrs get
    25% mortgage down-payment reduction. Xalq Banki, 14-16%.
    """
    is_teacher = p.get("profession_role") in (
        "teacher", "professor_lecturer", "school_principal", "vocational_trainer"
    )
    top_cat = p.get("teacher_qualification_category") == "top_category"
    exp_ok = p.get("teacher_experience_years", 0) >= 15
    purpose_ok = p.get("loan_purpose") == "mortgage"

    eligible = is_teacher and purpose_ok
    enhanced = is_teacher and top_cat and exp_ok and purpose_ok

    return {
        "eligible": eligible,
        "program_id": "teacher_mortgage",
        "program_name": "O'qituvchilar ipotekasi",
        "benefit": (
            "Boshlang'ich to'lov 5% + 25% chegirma (oliy toifali, 15+ yil)"
            if enhanced
            else "Boshlang'ich to'lov 5% (o'qituvchilar uchun)"
        ),
        "applicable_banks": ["xalq_banki"],
        "rate_discount_pct": 0.0,
        "max_loan_uzs": 400_000_000,
        "down_payment_pct": 5.0,
        "down_payment_reduction": 25.0 if enhanced else 0.0,
        "collateral_required": True,
    }


def check_youth_entrepreneur(p: dict) -> dict:
    """
    Yoshlar tadbirkorligi — Youth entrepreneur pilot 2025-2026.
    Interest-free (14% subsidized), up to 40.5M UZS. MKBank.
    """
    eligible = (
        p.get("is_youth_entrepreneur", False)
        and p.get("age", 99) <= 35
        and p.get("employment_type") in ("entrepreneur", "self_employed")
        and p.get("loan_purpose") in ("business", "consumer")
        and p.get("loan_amount_requested_uzs", 0) <= 40_500_000
    )
    return {
        "eligible": eligible,
        "program_id": "youth_entrepreneur",
        "program_name": "Yoshlar tadbirkorligi (pilot)",
        "benefit": "14% subsidiyalangan stavka, 40.5M UZS gacha (2025-2026 pilot)",
        "applicable_banks": ["mkbank"],
        "rate_discount_pct": 12.0,   # ~26% standard → 14%
        "max_loan_uzs": 40_500_000,
        "collateral_required": False,
    }


def check_mahalla_low_income(p: dict) -> dict:
    """
    Arzon ipoteka (Mahalla) — Low-income families, 14-16%, 15% down, 300M max.
    MKBank.
    """
    eligible = (
        p.get("is_mahalla_low_income", False)
        and p.get("loan_purpose") == "mortgage"
        and p.get("loan_amount_requested_uzs", 0) <= 300_000_000
    )
    return {
        "eligible": eligible,
        "program_id": "mahalla_low_income",
        "program_name": "Arzon ipoteka (Mahalla)",
        "benefit": "Kam ta'minlangan oilalar uchun 14-16% stavka, 15% boshlang'ich to'lov",
        "applicable_banks": ["mkbank"],
        "rate_discount_pct": 10.0,
        "max_loan_uzs": 300_000_000,
        "down_payment_pct": 15.0,
        "collateral_required": True,
    }


def check_agriculture(p: dict) -> dict:
    """
    Qishloq xo'jaligi krediti — Farmers, Agrobank, 14-18%, up to 200M UZS.
    """
    eligible = (
        p.get("is_farmer", False)
        and p.get("employment_type") in ("farmer", "self_employed", "entrepreneur")
        and p.get("loan_amount_requested_uzs", 0) <= 200_000_000
    )
    return {
        "eligible": eligible,
        "program_id": "agriculture",
        "program_name": "Qishloq xo'jaligi krediti",
        "benefit": "Fermerlar uchun 14-18% imtiyozli stavka, 200M UZS gacha",
        "applicable_banks": ["agrobank"],
        "rate_discount_pct": 8.0,
        "max_loan_uzs": 200_000_000,
        "collateral_required": False,
    }


def check_rural_mortgage(p: dict) -> dict:
    """
    Qishloq ipotekasi — Rural mortgage, Agrobank, 14-17%, up to 300M.
    """
    eligible = (
        p.get("is_farmer", False)
        and p.get("loan_purpose") == "mortgage"
        and p.get("loan_amount_requested_uzs", 0) <= 300_000_000
    )
    return {
        "eligible": eligible,
        "program_id": "rural_mortgage",
        "program_name": "Qishloq ipotekasi",
        "benefit": "Qishloq joylari uchun 14-17% imtiyozli ipoteka, 300M UZS gacha",
        "applicable_banks": ["agrobank"],
        "rate_discount_pct": 9.0,
        "max_loan_uzs": 300_000_000,
        "collateral_required": True,
    }


def check_budget_salary_project(p: dict) -> dict:
    """
    Maosh loyihasi — State/budget employees with salary card at partner bank.
    Lower rate, no collateral up to 100M.
    Multiple banks: Hamkorbank, Ipak Yo'li, Orient Finans, MKBank, NBU.
    """
    is_budget = p.get("employment_type") == "employed_state"
    has_salary_bank = p.get("salary_bank") not in ("none", "other")
    eligible = (
        is_budget
        and has_salary_bank
        and p.get("loan_amount_requested_uzs", 0) <= 100_000_000
        and p.get("loan_purpose") in ("consumer", "education", "computer_equipment")
    )
    return {
        "eligible": eligible,
        "program_id": "budget_salary_project",
        "program_name": "Maosh loyihasi",
        "benefit": "Byudjet xodimlari uchun -2–4% stavka, garovsiz 100M UZS gacha",
        "applicable_banks": ["hamkorbank", "ipak_yoli", "orient_finans", "mkbank", "nbu"],
        "rate_discount_pct": 3.0,
        "max_loan_uzs": 100_000_000,
        "collateral_required": False,
    }


def check_education_loan(p: dict) -> dict:
    """
    Ta'lim krediti — State-subsidized 14%, all students.
    MKBank, NBU, Xalq Banki.
    """
    eligible = (
        p.get("loan_purpose") == "education"
        and p.get("is_student", False)
    )
    return {
        "eligible": eligible,
        "program_id": "education_loan",
        "program_name": "Ta'lim krediti",
        "benefit": "Talabalar uchun 14% subsidiyalangan stavka",
        "applicable_banks": ["mkbank", "nbu", "xalq_banki"],
        "rate_discount_pct": 12.0,
        "max_loan_uzs": None,   # depends on tuition
        "collateral_required": False,
    }


def check_green_energy(p: dict) -> dict:
    """
    Yashil energiya — Solar/green energy loans. Aloqabank, 15-20%, up to 50M.
    """
    eligible = (
        p.get("loan_purpose") == "green_energy"
        and p.get("loan_amount_requested_uzs", 0) <= 50_000_000
    )
    return {
        "eligible": eligible,
        "program_id": "green_energy",
        "program_name": "Yashil energiya krediti",
        "benefit": "Quyosh panellari uchun 15-20% imtiyozli stavka, 50M UZS gacha",
        "applicable_banks": ["aloqabank"],
        "rate_discount_pct": 6.0,
        "max_loan_uzs": 50_000_000,
        "collateral_required": False,
    }


def check_women_ifc(p: dict) -> dict:
    """
    IFC Women Entrepreneurs — Ipak Yo'li Bank, women business owners.
    """
    eligible = (
        p.get("gender") == "female"
        and p.get("employment_type") in ("entrepreneur", "self_employed", "business_owner")
        and p.get("loan_purpose") == "business"
    )
    return {
        "eligible": eligible,
        "program_id": "women_ifc",
        "program_name": "IFC Ayol tadbirkorlar dasturi",
        "benefit": "Ayol tadbirkorlar uchun imtiyozli biznes kredit (Ipak Yo'li / IFC)",
        "applicable_banks": ["ipak_yoli"],
        "rate_discount_pct": 3.0,
        "max_loan_uzs": None,
        "collateral_required": False,
    }


# ── Registry ─────────────────────────────────────────────────────────────────

ALL_PROGRAMS = [
    check_hamrokh,
    check_teacher_mortgage,
    check_youth_entrepreneur,
    check_mahalla_low_income,
    check_agriculture,
    check_rural_mortgage,
    check_budget_salary_project,
    check_education_loan,
    check_green_energy,
    check_women_ifc,
]
