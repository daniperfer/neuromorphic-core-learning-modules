"""
Lecture 8.6: Saving Publication-Quality Figures
"""

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 6))
t = np.linspace(0, 10, 1000)
ax.plot(t, np.sin(t) * 20 - 55, "b-", linewidth=2)
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Voltage (mV)")
ax.set_title("Sample Neural Recording")

plt.tight_layout()

# PNG — best for presentations, posters, and web
# Lossless compression, transparent background supported
plt.savefig("figure_8-6-1.png", dpi=300, bbox_inches="tight", facecolor="white")

# PDF — best for publications and sharing with collaborators
# Vector format: infinitely scalable, editable in Illustrator/Inkscape
plt.savefig("figure_8-6-1.pdf", bbox_inches="tight", facecolor="white")

# SVG — best for editing individual figure elements
# Opens directly in Inkscape (free) or Adobe Illustrator
plt.savefig("figure_8-6-1.svg", bbox_inches="tight")

# TIFF — required by many journals for final submission
# Use 600 DPI for line art, 300 DPI for photographic/halftone content
plt.savefig("figure_8-6-1.tiff", dpi=600, bbox_inches="tight")

print("Figure saved in four formats example completed...")

# === Journal figure size conventions ===
# Single-column figure:  figsize=(3.5, 3.5) or (3.5, 2.8)
# Double-column figure:  figsize=(7.0, 5.0) or (7.0, 3.5)
# Maximum height:        9 inches (most journals)
# Most journals use pt font sizes of 7-8pt minimum for axis labels
# at print size — scale your rcParams accordingly

# === Presentation slide conventions ===
# Widescreen 16:9 slide: figsize=(16, 9)  or  figsize=(12, 6.75)
# Standard 4:3 slide:    figsize=(10, 7.5)
# A single large figure per slide: figsize=(10, 7) works well

# === Rules that apply in every context ===
# 1. Call plt.tight_layout() before plt.savefig()
# 2. Always specify dpi=300 minimum for raster formats
# 3. Always use bbox_inches='tight' to prevent label clipping
# 4. Always use facecolor='white' for clean raster backgrounds
# 5. For journal submission: check the specific journal's guide
#    — some require CMYK color mode, which needs post-processing
#    — some specify exact point sizes for axis labels
#    — some prohibit certain colormaps or require grayscale-compatible figures

# Step 1: Set figure size to match intended print size
fig, ax = plt.subplots(figsize=(3.5, 3.5))

# Step 2: Plot your data
t = np.linspace(0, 500, 5000)
voltage = -70 + np.cumsum(np.random.randn(5000)) * 0.1
ax.plot(t, voltage, "k-", linewidth=0.8)
ax.axhline(-55, color="red", linestyle="--", linewidth=1, label="Threshold")

# Step 3: Label at appropriate point sizes for the print size
ax.set_xlabel("Time (ms)", fontsize=8)
ax.set_ylabel("Voltage (mV)", fontsize=8)
ax.set_title("Membrane Potential", fontsize=9)
ax.legend(fontsize=7)
ax.tick_params(labelsize=7)

# Step 4: Remove spines for clean professional appearance
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Step 5: Apply tight layout before saving
plt.tight_layout()

# Step 6: Save in both vector (for journal) and raster (for slides)
filename = "figure_8-6-2_1a"
plt.savefig(f"{filename}.pdf", bbox_inches="tight", facecolor="white")
plt.savefig(f"{filename}.png", dpi=300, bbox_inches="tight", facecolor="white")

print(f"Saved {filename}.pdf and {filename}.png")
