# Assignment 7: Neural Population Analysis
# Student Name: [YOUR NAME]
# Date: [DATE]

import numpy as np

np.random.seed(42)  # Fix the random seed so results are reproducible

# Constants — do not change these
N_NEURONS = 20
N_TRIALS = 100
DURATION = 1000  # ms — length of each trial
BIN_SIZE = 10  # ms — time bin width for activity matrix


# ─────────────────────────────────────────────
# PART 1: Generate Spike Data (15 pts)
# ─────────────────────────────────────────────
# For each of the 20 neurons, simulate spike times across 100 trials.
# Each neuron should have its own baseline firing rate drawn from a
# realistic range. Use np.random.exponential() to generate ISIs,
# then np.cumsum() to convert ISIs into spike times.
# Keep only spikes that fall within [0, DURATION].
#
# Store your spike data in a structure that lets you access
# the spike times for neuron i, trial j.


# PART 1 CODE HERE


# ─────────────────────────────────────────────
# PART 2: ISI Analysis (20 pts)
# ─────────────────────────────────────────────
# For each neuron, compute ISI statistics across all trials combined.
# Use np.diff() to compute ISIs from spike times.
# Report for each neuron:
#   - Mean ISI
#   - Standard deviation of ISI
#   - Coefficient of variation (CV = std / mean)
#   - Firing pattern classification: Regular (CV < 0.3),
#     Irregular (0.3–0.8), or Bursty (CV > 0.8)


# PART 2 CODE HERE


# ─────────────────────────────────────────────
# PART 3: Build Activity Matrix (20 pts)
# ─────────────────────────────────────────────
# Create a 2D activity matrix of shape (N_NEURONS, n_bins) where
# n_bins = DURATION // BIN_SIZE.
# For each neuron, pool all spikes across trials and use np.histogram()
# to count spikes per time bin. Normalize to firing rate in Hz.
# The result should be a matrix where entry [i, j] is neuron i's
# average firing rate in time bin j.


# PART 3 CODE HERE


# ─────────────────────────────────────────────
# PART 4: Correlation Analysis (25 pts)
# ─────────────────────────────────────────────
# Compute the (N_NEURONS x N_NEURONS) correlation matrix from your
# activity matrix using np.corrcoef().
# Then identify all synchronous pairs: neuron pairs (i, j) where
# i < j and correlation > 0.7.
# Print each synchronous pair and their correlation value.
# Report how many synchronous pairs were found in total.


# PART 4 CODE HERE


# ─────────────────────────────────────────────
# PART 5: Population Firing Rate (20 pts)
# ─────────────────────────────────────────────
# Compute the population firing rate over time: the mean firing rate
# across all 20 neurons in each time bin (axis=0 of your activity matrix).
# Find and report:
#   - The time bin with the highest population activity
#   - The time bin with the lowest population activity
#   - The mean and standard deviation of population rate across all bins


# PART 5 CODE HERE


# ─────────────────────────────────────────────
# SAVE RESULTS
# ─────────────────────────────────────────────
# Save all key results to a single .npz file using np.savez().
# Include at minimum: the activity matrix, correlation matrix,
# and population firing rate array.


# SAVE CODE HERE


if __name__ == "__main__":
    print("=== NEURAL POPULATION ANALYSIS ===")
    # Your output should print a clear summary of results from all 5 parts
    print("✓ Results saved to assignment7_results.npz")
