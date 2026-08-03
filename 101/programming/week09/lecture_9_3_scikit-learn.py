"""
Lecture 9.3: Introduction to scikit-learn
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs, make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# Generate a synthetic spike classification dataset
# Imagine: 3 types of neurons classified by waveform features
X, y = make_blobs(n_samples=300, n_features=2, centers=3, cluster_std=1.2, random_state=42)

# Assign neuroscience-meaningful names to our three classes
class_names = {0: "Fast-spiking interneuron", 1: "Regular-spiking pyramidal", 2: "Bursting neuron"}

colors = ["#e74c3c", "#3498db", "#2ecc71"]

plt.figure(figsize=(7, 5))
for class_idx, (name, color) in enumerate(zip(class_names.values(), colors)):
    mask = y == class_idx
    plt.scatter(X[mask, 0], X[mask, 1], c=color, label=name, alpha=0.7, s=40)

plt.xlabel("Spike half-width (normalized)")
plt.ylabel("Peak-to-trough ratio (normalized)")
plt.title("Simulated Waveform Feature Space\n(3 Neuron Types)")
plt.legend(loc="best", fontsize=8)
plt.tight_layout()
plt.savefig("figure_9-3_neuron_clusters.png", dpi=150)

print(f"Dataset shape: {X.shape}")
print(f"Class distribution: {np.bincount(y)}")

# --------------------------------------------
# Test six different classification algorithms

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Scale features (essential for distance-based and gradient-based algorithms)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Define all classifiers
classifiers = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Support Vector Machine": SVC(kernel="rbf", C=1.0),
    "Decision Tree": DecisionTreeClassifier(max_depth=5),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
    "Neural Network (MLP)": MLPClassifier(
        hidden_layer_sizes=(64, 32), max_iter=500, random_state=42
    ),
}

print(f"{'Algorithm':<30} {'Accuracy':>10}")
print("-" * 42)

results = {}
for name, clf in classifiers.items():
    clf.fit(X_train_s, y_train)  # identical for all classifiers
    y_pred = clf.predict(X_test_s)  # identical for all classifiers
    acc = accuracy_score(y_test, y_pred)  # identical for all classifiers
    results[name] = acc
    print(f"{name:<30} {acc:>9.1%}")
print()

# -----------------------------------------------
# Feature Scaling: Why It Matters for Neural Data

# Simulate multi-scale neural features
np.random.seed(42)
n = 100
spike_amplitude_uV = np.random.normal(150, 40, n)  # mean 150, sd 40 uV
inter_spike_interval = np.random.exponential(20, n)  # mean 20 ms
waveform_area = np.random.normal(0.05, 0.01, n)  # mean 0.05

X_raw = np.column_stack([spike_amplitude_uV, inter_spike_interval, waveform_area])

print("Raw feature statistics:")
print(f"  Amplitude:  mean={X_raw[:,0].mean():.1f}, std={X_raw[:,0].std():.1f}")
print(f"  ISI:        mean={X_raw[:,1].mean():.1f}, std={X_raw[:,1].std():.1f}")
print(f"  Area:       mean={X_raw[:,2].mean():.4f}, std={X_raw[:,2].std():.4f}")

# StandardScaler: subtract mean, divide by std
# Each feature becomes mean=0, std=1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

print("\nAfter StandardScaler:")
print(f"  Amplitude:  mean={X_scaled[:,0].mean():.3f}, std={X_scaled[:,0].std():.3f}")
print(f"  ISI:        mean={X_scaled[:,1].mean():.3f}, std={X_scaled[:,1].std():.3f}")
print(f"  Area:       mean={X_scaled[:,2].mean():.3f}, std={X_scaled[:,2].std():.3f}")
print()

# -----------------------------------------
# A Complete Pipeline with Pipeline Objects

# Simulate: classify seizure vs. non-seizure epochs
# Features: power in delta, theta, alpha, beta, gamma bands
X, y = make_classification(
    n_samples=500, n_features=5, n_informative=4, n_redundant=0, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build pipeline: scale → classify
# No manual scaling needed — the pipeline handles it
pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", SVC(kernel="rbf", C=1.0))])

# Fit and predict work exactly like a regular model
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

# classification_report gives precision, recall, F1 — not just accuracy
print("Seizure Classification Results:")
print(classification_report(y_test, y_pred, target_names=["Non-seizure", "Seizure"]))
print()


"""
# CSV READING SAMPLE

import pandas as pd

# Load spike waveform features from a CSV (Week 6 format)
# Assume columns: half_width, peak_trough_ratio, peak_amplitude, neuron_type
df = pd.read_csv('spike_waveforms.csv')

X = df[['half_width', 'peak_trough_ratio', 'peak_amplitude']].values
y = df['neuron_type'].values  # string labels, e.g. 'FS', 'RS', 'Burst'

# If labels are strings, encode them as integers
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)
print("Classes:", le.classes_)  # ['Burst' 'FS' 'RS']

# Everything else is identical regardless of where the data came from
"""
