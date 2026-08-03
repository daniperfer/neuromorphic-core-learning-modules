"""
Lecture 9.5: Neural Network Architecture with Keras/TensorFlow
"""

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.datasets import make_classification
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping

print(f"TensorFlow version: {tf.__version__}")
print(f"Keras version: {keras.__version__}")

# Building a neural network with Keras Sequential API
# Scenario: classify neuron types from 6 electrophysiological features

model = keras.Sequential(
    [
        # Input layer: specify the shape of one example
        keras.Input(shape=(6,)),
        # Hidden layer 1: 64 neurons, ReLU activation
        # 6 inputs × 64 neurons + 64 biases = 448 parameters
        layers.Dense(64, activation="relu"),
        # Dropout: randomly zero out 30% of neurons during training
        # Prevents overfitting by forcing the network not to rely on any
        # single neuron — a form of ensemble learning
        layers.Dropout(0.3),
        # Hidden layer 2: 32 neurons, ReLU activation
        layers.Dense(32, activation="relu"),
        layers.Dropout(0.2),
        # Output layer: 3 neurons (one per neuron type)
        # Softmax converts raw scores to probabilities that sum to 1
        layers.Dense(3, activation="softmax"),
    ]
)

# Display the architecture — including the number of parameters in each layer
model.summary()
print()

# Compiling: Choosing How the Network Learns
model.compile(
    optimizer="adam",  # Adam: adaptive learning rate optimizer
    # Almost always a good first choice
    loss="sparse_categorical_crossentropy",
    # Use this when labels are integers (0, 1, 2)
    # Use 'categorical_crossentropy' if labels are one-hot encoded
    # Use 'binary_crossentropy' for binary (0/1) classification
    # Use 'mean_squared_error' for regression
    metrics=["accuracy"],  # Tracked but not optimized
)

# Generate synthetic electrophysiology dataset
# 6 features: AP amplitude, half-width, AHP depth, AHP duration, ISI mean, ISI CV
X, y = make_classification(
    n_samples=600,
    n_features=6,
    n_informative=5,
    n_redundant=0,
    n_classes=3,
    n_clusters_per_class=1,
    random_state=42,
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features — ALWAYS scale before feeding to a neural network
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Train the model
history = model.fit(
    X_train_s,
    y_train,
    epochs=100,  # Number of full passes through the training data
    batch_size=32,  # Number of examples per gradient update
    # Smaller batches: noisier gradients, slower per epoch
    # Larger batches: more stable gradients, faster per epoch
    # 32-64 is a standard starting point
    validation_split=0.2,
    # Hold out 20% of training data as validation set
    # Used to monitor overfitting during training — NOT used for final evaluation
    verbose=1,  # Print progress (set to 0 to suppress)
)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Loss curves
axes[0].plot(history.history["loss"], label="Train loss", color="#3498db", linewidth=2)
axes[0].plot(history.history["val_loss"], label="Val loss", color="#e74c3c", linewidth=2)
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Loss")
axes[0].set_title("Training vs Validation Loss")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Accuracy curves
axes[1].plot(history.history["accuracy"], label="Train acc", color="#3498db", linewidth=2)
axes[1].plot(history.history["val_accuracy"], label="Val acc", color="#e74c3c", linewidth=2)
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Accuracy")
axes[1].set_title("Training vs Validation Accuracy")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figure_9-5_training_curves.png", dpi=150)

# Evaluate on the test set (held out from ALL training decisions)
test_loss, test_accuracy = model.evaluate(X_test_s, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy:.1%}")
print(f"Test loss:     {test_loss:.4f}")

# Get class probabilities for each test example
probabilities = model.predict(X_test_s)  # shape: (n_test, n_classes)
print(f"\nProbabilities shape: {probabilities.shape}")
print(f"Example probabilities (first test sample): {probabilities[0].round(3)}")
print(f"Sum (should be 1.0): {probabilities[0].sum():.4f}")

# Convert probabilities to class predictions
y_pred = np.argmax(probabilities, axis=1)

neuron_types = ["Fast-spiking", "Regular-spiking", "Bursting"]
print("\nDetailed classification report:")
print(classification_report(y_test, y_pred, target_names=neuron_types))
print()

# ------------------------------------------------
# Early Stopping: Automated Overfitting Prevention

early_stopping = EarlyStopping(
    monitor="val_loss",  # Watch the validation loss
    patience=15,  # Stop after 15 epochs without improvement
    restore_best_weights=True,  # Revert to best weights, not final weights
)

# Rebuild and retrain with early stopping
model2 = keras.Sequential(
    [
        keras.Input(shape=(6,)),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(32, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(3, activation="softmax"),
    ]
)
model2.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

history2 = model2.fit(
    X_train_s,
    y_train,
    epochs=500,  # Set high — early stopping will decide when to stop
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=0,
)

stopped_at = len(history2.history["loss"])
print(f"Training stopped at epoch {stopped_at}")
print(f"Best validation accuracy: {max(history2.history['val_accuracy']):.1%}")
print()
