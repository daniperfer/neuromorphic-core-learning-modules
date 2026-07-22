"""
Lecture 9.1: What Is Machine Learning?
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Simulate spike waveform features for two neuron types
# Feature 0: normalized peak amplitude
# Feature 1: spike half-width (ms)
np.random.seed(42)

X, y = make_classification(
    n_samples=200,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_clusters_per_class=1,
    random_state=42,
)

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training examples: {len(X_train)}")
print(f"Testing examples:  {len(X_test)}")

# Train a logistic regression classifier
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate on the test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Classification accuracy: {accuracy:.1%}")

# Visualize the decision boundary
h = 0.02  # step size in the mesh
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap="RdBu")
plt.scatter(
    X_test[:, 0], X_test[:, 1], c=y_test, cmap="RdBu", edgecolors="k", s=60, label="Test points"
)
plt.xlabel("Peak Amplitude (normalized)")
plt.ylabel("Spike Half-Width (ms)")
plt.title("Logistic Regression: Neuron Type Classification")
plt.colorbar(label="Predicted class (0=Interneuron, 1=Pyramidal)")
plt.tight_layout()
plt.savefig("figure_9-1_decision_boundary.png", dpi=150)
