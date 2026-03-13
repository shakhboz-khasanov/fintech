"""
SarfAI V2 — Inference / Prediction

Entry point for the backend to call.

Usage:
    from ml.predict import SarfAIPredictor

    predictor = SarfAIPredictor()          # loads model once
    result = predictor.predict(profile)    # call per request
"""
import os
import sys
import json
import joblib
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from features import compute_features
from programs import check_all_programs
from banks import score_per_bank

_DEFAULT_MODEL_DIR = os.path.dirname(__file__)


class SarfAIPredictor:
    """
    Singleton-style predictor. Instantiate once at app startup,
    call .predict(profile) on each request.
    """

    def __init__(self, model_dir: str = _DEFAULT_MODEL_DIR):
        model_path  = os.path.join(model_dir, "model.pkl")
        scaler_path = os.path.join(model_dir, "scaler.pkl")
        meta_path   = os.path.join(model_dir, "meta.json")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"model.pkl not found at {model_path}. Run train.py first."
            )

        self.model  = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as f:
                self.meta = json.load(f)
        else:
            self.meta = {}

    # ── Public API ────────────────────────────────────────────────────────────

    def predict(self, profile: dict) -> dict:
        """
        Main inference method.

        Args:
            profile: dict with all (or partial) user profile fields.
                     See features.py for the full field list.

        Returns:
            {
              "global_approval_probability": float,   # 0.0 – 1.0
              "dti_ratio": float,
              "dti_warning": bool,                    # True if DTI > 0.40
              "dti_critical": bool,                   # True if DTI > 0.50 (CBU hard cap)
              "max_affordable_loan_uzs": int,
              "per_bank_scores": [ { ... } ],         # sorted best → worst
              "eligible_bank_count": int,
              "special_programs": [ { ... } ],
              "profile_tips": [ str ],
            }
        """
        # ── 1. Compute features & global probability ──────────────────────────
        feats = compute_features(profile).reshape(1, -1)
        feats_scaled = self.scaler.transform(feats)
        global_prob = float(self.model.predict_proba(feats_scaled)[0, 1])

        # ── 2. DTI ────────────────────────────────────────────────────────────
        total_income = (
            float(profile.get("monthly_income_uzs", 1))
            + float(profile.get("additional_income_uzs", 0))
        )
        total_income = max(total_income, 1.0)
        existing_debt = float(profile.get("existing_debt_monthly_uzs", 0))
        loan_amount   = float(profile.get("loan_amount_requested_uzs", 0))
        loan_term     = max(float(profile.get("loan_term_months", 12)), 1.0)

        r = 0.26 / 12
        monthly_payment = loan_amount * r / (1 - (1 + r) ** (-loan_term))
        dti = (existing_debt + monthly_payment) / total_income

        # Max affordable loan (CBU 50% DTI cap)
        max_monthly_payment = max(0.0, total_income * 0.50 - existing_debt)
        if max_monthly_payment > 0 and r > 0:
            n = loan_term
            max_affordable = max_monthly_payment * (1 - (1 + r) ** (-n)) / r
        else:
            max_affordable = 0.0

        # ── 3. Special programs ───────────────────────────────────────────────
        programs = check_all_programs(profile)
        program_ids = [p["program_id"] for p in programs]

        # ── 4. Per-bank scores ────────────────────────────────────────────────
        per_bank = score_per_bank(global_prob, profile, program_ids)
        eligible_count = sum(1 for b in per_bank if b["eligible"])

        # ── 5. Profile tips ───────────────────────────────────────────────────
        tips = self._build_tips(profile, dti, global_prob, per_bank)

        return {
            "global_approval_probability": round(global_prob, 3),
            "dti_ratio":                  round(dti, 3),
            "dti_warning":                dti > 0.40,
            "dti_critical":               dti > 0.50,
            "max_affordable_loan_uzs":    int(max_affordable),
            "per_bank_scores":            per_bank,
            "eligible_bank_count":        eligible_count,
            "special_programs":           programs,
            "profile_tips":               tips,
        }

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _build_tips(
        self,
        profile: dict,
        dti: float,
        prob: float,
        per_bank: list[dict],
    ) -> list[str]:
        tips = []

        # DTI tips
        if dti > 0.50:
            tips.append(
                "⚠️ DTI nisbatingiz 50% chegarasidan oshib ketgan — "
                "Markaziy bank qoidasiga ko'ra, ko'pchilik banklar rad etishi mumkin. "
                "Kredit miqdorini kamaytiring yoki muddatni uzaytiring."
            )
        elif dti > 0.40:
            tips.append(
                "📊 DTI nisbatingiz 40–50% oralig'ida — ba'zi banklar qo'shimcha "
                "garov yoki kafil talab qilishi mumkin."
            )

        # Collateral tip
        if not profile.get("has_collateral") and float(profile.get("loan_amount_requested_uzs", 0)) > 50_000_000:
            tips.append(
                "🏠 50M UZS dan ortiq kreditlar uchun garov taqdim etish "
                "tasdiqlash ehtimolini sezilarli oshiradi."
            )

        # Guarantor tip
        if not profile.get("has_guarantor") and prob < 0.65:
            tips.append(
                "👤 Kafil qo'shish tasdiqlash ehtimolini taxminan +10–15% oshirishi mumkin."
            )

        # Credit history tip
        credit = profile.get("credit_history_status")
        if credit == "overdue":
            tips.append(
                "🔴 Muddati o'tgan qarz yozuvlari tufayli aksariyat banklar rad etadi. "
                "Avval mavjud qarzlarni to'lang."
            )
        elif credit == "bad":
            tips.append(
                "🟡 Kredit tarixi yomon — garovli mahsulotlarni yoki "
                "maxsus dasturlarni ko'rib chiqing."
            )
        elif credit == "none":
            tips.append(
                "ℹ️ Kredit tarixi yo'q — kichik summali kredit bilan boshlash "
                "kredit tarixini shakllantiradi."
            )

        # Salary bank tip
        salary_bank = profile.get("salary_bank", "none")
        if salary_bank == "none" and profile.get("employment_type") in ("employed_state", "employed_private"):
            tips.append(
                "💳 Maosh loyihasi orqali bank kartasiga o'tish stavkani "
                "2–4% kamaytirishi mumkin."
            )

        # Income proof tip
        if profile.get("income_proof_type") == "none":
            tips.append(
                "📄 Rasmiy daromad ma'lumotnomasi (2-NDFL yoki bank ko'chirma) "
                "tasdiqlash ehtimolini oshiradi."
            )

        # Loan amount vs affordable
        loan = float(profile.get("loan_amount_requested_uzs", 0))
        total_income = max(
            float(profile.get("monthly_income_uzs", 1))
            + float(profile.get("additional_income_uzs", 0)),
            1.0
        )
        loan_term = max(float(profile.get("loan_term_months", 12)), 1.0)
        r = 0.26 / 12
        monthly_payment = loan * r / (1 - (1 + r) ** (-loan_term))
        if monthly_payment > total_income * 0.45:
            affordable = int(
                (total_income * 0.45) * (1 - (1 + r) ** (-loan_term)) / r
            )
            tips.append(
                f"💡 So'ralgan summa oylik daromadingizga nisbatan juda katta. "
                f"Taxminiy maqbul chegara: {affordable:,} UZS."
            )

        # Term tip for mortgage
        if profile.get("loan_purpose") == "mortgage" and float(profile.get("loan_term_months", 0)) < 60:
            tips.append(
                "🏗️ Ipoteka uchun minimal muddat odatda 60 oy (5 yil). "
                "Muddatni oshirishni ko'rib chiqing."
            )

        # No eligible banks tip
        if sum(1 for b in per_bank if b["eligible"]) == 0:
            tips.append(
                "❌ Hozirgi profil bo'yicha mos bank mahsuloti topilmadi. "
                "Kredit miqdorini kamaytiring yoki garov qo'shing."
            )

        return tips


# ── Convenience function ─────────────────────────────────────────────────────

_predictor: SarfAIPredictor | None = None


def get_predictor(model_dir: str = _DEFAULT_MODEL_DIR) -> SarfAIPredictor:
    """Return a module-level singleton predictor (lazy-loaded)."""
    global _predictor
    if _predictor is None:
        _predictor = SarfAIPredictor(model_dir=model_dir)
    return _predictor


def predict(profile: dict, model_dir: str = _DEFAULT_MODEL_DIR) -> dict:
    """Stateless convenience wrapper."""
    return get_predictor(model_dir).predict(profile)
