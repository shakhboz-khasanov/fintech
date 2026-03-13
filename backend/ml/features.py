"""
SarfAI V2 — Feature Engineering
Converts a raw user profile dict into a numeric feature vector
for the logistic regression model.

All 34 input fields from the ML spec are used.
CBU Uzbekistan rules are baked into derived features.
"""
import numpy as np

# ── Categorical encodings ────────────────────────────────────────────────────

EMPLOYMENT_TYPE_SCORE = {
    "employed_state":   0.95,
    "employed_private": 0.80,
    "pensioner":        0.88,
    "entrepreneur":     0.62,
    "self_employed":    0.55,
    "farmer":           0.50,
    "student":          0.28,
    "unemployed":       0.05,
}

CREDIT_HISTORY_SCORE = {
    "good":    1.0,
    "none":    0.55,
    "bad":     0.20,
    "overdue": 0.00,
}

INCOME_PROOF_SCORE = {
    "official_certificate": 1.0,
    "bank_statement":       0.80,
    "tax_declaration":      0.70,
    "none":                 0.20,
}

COLLATERAL_TYPE_SCORE = {
    "both":        1.0,
    "real_estate": 0.90,
    "vehicle":     0.65,
    "none":        0.0,
}

LOAN_PURPOSE_RISK = {
    "mortgage":           0.85,   # secured, lower risk
    "education":          0.80,
    "auto":               0.75,
    "green_energy":       0.78,
    "computer_equipment": 0.72,
    "consumer":           0.60,
    "business":           0.55,
}

PROFESSION_STABILITY = {
    # Education
    "teacher":             0.90,
    "professor_lecturer":  0.88,
    "school_principal":    0.92,
    "vocational_trainer":  0.85,
    "tutor_private":       0.60,
    # Healthcare
    "doctor_physician":    0.92,
    "dentist":             0.88,
    "pharmacist":          0.82,
    "nurse":               0.80,
    "hospital_admin":      0.85,
    "paramedic":           0.78,
    # Security / military
    "military":            0.95,
    "police_officer":      0.93,
    "firefighter":         0.90,
    "border_guard":        0.92,
    "prison_officer":      0.88,
    "intelligence_nss":    0.95,
    # Agriculture
    "farmer":              0.52,
    "agronomist":          0.65,
    "dehqon":              0.48,
    "farm_manager":        0.68,
    # IT / Tech
    "software_developer":  0.85,
    "it_specialist":       0.82,
    # Finance / Legal
    "banker":              0.90,
    "accountant":          0.88,
    "lawyer":              0.85,
    "notary":              0.87,
    # Civil service
    "civil_servant":       0.92,
    "state_official":      0.94,
    # Business
    "entrepreneur":        0.62,
    "business_owner":      0.65,
    # Other
    "other":               0.55,
}

SALARY_BANK_BONUS = {
    # These banks give better rates to salary-project clients
    "kapitalbank":  0.08,
    "hamkorbank":   0.07,
    "xalq_banki":   0.07,
    "ipoteka_bank": 0.06,
    "nbu":          0.06,
    "orient_finans":0.06,
    "asakabank":    0.05,
    "ipak_yoli":    0.05,
    "agrobank":     0.05,
    "mkbank":       0.05,
    "aloqabank":    0.04,
    "trastbank":    0.04,
    "turonbank":    0.04,
    "other":        0.02,
    "none":         0.00,
}

# ── Main feature function ────────────────────────────────────────────────────

FEATURE_NAMES = [
    # Demographics
    "age_norm",
    "dependents_norm",
    "is_young_family",
    # Employment
    "employment_stability",
    "profession_stability",
    "work_experience_norm",
    "salary_bank_bonus",
    "is_formal_employed",
    # Income
    "income_log_norm",
    "has_additional_income",
    "additional_income_ratio",
    "income_proof_score",
    # Debt / DTI
    "dti_ratio",
    "existing_debt_ratio",
    "monthly_payment_ratio",
    # Loan characteristics
    "loan_to_annual_income",
    "loan_term_norm",
    "loan_purpose_risk",
    # Collateral / guarantor
    "collateral_score",
    "collateral_coverage_ratio",
    "has_guarantor",
    # Credit history
    "credit_history_score",
    # Special program flags
    "is_student",
    "is_mahalla_low_income",
    "is_women_entrepreneur",
    "is_youth_entrepreneur",
    "is_farmer",
    "is_top_teacher",
    # CBU hard rule signals
    "cbu_dti_ok",          # 1 if DTI ≤ 0.50
    "cbu_collateral_ok",   # 1 if loan ≤ 50M or has collateral
]


