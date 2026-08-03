"""
Lecture 8.2: Common Plot Types
"""

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

# Simulate stimulus intensity (%) and corresponding neural firing rate (Hz)
stimulus_intensity = np.random.uniform(0, 100, 50)
firing_rate = 0.5 * stimulus_intensity + np.random.randn(50) * 5
firing_rate = np.clip(firing_rate, 0, None)  # Firing rates can't be negative

fig, ax = plt.subplots(figsize=(8, 6))

scatter = ax.scatter(
    stimulus_intensity,
    firing_rate,
    c=firing_rate,  # Color each point by its firing rate
    cmap="hot",  # Colormap: low=dark, high=bright
    s=100,  # Point size
    alpha=0.7,
    edgecolors="black",
    linewidths=0.5,
)

# Add a colorbar to explain the color encoding
plt.colorbar(scatter, ax=ax, label="Firing Rate (Hz)")

ax.set_xlabel("Stimulus Intensity (%)", fontsize=12)
ax.set_ylabel("Firing Rate (Hz)", fontsize=12)
ax.set_title("Stimulus-Response Curve", fontsize=14)

# Fit and plot a linear trend line
z = np.polyfit(stimulus_intensity, firing_rate, 1)
p = np.poly1d(z)
x_line = np.linspace(0, 100, 100)
ax.plot(x_line, p(x_line), "b--", linewidth=2, label="Trend")
ax.legend()

plt.tight_layout()
plt.savefig("figure_8-2-1_scatter_plot.png", dpi=300, bbox_inches="tight")
print("Scatter plot example completed...")

# Simulate two types of neurons
regular_isi = np.random.normal(50, 5, 500)  # Regular firing: narrow bell curve
irregular_isi = np.random.exponential(50, 500)  # Irregular firing: exponential decay

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: regular neuron
axes[0].hist(regular_isi, bins=30, color="steelblue", edgecolor="white", alpha=0.8)
axes[0].axvline(
    np.mean(regular_isi),
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {np.mean(regular_isi):.1f}ms",
)
axes[0].set_xlabel("ISI (ms)")
axes[0].set_ylabel("Count")
axes[0].set_title("Regular Neuron")
axes[0].legend()

# Right panel: irregular neuron
axes[1].hist(irregular_isi, bins=30, color="coral", edgecolor="white", alpha=0.8)
axes[1].axvline(
    np.mean(irregular_isi),
    color="darkred",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {np.mean(irregular_isi):.1f}ms",
)
axes[1].set_xlabel("ISI (ms)")
axes[1].set_ylabel("Count")
axes[1].set_title("Irregular Neuron")
axes[1].legend()

plt.suptitle("ISI Distributions", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("figure_8-2-2_histogram_plot.png", dpi=300, bbox_inches="tight")
print("Histogram plot example completed...")

regions = ["Cortex", "Hippocampus", "Amygdala", "Cerebellum", "Thalamus"]
firing_rates = [15.2, 8.7, 22.4, 45.8, 18.3]
std_devs = [3.1, 2.2, 4.5, 8.2, 3.7]

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(regions))

bars = ax.bar(
    x,
    firing_rates,
    yerr=std_devs,
    capsize=5,
    color=["#2E75B6", "#FF6B35", "#4CAF50", "#9C27B0", "#FF9800"],
    edgecolor="black",
    linewidth=0.8,
    alpha=0.85,
)

# Annotate each bar with its exact value
for bar, rate in zip(bars, firing_rates):
    ax.text(
        bar.get_x() + bar.get_width(),
        bar.get_height() - 0.1,
        f"{rate}",
        ha="right",
        va="top",
        fontsize=10,
    )

ax.set_xticks(x)
ax.set_xticklabels(regions, fontsize=11)
ax.set_ylabel("Firing Rate (Hz)", fontsize=12)
ax.set_title("Average Firing Rates by Brain Region", fontsize=14)
ax.set_ylim(0, 60)
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("figure_8-2-3_bar_chart.png", dpi=300, bbox_inches="tight")
print("Bar chart example completed...")

conditions = {
    "Baseline": np.random.normal(15, 4, 50),
    "Stimulus": np.random.normal(28, 6, 50),
    "Post-stim": np.random.normal(18, 5, 50),
    "Drug": np.random.normal(8, 3, 50),
}

fig, ax = plt.subplots(figsize=(10, 6))

bp = ax.boxplot(
    conditions.values(),
    tick_labels=conditions.keys(),
    patch_artist=True,  # Fill boxes with color
    showfliers=True,
)  # Show outlier points

# Color each box individually
colors = ["#AED6F1", "#F1948A", "#A9DFBF", "#F9E79F"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)

ax.set_ylabel("Firing Rate (Hz)", fontsize=12)
ax.set_title("Firing Rate Distribution Across Conditions", fontsize=14)
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("figure_8-2-4_box_plot.png", dpi=300, bbox_inches="tight")
print("Box plot example completed...")
