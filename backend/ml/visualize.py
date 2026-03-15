import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import roc_curve, auc, confusion_matrix

from train import load_dataset
from features import compute_features_batch, FEATURE_NAMES

BASE_DIR = os.path.dirname(__file__)

# ── Load model ─────────────────────────
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# ── Load dataset ───────────────────────
data_path = os.path.join(BASE_DIR, "..", "data", "sarfai_datasets.xlsx")

profiles, y = load_dataset(data_path)

X = compute_features_batch(profiles)
X_s = scaler.transform(X)

y_pred = model.predict(X_s)
y_prob = model.predict_proba(X_s)[:,1]

# ───────────────────────────────────────
# ROC CURVE
# ───────────────────────────────────────

fpr, tpr, _ = roc_curve(y, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6,6))
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
plt.plot([0,1],[0,1],'--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()

# ───────────────────────────────────────
# CONFUSION MATRIX
# ───────────────────────────────────────

cm = confusion_matrix(y, y_pred)

plt.figure(figsize=(5,4))
sns.heatmap(cm,
            annot=True,
            fmt="d",
            xticklabels=["Rejected","Approved"],
            yticklabels=["Rejected","Approved"])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# ───────────────────────────────────────
# FEATURE IMPORTANCE
# ───────────────────────────────────────

coefs = model.coef_[0]

idx = np.argsort(np.abs(coefs))[::-1][:10]

names = [FEATURE_NAMES[i] for i in idx]
values = coefs[idx]

plt.figure(figsize=(8,5))
plt.barh(names, values)
plt.gca().invert_yaxis()
plt.title("Top 10 Feature Importances")
plt.show()