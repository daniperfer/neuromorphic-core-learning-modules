# Assignment 7: Neural Population Analysis
# Student Name: Daniel Pereira
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
# realistic range.
# Use np.random.exponential() to generate ISIs,
# then np.cumsum() to convert ISIs into spike times.
# Keep only spikes that fall within [0, DURATION].
#
# Store your spike data in a structure that lets you access
# the spike times for neuron i, trial j.

baseline_firing_rate = np.random.normal(30, 10, N_NEURONS)
isis = np.random.exponential(baseline_firing_rate[:, None, None], (N_NEURONS, N_TRIALS, DURATION))
spike_times = np.cumsum(isis, axis=2)

# find the minimum spike time across all trials which is > DURATION
mask = spike_times > DURATION
idx = mask.argmax(axis=2)
end_trial_time = np.min(idx)
print(f"end_trial_time = {end_trial_time}")
spike_times = spike_times[:, :, :end_trial_time]
print(f"spike_times.shape = {spike_times.shape}")
i = 5
j = 6
print(f"neuron {i}, trial {j}, spike_times: {spike_times[i, j, :5]}...")
print(f"np.max(spike_times) = {np.max(spike_times)}")
print(f"np.min(spike_times) = {np.min(spike_times)}")

# Insert a non bursty neuron
# Regular: ISIs drawn from a tight normal distribution (mean 50ms, std 5ms)
regular_spikes = np.cumsum(np.random.normal(50, 5, (1, N_TRIALS, spike_times.shape[2])))
spike_times[0, :, :] = regular_spikes.reshape(1, N_TRIALS, spike_times.shape[2])


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

# Inter-spike intervals — np.diff computes the difference between consecutive elements
isi = np.diff(spike_times, axis=2)
mean_isi = np.mean(isi, axis=(1, 2))
std_isi = np.std(isi, axis=(1, 2))
cv_isi = std_isi / mean_isi  # coefficient of
print(mean_isi)
print(cv_isi)
print()

# ─────────────────────────────────────────────
# PART 3: Build Activity Matrix (20 pts)
# ─────────────────────────────────────────────
# Create a 2D activity matrix of shape (N_NEURONS, n_bins) where
# n_bins = DURATION // BIN_SIZE.
# For each neuron, pool all spikes across trials and use np.histogram()
# to count spikes per time bin. Normalize to firing rate in Hz.
# The result should be a matrix where entry [i, j] is neuron i's
# average firing rate in time bin j.

bins = np.arange(0, DURATION + BIN_SIZE, BIN_SIZE)
print(f"len(bins)= {len(bins)}")
activity = np.zeros((N_NEURONS, len(bins) - 1))  # one count per bin
for k in range(N_NEURONS):
    counts, _ = np.histogram(spike_times[k, :, :], bins=bins)
    activity[k, :] += counts
activity_rate = (activity / N_TRIALS) / (BIN_SIZE / 1000)  # spikes per trial per bin → Hz
print()


# ─────────────────────────────────────────────
# PART 4: Correlation Analysis (25 pts)
# ─────────────────────────────────────────────
# Compute the (N_NEURONS x N_NEURONS) correlation matrix from your
# activity matrix using np.corrcoef().
# Then identify all synchronous pairs: neuron pairs (i, j) where
# i < j and correlation > 0.7.
# Print each synchronous pair and their correlation value.
# Report how many synchronous pairs were found in total.

correlation = np.corrcoef(activity)
corr_indices = np.argwhere(correlation > 0.7)

# ─────────────────────────────────────────────
# PART 5: Population Firing Rate (20 pts)
# ─────────────────────────────────────────────
# Compute the population firing rate over time: the mean firing rate
# across all 20 neurons in each time bin (axis=0 of your activity matrix).
# Find and report:
#   - The time bin with the highest population activity
#   - The time bin with the lowest population activity
#   - The mean and standard deviation of population rate across all bins

mean_activities = np.mean(activity_rate, axis=0)
peak_activity_bin = np.argmax(mean_activities)
lowest_activity_bin = np.argmin(mean_activities)
mean_rate_bins = np.mean(mean_activities)
std_rate_bins = np.std(mean_activities)

# ─────────────────────────────────────────────
# SAVE RESULTS
# ─────────────────────────────────────────────
# Save all key results to a single .npz file using np.savez().
# Include at minimum: the activity matrix, correlation matrix,
# and population firing rate array.

# Save multiple arrays under named keys
filename_npz = "assignment_7_danielpereira.npz"
np.savez(
    filename_npz,
    activity=activity,
    correlation=correlation,
    population_rate=mean_activities,
)


if __name__ == "__main__":
    print("\n=== NEURAL POPULATION ANALYSIS ===")
    # Your output should print a clear summary of results from all 5 parts
    print("--- Part 2: ISI Analysis ---")
    for k in range(mean_isi.size):
        pattern = "Bursty"
        if cv_isi[k] < 0.3:
            pattern = "Regular"
        elif cv_isi[k] < 0.8:
            pattern = "Irregular"
        print(
            f"""Neuron {k:<3}: Mean
            ISI = {mean_isi[k]:<3.3f} ms | CV = {cv_isi[k]:<3.3f} | Pattern: {pattern}"""
        )
    print()

    print("--- Part 3: Build Activity Matrix ---")
    tbins = 8
    for k, neuron_activity_r in enumerate(activity_rate):
        print(
            f"""Neuron {k} activity
            rate (Hz) in first {tbins} bins: {neuron_activity_r[:tbins]}"""
        )
    print()
    for k, n_activity in enumerate(activity):
        print(f"Neuron {k:<3} activity spikes in first {tbins} bins: {n_activity[:tbins]}")
    print()

    print("--- Part 4: Correlation Analysis ---")
    pairs = 0
    for i, j in corr_indices:
        if i < j:
            print(f"Neurons {i} and {j}: r = {correlation[i,j]}")
            pairs += 1
    total_pairs = ((N_NEURONS * N_NEURONS) - N_NEURONS) / 2
    print(f"Total synchronous pairs found: {pairs} (Total would be {total_pairs})")
    print()

    print("--- Part 5: Population Firing Rate ---")
    print(
        f"""Peak activity bin: [{bins[peak_activity_bin]}, {bins[peak_activity_bin + 1]}) ms
        ({mean_activities[peak_activity_bin]:<3.3f} Hz)"""
    )
    print(
        f"""Lowest activity bin: [{bins[lowest_activity_bin]}, {bins[lowest_activity_bin + 1]}) ms
        ({mean_activities[lowest_activity_bin]:<3.3f} Hz)"""
    )
    print(f"Mean population rate: {mean_rate_bins} ± {std_rate_bins} Hz")
    print()

    print(f"✓ Results saved to {filename_npz}")
