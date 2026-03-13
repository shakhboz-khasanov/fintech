"""
SarfAI V2 — Model Training

Reads sarfai_datasets.xlsx (Sheet: ML User Dataset),
engineers features via features.py,
trains a Logistic Regression model,
and saves model.pkl + meta.json.

Usage:
    python train.py [--data path/to/sarfai_datasets.xlsx]
"""
import argparse
import json
import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, roc_auc_score,
    confusion_matrix, accuracy_score
)

# Local imports
sys.path.insert(0, os.path.dirname(__file__))
from features import compute_features_batch, FEATURE_NAMES

# ── Column mapping: Excel → profile dict keys ────────────────────────────────

COLUMN_MAP = {
    "age":                          "age",
    "gender":                       "gender",
    "dependents_count":             "dependents_count",
    "is_young_family":              "is_young_family",
    "employment_type":              "employment_type",
    "profession_role":              "profession_role",
    "salary_bank":                  "salary_bank",
    "work_experience_months":       "work_experience_months",
    "monthly_income_uzs":           "monthly_income_uzs",
    "has_additional_income":        "has_additional_income",
    "additional_income_uzs":        "additional_income_uzs",
    "income_proof_type":            "income_proof_type",
    "existing_debt_monthly_uzs":    "existing_debt_monthly_uzs",
    "credit_history_status":        "credit_history_status",
    "has_collateral":               "has_collateral",
    "collateral_type":              "collateral_type",
    "collateral_value_uzs":         "collateral_value_uzs",
    "has_guarantor":                "has_guarantor",
    "savings_uzs":                  "savings_uzs",
    "loan_purpose":                 "loan_purpose",
    "loan_amount_requested_uzs":    "loan_amount_requested_uzs",
    "loan_term_months":             "loan_term_months",
    "is_student":                   "is_student",
    "is_mahalla_low_income":        "is_mahalla_low_income",
    "is_women_entrepreneur":        "is_women_entrepreneur",
    "is_youth_entrepreneur":        "is_youth_entrepreneur",
    "is_farmer":                    "is_farmer",
    "teacher_qualification_category": "teacher_qualification_category",
    "teacher_experience_years":     "teacher_experience_years",
    "approved":                     "_label",
}


def load_dataset(xlsx_path: str) -> tuple[list[dict], np.ndarray]:
    print(f"Loading dataset from: {xlsx_path}")
    df = pd.read_excel(xlsx_path, sheet_name="ML User Dataset")
    print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")

    profiles, labels = [], []
    for _, row in df.iterrows():
        profile = {}
        label = None
        for col, key in COLUMN_MAP.items():
            if col not in df.columns:
                continue
            val = row[col]
            # Coerce booleans stored as various types
            if key in (
                "is_young_family", "has_additional_income",
                "has_collateral", "has_guarantor", "is_student",
                "is_mahalla_low_income", "is_women_entrepreneur",
                "is_youth_entrepreneur", "is_farmer",
            ):
                val = bool(val) if not pd.isna(val) else False
            elif key == "_label":
                label = int(val) if not pd.isna(val) else 0
                continue
            else:
                if pd.isna(val):
                    val = None
            profile[key] = val

        profiles.append(profile)
        labels.append(label if label is not None else 0)

    return profiles, np.array(labels)


def train(xlsx_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # ── Load & engineer features ─────────────────────────────────────────────
    profiles, y = load_dataset(xlsx_path)
    print(f"  Approved: {y.sum()} ({100*y.mean():.1f}%)")

    X = compute_features_batch(profiles)
    print(f"  Feature matrix: {X.shape}")

    # ── Train / test split ───────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # ── Scale ────────────────────────────────────────────────────────────────
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)

    # ── Train logistic regression ─────────────────────────────────────────────
    print("\nTraining Logistic Regression...")
    model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        solver="lbfgs",
        class_weight="balanced",
        random_state=42,
    )
    model.fit(X_train_s, y_train)

    # ── Evaluate ─────────────────────────────────────────────────────────────
    y_pred  = model.predict(X_test_s)
    y_proba = model.predict_proba(X_test_s)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    cv_scores = cross_val_score(model, scaler.transform(X), y, cv=5, scoring="roc_auc")

    print(f"\n── Evaluation ───────────────────────────────────────")
    print(f"  Accuracy:        {acc:.4f}")
    print(f"  ROC-AUC:         {auc:.4f}")
    print(f"  CV AUC (5-fold): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"\n── Classification Report ────────────────────────────")
    print(classification_report(y_test, y_pred, target_names=["Rejected", "Approved"]))
    print(f"── Confusion Matrix ─────────────────────────────────")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  TN={cm[0,0]}  FP={cm[0,1]}")
    print(f"  FN={cm[1,0]}  TP={cm[1,1]}")

    # ── Feature importances (via coefficients) ────────────────────────────────
    coefs = model.coef_[0]
    sorted_idx = np.argsort(np.abs(coefs))[::-1]
    print(f"\n── Top Feature Importances ──────────────────────────")
    for i in sorted_idx[:15]:
        sign = "+" if coefs[i] > 0 else "-"
        print(f"  {sign}  {FEATURE_NAMES[i]:<30} {abs(coefs[i]):.4f}")

    # ── Save artifacts ────────────────────────────────────────────────────────
    model_path   = os.path.join(output_dir, "model.pkl")
    scaler_path  = os.path.join(output_dir, "scaler.pkl")
    meta_path    = os.path.join(output_dir, "meta.json")

    joblib.dump(model,  model_path)
    joblib.dump(scaler, scaler_path)

    meta = {
        "model_type":    "LogisticRegression",
        "feature_names": FEATURE_NAMES,
        "n_features":    len(FEATURE_NAMES),
        "n_train":       len(X_train),
        "n_test":        len(X_test),
        "accuracy":      round(acc, 4),
        "roc_auc":       round(auc, 4),
        "cv_auc_mean":   round(float(cv_scores.mean()), 4),
        "cv_auc_std":    round(float(cv_scores.std()), 4),
        "approval_rate": round(float(y.mean()), 4),
        "trained_on":    xlsx_path,
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"\n── Saved ────────────────────────────────────────────")
    print(f"  model.pkl  → {model_path}")
    print(f"  scaler.pkl → {scaler_path}")
    print(f"  meta.json  → {meta_path}")
    print("\nTraining complete ✓")
    return model, scaler, meta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train SarfAI V2 ML model")
    parser.add_argument(
        "--data",
        default=os.path.join(os.path.dirname(__file__), "..", "data", "sarfai_datasets.xlsx"),
        help="Path to sarfai_datasets.xlsx",
    )
    parser.add_argument(
        "--out",
        default=os.path.dirname(__file__),
        help="Directory to save model artifacts",
    )
    args = parser.parse_args()
    train(args.data, args.out)
