"""
Lecture 9.7: Evaluating and Improving Models
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import uniform
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (  # RocCurveDisplay,
    auc,
    average_precision_score,
    f1_score,
    precision_recall_curve,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedKFold,
    permutation_test_score,
    train_test_split,
)
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_class_weight

np.random.seed(42)

# Binary classification: seizure detection
# Features: LFP (local field potentials) power in 5 frequency bands + 2 nonlinear features
X, y = make_classification(
    n_samples=500, n_features=7, n_informative=5, weights=[0.85, 0.15], random_state=42
)
# Note: weights=[0.85, 0.15] creates imbalance — 85% non-seizure, 15% seizure
# This is realistic for epilepsy monitoring datasets

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Train multiple classifiers
classifiers = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, class_weight="balanced", random_state=42
    ),
    "SVM (RBF)": SVC(probability=True, class_weight="balanced", random_state=42),
}

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

for name, clf in classifiers.items():
    clf.fit(X_train_s, y_train)
    y_score = clf.predict_proba(X_test_s)[:, 1]

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    axes[0].plot(fpr, tpr, linewidth=2, label=f"{name} (AUC = {roc_auc:.3f})")

    # Precision-Recall curve
    precision, recall, _ = precision_recall_curve(y_test, y_score)
    ap = average_precision_score(y_test, y_score)
    axes[1].plot(recall, precision, linewidth=2, label=f"{name} (AP = {ap:.3f})")

# ROC plot
axes[0].plot([0, 1], [0, 1], "k--", linewidth=1, label="Chance (AUC = 0.500)")
axes[0].set_xlabel("False Positive Rate\n(1 - Specificity)", fontsize=11)
axes[0].set_ylabel("True Positive Rate (Sensitivity)", fontsize=11)
axes[0].set_title("ROC Curves: Seizure Detection", fontweight="bold")
axes[0].legend(fontsize=8)
axes[0].grid(True, alpha=0.3)

# Precision-Recall plot (better for imbalanced data)
baseline_rate = y_test.mean()
axes[1].axhline(
    baseline_rate, color="gray", linestyle="--", label=f"Chance (precision = {baseline_rate:.2f})"
)
axes[1].set_xlabel("Recall (Sensitivity)", fontsize=11)
axes[1].set_ylabel("Precision", fontsize=11)
axes[1].set_title(
    "Precision-Recall Curves: Seizure Detection\n" "(better metric for imbalanced datasets)",
    fontweight="bold",
)
axes[1].legend(fontsize=8)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figure_9-7_roc_pr_curves.png", dpi=150)
print()

# ---------------------------------------
# Permutation Tests: Is Your Result Real?

clf_perm = RandomForestClassifier(n_estimators=50, class_weight="balanced", random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# This function:
# 1. Computes real cross-validated accuracy
# 2. Runs the model 100 times with shuffled labels
# 3. Returns all permuted scores and a p-value
score, perm_scores, pvalue = permutation_test_score(
    clf_perm, X, y, cv=cv, n_permutations=100, scoring="roc_auc", n_jobs=-1, random_state=42
)

print(f"Real classifier AUC:      {score:.4f}")
print(f"Permutation mean AUC:     {perm_scores.mean():.4f} ± {perm_scores.std():.4f}")
print(f"P-value:                  {pvalue:.4f}")
print(f"Result is {'SIGNIFICANT' if pvalue < 0.05 else 'NOT SIGNIFICANT'} (p < 0.05)")

# Visualize the null distribution
plt.figure(figsize=(8, 4))
plt.hist(
    perm_scores,
    bins=20,
    color="#95a5a6",
    alpha=0.8,
    label="Permuted label scores",
    edgecolor="white",
)
plt.axvline(
    score, color="#e74c3c", linewidth=3, linestyle="-", label=f"Real classifier: AUC = {score:.3f}"
)
plt.axvline(
    perm_scores.mean(),
    color="gray",
    linewidth=1.5,
    linestyle="--",
    label=f"Chance level: AUC = {perm_scores.mean():.3f}",
)
plt.xlabel("Cross-validated AUC")
plt.ylabel("Count")
plt.title(f"Permutation Test: Is Neural Decoding Significant?\np = {pvalue:.4f}")
plt.legend()
plt.tight_layout()
plt.savefig("figure_9-7_permutation_test.png", dpi=150)
print()

# -------------------------------------------------
# Hyperparameter Tuning with Cross-Validated Search

# Grid search: exhaustive over specified values
# Best for small search spaces with clear options
param_grid = {
    "hidden_layer_sizes": [(32,), (64,), (64, 32), (128, 64), (64, 32, 16)],
    "alpha": [0.0001, 0.001, 0.01],  # L2 regularization strength
    "learning_rate_init": [0.001, 0.01],
}

mlp = MLPClassifier(max_iter=300, early_stopping=True, validation_fraction=0.15, random_state=42)

grid_search = GridSearchCV(
    mlp,
    param_grid,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring="roc_auc",
    n_jobs=-1,
    verbose=1,
)

grid_search.fit(X_train_s, y_train)

print(f"\nBest parameters:    {grid_search.best_params_}")
print(f"Best CV AUC (train-val):        {grid_search.best_score_:.4f}")

# Evaluate best model on test set
best_model = grid_search.best_estimator_
y_score_best = best_model.predict_proba(X_test_s)[:, 1]
test_auc = auc(*roc_curve(y_test, y_score_best)[:2])
print(f"Test AUC (best model): {test_auc:.4f}")
print()

# Randomized search: efficient for continuous hyperparameters
param_dist = {
    "hidden_layer_sizes": [(32,), (64,), (64, 32), (128, 64), (128, 64, 32)],
    "alpha": uniform(0.0001, 0.05),  # Uniform distribution between 0.0001 and 0.05
    "learning_rate_init": uniform(0.0005, 0.02),
}

random_search = RandomizedSearchCV(
    mlp,
    param_dist,
    n_iter=20,  # Try 20 random combinations
    cv=5,
    scoring="roc_auc",
    n_jobs=-1,
    random_state=42,
)

random_search.fit(X_train_s, y_train)
print(f"\nRandomized search best AUC: {random_search.best_score_:.4f}")
print(f"Best params: {random_search.best_params_}")
print()

# ----------------------------------------------------
# Class Imbalance: Handling Unequal Neuron Type Counts

# Approach 1: class_weight='balanced' in the classifier
# The algorithm internally upweights minority class examples
clf_balanced = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",  # Automatically weights inversely to frequency
    random_state=42,
)

# Approach 2: Sample weights (for Keras)
# Compute weights inversely proportional to class frequency
classes = np.unique(y_train)
weights = compute_class_weight("balanced", classes=classes, y=y_train)
weight_dict = dict(zip(classes, weights))
print("Class weights:", weight_dict)
# Then pass to model.fit: model.fit(X, y, class_weight=weight_dict)

# Approach 3: Threshold optimization
# For binary classifiers, the decision threshold of 0.5 is rarely optimal
# when classes are imbalanced — a lower threshold increases recall for minority class

clf_balanced.fit(X_train_s, y_train)
y_score_bal = clf_balanced.predict_proba(X_test_s)[:, 1]

thresholds = np.arange(0.1, 0.9, 0.05)
f1_scores = []

for thresh in thresholds:
    y_pred_thresh = (y_score_bal >= thresh).astype(int)
    f1_scores.append(f1_score(y_test, y_pred_thresh, zero_division=0))

best_thresh = thresholds[np.argmax(f1_scores)]
print(f"\nOptimal threshold (F1): {best_thresh:.2f}")
print(f"F1 at optimal threshold: {max(f1_scores):.3f}")
print(f"F1 at default (0.5) threshold: {f1_score(y_test, (y_score_bal >= 0.5).astype(int)):.3f}")
print()