def compute_features(profile: dict) -> np.ndarray:
    """
    Convert a user profile dict to a fixed-length feature vector.

    All monetary values assumed to be in UZS.
    Returns np.ndarray of shape (30,).
    """
    # ── Raw inputs ───────────────────────────────────────────────────────────
    age                   = float(profile.get("age", 30))
    dependents            = float(profile.get("dependents_count", 0))
    is_young_family       = float(bool(profile.get("is_young_family", False)))

    employment_type       = profile.get("employment_type", "employed_private")
    profession_role       = profile.get("profession_role", "other")
    work_exp_months       = float(profile.get("work_experience_months", 0))
    salary_bank           = profile.get("salary_bank", "none")

    monthly_income        = max(float(profile.get("monthly_income_uzs", 1)), 1.0)
    has_add_income        = float(bool(profile.get("has_additional_income", False)))
    add_income            = float(profile.get("additional_income_uzs", 0))
    income_proof          = profile.get("income_proof_type", "none")

    existing_debt         = float(profile.get("existing_debt_monthly_uzs", 0))
    credit_hist           = profile.get("credit_history_status", "none")

    has_collateral        = bool(profile.get("has_collateral", False))
    collateral_type       = profile.get("collateral_type", "none")
    collateral_value      = float(profile.get("collateral_value_uzs", 0))
    has_guarantor         = float(bool(profile.get("has_guarantor", False)))
    savings               = float(profile.get("savings_uzs", 0))

    loan_amount           = float(profile.get("loan_amount_requested_uzs", 1_000_000))
    loan_term             = max(float(profile.get("loan_term_months", 12)), 1.0)
    loan_purpose          = profile.get("loan_purpose", "consumer")

    is_student            = float(bool(profile.get("is_student", False)))
    is_mahalla            = float(bool(profile.get("is_mahalla_low_income", False)))
    is_women_ent          = float(bool(profile.get("is_women_entrepreneur", False)))
    is_youth_ent          = float(bool(profile.get("is_youth_entrepreneur", False)))
    is_farmer             = float(bool(profile.get("is_farmer", False)))

    teacher_cat           = profile.get("teacher_qualification_category", "none")
    teacher_exp           = float(profile.get("teacher_experience_years", 0))

    # ── Derived values ───────────────────────────────────────────────────────
    total_income = monthly_income + add_income

    # Rough monthly payment at ~26% annual (average UZB rate)
    r = 0.26 / 12
    monthly_payment = loan_amount * r / (1 - (1 + r) ** (-loan_term))

    dti = (existing_debt + monthly_payment) / max(total_income, 1)

    # Collateral coverage (CBU requires ≥125% for loans >50M)
    collateral_coverage = (
        collateral_value / max(loan_amount, 1) if has_collateral else 0.0
    )

    is_formal = float(employment_type in (
        "employed_state", "employed_private", "pensioner"
    ))

    is_top_teacher = float(
        teacher_cat == "top_category" and teacher_exp >= 15
    )

    # CBU hard rule flags
    cbu_dti_ok = float(dti <= 0.50)
    cbu_collateral_ok = float(
        loan_amount <= 50_000_000 or has_collateral
    )

    # ── Normalised / scored values ───────────────────────────────────────────
    age_norm              = np.clip(age / 65.0, 0, 1)
    dependents_norm       = np.clip(dependents / 10.0, 0, 1)
    emp_stability         = EMPLOYMENT_TYPE_SCORE.get(employment_type, 0.5)
    prof_stability        = PROFESSION_STABILITY.get(profession_role, 0.55)
    work_exp_norm         = np.clip(work_exp_months / 240.0, 0, 1)
    sb_bonus              = SALARY_BANK_BONUS.get(salary_bank, 0.0)
    income_log_norm       = np.clip(np.log1p(total_income) / 18.0, 0, 1)
    add_income_ratio      = np.clip(add_income / max(total_income, 1), 0, 1)
    income_proof_score    = INCOME_PROOF_SCORE.get(income_proof, 0.2)
    dti_clipped           = np.clip(dti, 0, 2.0)
    existing_debt_ratio   = np.clip(existing_debt / max(total_income, 1), 0, 2)
    monthly_pay_ratio     = np.clip(monthly_payment / max(total_income, 1), 0, 2)
    loan_to_ann_income    = np.clip(loan_amount / max(total_income * 12, 1), 0, 10)
    loan_term_norm        = np.clip(loan_term / 240.0, 0, 1)
    purpose_risk          = LOAN_PURPOSE_RISK.get(loan_purpose, 0.6)
    coll_score            = COLLATERAL_TYPE_SCORE.get(collateral_type, 0.0)
    coll_coverage_norm    = np.clip(collateral_coverage / 2.0, 0, 1)
    credit_score          = CREDIT_HISTORY_SCORE.get(credit_hist, 0.55)

    return np.array([
        age_norm,
        dependents_norm,
        is_young_family,
        emp_stability,
        prof_stability,
        work_exp_norm,
        sb_bonus,
        is_formal,
        income_log_norm,
        has_add_income,
        add_income_ratio,
        income_proof_score,
        dti_clipped,
        existing_debt_ratio,
        monthly_pay_ratio,
        loan_to_ann_income,
        loan_term_norm,
        purpose_risk,
        coll_score,
        coll_coverage_norm,
        has_guarantor,
        credit_score,
        is_student,
        is_mahalla,
        is_women_ent,
        is_youth_ent,
        is_farmer,
        is_top_teacher,
        cbu_dti_ok,
        cbu_collateral_ok,
    ], dtype=np.float32)


def compute_features_batch(profiles: list) -> np.ndarray:
    return np.vstack([compute_features(p) for p in profiles])
