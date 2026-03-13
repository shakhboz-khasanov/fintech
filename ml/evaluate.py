"""
SarfAI V2 — Model Evaluation

Prints a full model quality report including:
  - Accuracy, ROC-AUC, F1
  - Confusion matrix
  - Feature importances
  - Sample predictions

Usage:
    python evaluate.py [--data path/to/sarfai_datasets.xlsx]
"""
import argparse
import json
import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report, roc_auc_score,
    confusion_matrix, accuracy_score,
    precision_recall_curve, average_precision_score
)

sys.path.insert(0, os.path.dirname(__file__))
from features import compute_features_batch, FEATURE_NAMES
from train import load_dataset
from predict import SarfAIPredictor

_ML_DIR = os.path.dirname(__file__)


def evaluate(xlsx_path: str):
    print("=" * 60)
    print("SarfAI V2 — Model Evaluation Report")
    print("=" * 60)

    # ── Load model ────────────────────────────────────────────────────────────
    predictor = SarfAIPredictor(model_dir=_ML_DIR)
    model     = predictor.model
    scaler    = predictor.scaler

    meta_path = os.path.join(_ML_DIR, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
        print(f"\nModel type   : {meta.get('model_type')}")
        print(f"Features     : {meta.get('n_features')}")
        print(f"Train rows   : {meta.get('n_train')}")
        print(f"Test rows    : {meta.get('n_test')}")
        print(f"Approval rate: {meta.get('approval_rate', 0)*100:.1f}%")

    # ── Load full dataset ─────────────────────────────────────────────────────
    profiles, y = load_dataset(xlsx_path)
    X = compute_features_batch(profiles)
    X_s = scaler.transform(X)

    y_pred  = model.predict(X_s)
    y_proba = model.predict_proba(X_s)[:, 1]

    acc = accuracy_score(y, y_pred)
    auc = roc_auc_score(y, y_proba)
    ap  = average_precision_score(y, y_proba)

    print(f"\n── Metrics (full dataset) ───────────────────────────")
    print(f"  Accuracy        : {acc:.4f}")
    print(f"  ROC-AUC         : {auc:.4f}")
    print(f"  Avg Precision   : {ap:.4f}")
    if meta:
        print(f"  CV AUC (5-fold) : {meta.get('cv_auc_mean'):.4f} ± {meta.get('cv_auc_std'):.4f}")

    print(f"\n── Classification Report ────────────────────────────")
    print(classification_report(y, y_pred, target_names=["Rejected", "Approved"]))

    cm = confusion_matrix(y, y_pred)
    print(f"── Confusion Matrix ─────────────────────────────────")
    print(f"               Predicted")
    print(f"               Rej    App")
    print(f"  Actual Rej   {cm[0,0]:<6} {cm[0,1]}")
    print(f"  Actual App   {cm[1,0]:<6} {cm[1,1]}")
    tn, fp, fn, tp = cm.ravel()
    print(f"\n  True Negative  (correct rejections) : {tn}")
    print(f"  False Positive (wrong approvals)    : {fp}")
    print(f"  False Negative (missed approvals)   : {fn}")
    print(f"  True Positive  (correct approvals)  : {tp}")

    print(f"\n── Feature Importances (by coefficient magnitude) ───")
    coefs = model.coef_[0]
    sorted_idx = np.argsort(np.abs(coefs))[::-1]
    for rank, i in enumerate(sorted_idx, 1):
        sign = "↑" if coefs[i] > 0 else "↓"
        bar  = "█" * int(abs(coefs[i]) * 20)
        print(f"  {rank:2}. {sign} {FEATURE_NAMES[i]:<32} {bar}  {coefs[i]:+.4f}")

    # ── Sample predictions ────────────────────────────────────────────────────
    print(f"\n── Sample Predictions (first 10 test profiles) ──────")
    for i, (profile, actual) in enumerate(zip(profiles[:10], y[:10])):
        result = predictor.predict(profile)
        prob   = result["global_approval_probability"]
        dti    = result["dti_ratio"]
        progs  = [p["program_id"] for p in result["special_programs"]]
        elig   = result["eligible_bank_count"]
        status = "✓" if actual == 1 else "✗"
        print(
            f"  [{status}] prob={prob:.2f}  dti={dti:.2f}  "
            f"eligible_banks={elig}  programs={progs or 'none'}"
        )

    print("\n" + "=" * 60)
    print("Evaluation complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        default=os.path.join(_ML_DIR, "..", "data", "sarfai_datasets.xlsx"),
        help="Path to sarfai_datasets.xlsx",
    )
    args = parser.parse_args()
    evaluate(args.data)
