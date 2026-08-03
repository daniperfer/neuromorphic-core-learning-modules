"""
Lecture 8.1: Introduction to Matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np

# Create a time axis from 0 to 10 seconds, sampled at 100 points
time = np.linspace(0, 10, 100)

# Simulate a membrane potential oscillating around -70 mV
voltage = -70 + 5 * np.sin(time)

plt.plot(time, voltage)
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (mV)")
plt.title("Membrane Potential Oscillation")
plt.savefig("figure_8-1-1.png")
print("First figure example completed...")

# Create a figure with explicit size (width=10 inches, height=6 inches)
fig, ax = plt.subplots(figsize=(10, 6))

time = np.linspace(0, 5, 500)
voltage = -70 + np.random.randn(500) * 2  # Noisy membrane potential

# Plot the voltage trace
ax.plot(time, voltage, color="blue", linewidth=1, label="Vm")

# Add a horizontal dashed line at the action potential threshold
ax.axhline(y=-55, color="red", linestyle="--", label="Threshold")

# Label axes and title using the Axes object methods
ax.set_xlabel("Time (ms)", fontsize=12)
ax.set_ylabel("Voltage (mV)", fontsize=12)
ax.set_title("Membrane Potential Recording", fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figure_8-1-2_membrane_potential.png", dpi=300, bbox_inches="tight")
print("Second figure example completed...")

fig, ax = plt.subplots(figsize=(10, 6))
t = np.linspace(0, 10, 200)

ax.plot(t, np.sin(t), color="blue", linestyle="-", linewidth=2, label="Solid")
ax.plot(t, np.sin(t + 1), color="red", linestyle="--", linewidth=2, label="Dashed")
ax.plot(t, np.sin(t + 2), color="green", linestyle=":", linewidth=2, label="Dotted")
ax.plot(t, np.sin(t + 3), color="orange", linestyle="-.", linewidth=2, label="Dash-dot")

ax.legend()
ax.set_title("Line Style Options")
plt.tight_layout()
plt.savefig("figure_8-1-3_line_style_options.png", dpi=300, bbox_inches="tight")
print("Line style example figure completed...")
