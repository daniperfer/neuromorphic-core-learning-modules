"""
Lecture 8.5: Plot Customization and Style
"""

import matplotlib.pyplot as plt
import numpy as np

# Apply professional settings at the top of your script
plt.rcParams.update(
    {
        "font.size": 12,
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "legend.fontsize": 11,
        "axes.spines.top": False,  # Remove top border
        "axes.spines.right": False,  # Remove right border
    }
)

np.random.seed(42)
fig, ax = plt.subplots(figsize=(9, 6))

conditions = ["Control", "Drug A", "Drug B", "Drug A+B"]
means = [15.2, 28.4, 22.1, 35.8]
sems = [1.2, 2.1, 1.8, 2.5]
colors = ["#95A5A6", "#2980B9", "#27AE60", "#E74C3C"]

x = np.arange(len(conditions))
bars = ax.bar(
    x,
    means,
    yerr=sems,
    capsize=6,
    color=colors,
    edgecolor="black",
    linewidth=0.8,
    error_kw={"linewidth": 2, "ecolor": "black"},
)

# Add a significance bracket between Control and Drug A
ax.plot([0, 1], [31, 31], "k-", linewidth=1)
ax.text(0.5, 31.5, "**", ha="center", fontsize=14)

ax.set_xticks(x)
ax.set_xticklabels(conditions)
ax.set_ylabel("Firing Rate (Hz)")
ax.set_title("Effect of Pharmacological Agents on Firing Rate")
ax.set_ylim(0, 42)

plt.tight_layout()
plt.savefig("figure_8-5-1_rcParams.png", dpi=300, bbox_inches="tight")
print("Professional Plot Styling with rcParams example completed...")

# Colormap quick reference for neuroscience:
# 'hot'       — sequential, dark to bright; dramatic visual impact
# 'viridis'   — sequential, perceptually uniform, colorblind-safe
# 'RdBu_r'    — diverging; good for correlations and z-scores
# 'coolwarm'  — diverging; intuitive warm/cool distinction
# 'gray'      — for microscopy images and anatomical figures

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Use the same random data for fair comparison across colormaps
np.random.seed(42)
data = np.random.randn(20, 20)

colormaps = ["hot", "RdBu_r", "viridis"]
titles = ["Activity Map (hot)", "Correlation (RdBu_r)", "Density (viridis)"]

for ax, cmap, title in zip(axes, colormaps, titles):
    if cmap == "RdBu_r":
        im = ax.imshow(data, cmap="RdBu_r", vmin=-1, vmax=1)
    else:
        im = ax.imshow(data, cmap=cmap, aspect="equal")
    plt.colorbar(im, ax=ax)
    ax.set_title(title)

plt.suptitle("Colormap Selection Guide", fontsize=14)
plt.tight_layout()
plt.savefig("figure_8-5-2_colormaps.png", dpi=300, bbox_inches="tight")
print("Colormap Selection example completed...")

plt.rcdefaults()

"""
A more targeted approach for notebooks where you want different styles in
different cells is to use plt.style.context() as a context manager:

with plt.style.context('seaborn-v0_8-whitegrid'):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    plt.show()
# Outside the 'with' block, original rcParams are restored
"""
