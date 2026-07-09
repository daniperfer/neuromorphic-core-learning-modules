# Assignment 8: Neural Data Visualization Dashboard
# Student Name: [YOUR NAME]
# Date: [DATE]

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

# ── Experiment parameters ──────────────────────────────────────────────────────
np.random.seed(42)
N_NEURONS = 10
N_TRIALS = 20
DURATION = 1000  # ms
STIMULUS_TIME = 300  # ms

# ── PART 1: Generate spike data ───────────────────────────────────────────────
# Create a list-of-lists structure:
#   all_spikes[neuron][trial] = array of spike times (ms)
#
# Each neuron should have:
#   - Background firing (low rate, ~5 Hz) throughout the trial
#   - An elevated response in the 300–500 ms window (Poisson-distributed,
#     different mean rate per neuron so some neurons respond more than others)
#
# Hint: np.random.poisson() draws a random spike count;
#       np.random.uniform() generates random spike times within a window.

all_spikes = []  # all_spikes[neuron_idx][trial_idx] = spike time array

for neuron in range(N_NEURONS):
    neuron_spikes = []
    # TODO: Define this neuron's response strength
    # (e.g., response_rate = np.random.uniform(5, 25))

    for trial in range(N_TRIALS):
        # TODO: Generate background spikes (hint: ~5 background spikes per trial)
        background = ...

        # TODO: Generate response spikes in 300–500 ms window
        response = ...

        # TODO: Combine and sort spike times
        spikes = ...
        neuron_spikes.append(spikes)

    all_spikes.append(neuron_spikes)


# ── PART 2: Set up the figure ─────────────────────────────────────────────────
plt.rcParams.update(
    {
        "font.size": 11,
        "axes.labelsize": 11,
        "axes.titlesize": 12,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

fig = plt.figure(figsize=(16, 12))
fig.suptitle("Neural Population Analysis Dashboard", fontsize=16, fontweight="bold")
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# Panel handles — do not rename these variables
ax_raster = fig.add_subplot(gs[0, :])  # Top row, full width
ax_psth = fig.add_subplot(gs[1, 0])  # Middle left
ax_isi = fig.add_subplot(gs[1, 1])  # Middle center
ax_corr = fig.add_subplot(gs[1, 2])  # Middle right
ax_bar = fig.add_subplot(gs[2, :2])  # Bottom left + center
ax_stats = fig.add_subplot(gs[2, 2])  # Bottom right (text panel)
ax_stats.axis("off")


# ── PART 3: Raster plot ───────────────────────────────────────────────────────
# Plot spike trains for all 10 neurons × 20 trials.
# Each "row" in the raster = one (neuron, trial) combination.
# Color-code by neuron (use a colormap or a list of 10 colors).
# Add a vertical dashed line at STIMULUS_TIME.
#
# Hint: row_index = neuron * N_TRIALS + trial

# TODO: Your raster code here

ax_raster.set_xlim(0, DURATION)
ax_raster.set_xlabel("Time (ms)")
ax_raster.set_ylabel("Neuron × Trial")
ax_raster.set_title(f"Spike Raster — {N_NEURONS} Neurons × {N_TRIALS} Trials")
ax_raster.set_yticks([])


# ── PART 4: PSTH ──────────────────────────────────────────────────────────────
# Pool all spikes from all neurons and all trials into one array.
# Histogram with 20 ms bins.
# Convert spike counts to firing rate (Hz):
#   rate = count / (N_NEURONS * N_TRIALS) / (bin_size_ms / 1000)
# Add a vertical line at STIMULUS_TIME.

# TODO: Your PSTH code here

ax_psth.set_xlabel("Time (ms)")
ax_psth.set_ylabel("Firing Rate (Hz)")
ax_psth.set_title("Population PSTH")


# ── PART 5: ISI histogram ─────────────────────────────────────────────────────
# Find the most active neuron (highest total spike count across all trials).
# Collect all ISIs for that neuron (np.diff on each trial's spike array,
# then concatenate across trials).
# Plot as a histogram. Add a vertical line at the mean ISI.
# Label the title with the neuron index and its spike count.

# TODO: Your ISI histogram code here

ax_isi.set_xlabel("ISI (ms)")
ax_isi.set_ylabel("Count")
# ax_isi.set_title(...)   ← fill in with neuron index


# ── PART 6: Correlation heatmap ───────────────────────────────────────────────
# For each neuron, build a binary spike-count vector across time:
#   Divide the trial into 50 ms bins; count spikes in each bin per trial,
#   then average across trials → a 1D rate vector of length (DURATION/50).
# Stack 10 such vectors into a (10 × n_bins) matrix.
# Compute np.corrcoef() on the matrix (produces a 10×10 correlation matrix).
# Display with ax_corr.imshow(), colormap 'RdBu_r', vmin=-1, vmax=1.
# Add a colorbar. Label axes.

# TODO: Your correlation heatmap code here

ax_corr.set_xlabel("Neuron #")
ax_corr.set_ylabel("Neuron #")
ax_corr.set_title("Pairwise Neuron Correlations")


# ── PART 7: Firing rate bar chart ─────────────────────────────────────────────
# For each neuron, compute:
#   mean_rate = total spikes / (N_TRIALS * DURATION / 1000)   [Hz]
#   sem_rate  = std of per-trial rates / sqrt(N_TRIALS)
# Plot as a bar chart with error bars (capsize=5).
# Color bars by neuron index using the same colormap you used in the raster.
# Add a horizontal dashed line at the population mean rate.

# TODO: Your bar chart code here

ax_bar.set_xlabel("Neuron #")
ax_bar.set_ylabel("Mean Firing Rate (Hz)")
ax_bar.set_title("Mean Firing Rate per Neuron (± SEM)")


# ── PART 8: Statistics text panel ────────────────────────────────────────────
# Compute and display the following:
#   - Total spikes recorded
#   - Mean firing rate across all neurons (Hz)
#   - Most active neuron index and its rate
#   - Least active neuron index and its rate
#   - Mean pairwise correlation (off-diagonal elements of the corr matrix)
#   - Stimulus response ratio:
#       (mean rate 300–500 ms) / (mean rate 0–300 ms)
#
# Format as a monospace text block inside a rounded bbox (facecolor='lightyellow').

# TODO: Your statistics panel code here


# ── Save and show ─────────────────────────────────────────────────────────────
plt.savefig("assignment8_dashboard.png", dpi=300, bbox_inches="tight", facecolor="white")
print("Dashboard saved as assignment8_dashboard.png")
plt.show()
