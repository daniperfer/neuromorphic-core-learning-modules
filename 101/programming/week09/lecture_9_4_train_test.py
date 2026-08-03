"""
Lecture 9.4: Training and Testing Models
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
from sklearn.model_selection import (
    StratifiedKFold,
    TimeSeriesSplit,
    cross_val_score,
    learning_curve,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

# --------------------------
# The Bias-Variance Tradeoff

# Simulate: predicting firing rate from stimulus intensity
# True relationship: mildly nonlinear
np.random.seed(42)
n = 60
X_1d = np.linspace(0, 3, n)
y_true = 2 * X_1d + 0.5 * X_1d**3 + np.random.normal(0, 0.8, n)

X_train_1d, X_test_1d, y_train, y_test = train_test_split(
    X_1d.reshape(-1, 1), y_true, test_size=0.3, random_state=7
)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
degrees = [1, 4, 15]
titles = [
    "Underfitting\n(degree 1: too simple)",
    "Good fit\n(degree 4: just right)",
    "Overfitting\n(degree 15: too complex)",
]

for ax, degree, title in zip(axes, degrees, titles):
    model = Pipeline([("poly", PolynomialFeatures(degree)), ("reg", LinearRegression())])
    model.fit(X_train_1d, y_train)

    train_err = mean_squared_error(y_train, model.predict(X_train_1d))
    test_err = mean_squared_error(y_test, model.predict(X_test_1d))

    x_plot = np.linspace(0, 3, 200).reshape(-1, 1)
    ax.scatter(X_train_1d, y_train, s=20, alpha=0.6, label="Train", color="#3498db")
    ax.scatter(X_test_1d, y_test, s=20, alpha=0.8, label="Test", color="#e74c3c", marker="^")
    ax.plot(x_plot, model.predict(x_plot), "k-", linewidth=2)
    ax.set_title(f"{title}\nTrain MSE: {train_err:.2f}  Test MSE: {test_err:.2f}")
    ax.legend(fontsize=8)
    ax.set_xlabel("Stimulus Intensity")
    ax.set_ylabel("Firing Rate (spikes/s)")

plt.tight_layout()
plt.savefig("figure_9-4_bias_variance.png", dpi=150)
print("Bias vs. Variance example completed...\n")

"""
Bias is the error that comes from a model being too simple
to capture the true patterns in the data.
A straight line fitted to a dataset that follows a quadratic
relationship will consistently miss the curve — that consistent miss is bias.
High-bias models are said to underfit: they perform poorly on
both training and test data.

