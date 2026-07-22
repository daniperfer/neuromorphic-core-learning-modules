"""
Lecture 9.2: The Perceptron and Biological Neurons
"""

import matplotlib.pyplot as plt
import numpy as np


# A single perceptron: manual implementation
def perceptron_predict(X, weights, bias):
    """
    X: feature matrix (n_samples x n_features)
    weights: weight vector (n_features,)
    bias: scalar bias term
    Returns: binary predictions (0 or 1)
    """
    # Weighted sum — analogous to synaptic integration
    linear_output = np.dot(X, weights) + bias

    # Step function threshold — analogous to action potential threshold
    predictions = (linear_output >= 0).astype(int)
    return predictions


# Simulate a simple neuron classification problem:
# Can a perceptron distinguish two classes of neural events
# based on amplitude and duration?

np.random.seed(7)

# Class 0: short, low-amplitude events (noise bursts)
class0 = np.random.randn(50, 2) + np.array([-1.5, -1.5])

# Class 1: tall, longer-duration events (true spikes)
class1 = np.random.randn(50, 2) + np.array([1.5, 1.5])

X = np.vstack([class0, class1])
y = np.array([0] * 50 + [1] * 50)

print("Feature matrix shape:", X.shape)  # (100, 2)
print("Label vector shape:  ", y.shape)  # (100,)
print("Class distribution:  ", np.bincount(y))


def train_perceptron(X, y, learning_rate=0.1, n_epochs=50):
    """
    Train a perceptron using the Rosenblatt update rule.

    The update rule:
      if prediction is wrong:
          weights += learning_rate * (true_label - predicted) * input
          bias    += learning_rate * (true_label - predicted)

    This directly mirrors Hebbian plasticity: weights that contributed
    to a correct prediction are unchanged; weights that contributed to
    an error are adjusted in the corrective direction.
    """
    n_features = X.shape[1]
    weights = np.zeros(n_features)
    bias = 0.0
    errors_per_epoch = []

    for epoch in range(n_epochs):
        errors = 0
        for xi, yi in zip(X, y):
            prediction = int(np.dot(xi, weights) + bias >= 0)
            update = learning_rate * (yi - prediction)
            weights += update * xi
            bias += update
            errors += int(update != 0)
        errors_per_epoch.append(errors)

    return weights, bias, errors_per_epoch


weights, bias, error_history = train_perceptron(X, y)

print(f"\nLearned weights: [{weights[0]:.3f}, {weights[1]:.3f}]")
print(f"Learned bias:    {bias:.3f}")
print(f"Final epoch errors: {error_history[-1]}")
# Visualize learning progress and decision boundary
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: training error over epochs
axes[0].plot(error_history, color="#e74c3c", linewidth=2)
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Misclassified examples")
axes[0].set_title("Perceptron Learning Curve")
axes[0].axhline(y=0, color="gray", linestyle="--", alpha=0.5)

# Right: decision boundary
axes[1].scatter(class0[:, 0], class0[:, 1], c="#3498db", label="Noise (class 0)", alpha=0.7)
axes[1].scatter(class1[:, 0], class1[:, 1], c="#e74c3c", label="Spikes (class 1)", alpha=0.7)

# Draw the decision boundary: weights[0]*x + weights[1]*y + bias = 0
x_line = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
if weights[1] != 0:
    y_line = -(weights[0] * x_line + bias) / weights[1]
    axes[1].plot(x_line, y_line, "k-", linewidth=2, label="Decision boundary")

axes[1].set_xlabel("Peak Amplitude")
axes[1].set_ylabel("Event Duration")
axes[1].set_title("Perceptron Decision Boundary")
axes[1].legend()

plt.tight_layout()
plt.savefig("figure_9-2_perceptron_learning.png", dpi=150)
print()

# Demonstrate the XOR problem — perceptron limitation
# This mirrors a real neuroscience problem: some neural states
# cannot be separated by any linear combination of their features

X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])  # XOR: fires only when inputs differ

weights_xor, bias_xor, errors_xor = train_perceptron(X_xor, y_xor, learning_rate=0.1, n_epochs=100)

print("XOR final epoch errors:", errors_xor[-1])
print("(Non-zero = perceptron failed to converge — expected!)")

# This is why we need multi-layer networks: they can learn
# non-linear boundaries by composing multiple perceptrons

print()

x = np.linspace(-5, 5, 300)

# 1. Sigmoid: maps any value to (0, 1)
# Historically the most common; biologically resembles a
# neuron's sigmoidal input-output (f-I) curve
sigmoid = 1 / (1 + np.exp(-x))

# 2. ReLU (Rectified Linear Unit): max(0, x)
# Currently dominant in deep networks; computationally efficient;
# resembles a threshold-linear neuron model from computational neuroscience
relu = np.maximum(0, x)

# 3. Tanh: maps any value to (-1, 1)
# Centered at zero; often preferred over sigmoid for hidden layers
tanh = np.tanh(x)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, func, name, color in zip(
    axes, [sigmoid, relu, tanh], ["Sigmoid", "ReLU", "Tanh"], ["#3498db", "#e74c3c", "#2ecc71"]
):
    ax.plot(x, func, color=color, linewidth=2.5)
    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.set_title(f"{name} Activation Function", fontweight="bold")
    ax.set_xlabel("Input (weighted sum)")
    ax.set_ylabel("Output (activation)")
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figure_9-2_activation_functions.png", dpi=150)
print()