Variance is the error that comes from a model being too sensitive
to the particular training examples it saw.
A highly complex model — say, a decision tree with no depth limit — can draw
an elaborate boundary that passes through every single training point perfectly.
Change the training set slightly (a different random 80% of your recordings),
and the boundary changes dramatically.
High-variance models are said to overfit:
they perform excellently on training data but poorly on new data.
"""

# --------------------------------
# Train-Test Split: The Foundation

# Simulate neural state classification:
# 4 brain states based on LFP power features (delta, theta, alpha, beta, gamma)
np.random.seed(42)
X, y = make_classification(
    n_samples=400,
    n_features=5,
    n_informative=4,
    n_redundant=0,
    n_classes=4,
    n_clusters_per_class=1,
    random_state=42,
)

state_names = ["Wake", "NREM-light", "NREM-deep", "REM"]

# 20% test split, stratified to preserve class proportions
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Training:   {len(X_train)} examples")
print(f"Testing:    {len(X_test)} examples")
print(f"\nTraining class distribution: {np.bincount(y_train)}")
print(f"Test class distribution:     {np.bincount(y_test)}")

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(f"\nTest Accuracy: {accuracy_score(y_test, y_pred):.1%}")
print("\nPer-class performance:")
print(classification_report(y_test, y_pred, target_names=state_names))
print()

# -----------------------------------------------------
# Cross-Validation: More Reliable Performance Estimates

# Use the same neural state data
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# 5-fold stratified cross-validation
# StratifiedKFold preserves class proportions in each fold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")

print("5-fold Cross-Validation Results:")
print(f"  Accuracy per fold: {cv_scores.round(3)}")
print(f"  Mean:  {cv_scores.mean():.3f}")
print(f"  Std:   {cv_scores.std():.3f}")
print(
    f"  95% CI: ({cv_scores.mean() - 2 * cv_scores.std():.3f}, "
    f"{cv_scores.mean() + 2 * cv_scores.std():.3f})"
)
print()


# For chronologically ordered neural recording sessions
tscv = TimeSeriesSplit(n_splits=5)
cv_scores_ts = cross_val_score(clf, X, y, cv=tscv, scoring="accuracy")
print("\nTime-series CV (chronological splits):")
print(f"  Mean: {cv_scores_ts.mean():.3f} ± {cv_scores_ts.std():.3f}")
print()

# --------------------------------------------------------
# Learning Curves: Diagnosing Underfitting and Overfitting


def plot_learning_curve(estimator, X, y, title, cv=5, n_jobs=-1):
    """
    Plot learning curves for different train sizes
    """
    train_sizes = np.linspace(0.1, 1.0, 10)

    train_sizes_abs, train_scores, val_scores = learning_curve(
        estimator,
        X,
        y,
        train_sizes=train_sizes,
        cv=StratifiedKFold(n_splits=cv, shuffle=True, random_state=42),
        scoring="accuracy",
        n_jobs=n_jobs,
    )

    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)

    plt.figure(figsize=(8, 5))
    plt.plot(
        train_sizes_abs, train_mean, "o-", color="#3498db", linewidth=2, label="Training score"
    )
    plt.fill_between(
        train_sizes_abs, train_mean - train_std, train_mean + train_std, alpha=0.15, color="#3498db"
    )
    plt.plot(
        train_sizes_abs,
        val_mean,
        "s-",
        color="#e74c3c",
        linewidth=2,
        label="Cross-validation score",
    )
    plt.fill_between(
        train_sizes_abs, val_mean - val_std, val_mean + val_std, alpha=0.15, color="#e74c3c"
    )

    plt.xlabel("Training set size")
    plt.ylabel("Accuracy")
    plt.title(title)
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig("figure_9-4_learning_curve.png", dpi=150)


plot_learning_curve(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X,
    y,
    "Learning Curve: Neural State Classification",
)
print("Learning Curve example completed...\n")

"""
When the training and validation curves converge to
a high accuracy value as training size increases,
your model is well-calibrated and more data will help marginally.
When both curves plateau at a low value,
you have underfitting — a more complex model is needed.
When the training curve is high and the validation curve is
substantially lower with a large gap,
you have overfitting — more data, regularization, or a simpler model is needed.
"""

# -----------------------------------------------------
# Feature Importance: What Is the Model Actually Using?
# Example: 4 brain states based on LFP power features
# (delta, theta, alpha, beta, gamma)

feature_names = ["Delta power", "Theta power", "Alpha power", "Beta power", "Gamma power"]

clf_final = RandomForestClassifier(n_estimators=200, random_state=42)
clf_final.fit(X_train, y_train)

importances = clf_final.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(7, 4))
plt.bar(range(len(feature_names)), importances[indices], color="#3498db", alpha=0.8)
plt.xticks(range(len(feature_names)), [feature_names[i] for i in indices], rotation=20, ha="right")
plt.ylabel("Feature Importance (mean decrease impurity)")
plt.title("What predicts brain state?\nRandom Forest Feature Importances")
plt.tight_layout()
plt.savefig("figure_9-4_feature_importance.png", dpi=150)

for i in indices:
    print(f"  {feature_names[i]:<15}: {importances[i]:.3f}")
print("Feature Importance example completed...")
