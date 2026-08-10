"""
Lecture 12.7: Putting It Together — Multi-Neuron Population Analysis
"""

from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(55)

# --- Population parameters ---
n_neurons = 8
orientations = np.arange(0, 360, 45)  # 8 stimulus conditions
n_trials = 20
stim_duration = 0.5  # seconds

# Each neuron has a different preferred orientation, evenly tiling 360°
preferred_oris = np.linspace(0, 315, n_neurons)
peak_rates = np.random.uniform(25, 55, n_neurons)  # Hz
baseline_rates = np.random.uniform(2, 10, n_neurons)  # Hz
kappas = np.random.uniform(1.5, 4.0, n_neurons)  # tuning sharpness

print("Population parameters:")
print(f"{'Neuron':>7}  {'Pref (°)':>9}  {'Peak (Hz)':>10}  {'Baseline':>9}  {'Kappa':>6}")
print("-" * 50)
for i in range(n_neurons):
    print(
        f"{i:>7}  {preferred_oris[i]:>9.1f}  {peak_rates[i]:>10.1f}  "
        f"{baseline_rates[i]:>9.1f}  {kappas[i]:>6.2f}"
    )


def von_mises_rate(ori_deg, preferred_deg, peak_rate, baseline_rate, kappa):
    """Von Mises rate."""
    diff_rad = np.deg2rad(ori_deg - preferred_deg)
    tuning = np.exp(kappa * np.cos(diff_rad)) / np.exp(kappa)
    return baseline_rate + (peak_rate - baseline_rate) * tuning


def simulate_trial_spikes(rate_hz, duration):
    """Simulate trials."""
    if rate_hz <= 0:
        return np.array([])
    isis = np.random.exponential(1.0 / rate_hz, size=int(rate_hz * duration * 3))
    times = np.cumsum(isis)
    return times[times < duration]


# spike_data[neuron_idx][orientation][trial] = spike times array
spike_data: Dict[int, Dict[int, List]] = {}
for n in range(n_neurons):
    spike_data[n] = {}
    for ori in orientations:
        rate = von_mises_rate(ori, preferred_oris[n], peak_rates[n], baseline_rates[n], kappas[n])
        spike_data[n][ori] = [simulate_trial_spikes(rate, stim_duration) for _ in range(n_trials)]
print()

# ------------------------------
# The Population Response Matrix


def build_population_matrix(spike_data, n_neurons, orientations, stim_duration):
    """
    Build the population response matrix.

    Returns
    -------
    R : array of shape (n_neurons, n_orientations)
        Mean firing rate (Hz) for each neuron × orientation combination.
    """
    R = np.zeros((n_neurons, len(orientations)))
    for n in range(n_neurons):
        for j, ori in enumerate(orientations):
            counts = [len(spikes) for spikes in spike_data[n][ori]]
            R[n, j] = np.mean(counts) / stim_duration
    return R


R = build_population_matrix(spike_data, n_neurons, orientations, stim_duration)

# Visualize the population matrix as a heatmap
fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(R, aspect="auto", cmap="hot", interpolation="nearest")
ax.set_xticks(range(len(orientations)))
ax.set_xticklabels([f"{o}°" for o in orientations])
ax.set_yticks(range(n_neurons))
ax.set_yticklabels([f"N{i} (pref {preferred_oris[i]:.0f}°)" for i in range(n_neurons)])
ax.set_xlabel("Stimulus Orientation")
ax.set_ylabel("Neuron")
ax.set_title("Population Response Matrix — Mean Firing Rate (Hz)")
plt.colorbar(im, ax=ax, label="Firing Rate (Hz)")
plt.tight_layout()
plt.savefig("figure_12-7-1_population_matrix.png", dpi=150, bbox_inches="tight")
print("Population example completed...")

# ---------------------
# The Population Vector


def population_vector_decode(firing_rates, preferred_oris_deg):
    """
    Decode stimulus orientation using the population vector method.

    Params
    ------
    firing_rates      : 1D array of firing rates for each neuron (Hz)
    preferred_oris_deg: 1D array of preferred orientations in degrees

    Returns
    -------
    decoded_ori : float, decoded orientation in degrees [0, 180)
    """
    # Use doubled angles to handle 180° periodicity of orientation
    theta = np.deg2rad(2 * preferred_oris_deg)
    x = np.sum(firing_rates * np.cos(theta))
    y = np.sum(firing_rates * np.sin(theta))
    decoded_rad = np.arctan2(y, x) / 2.0  # halve back to [0°, 180°)
    decoded_deg = np.rad2deg(decoded_rad) % 180
    return decoded_deg


# Decode each orientation from the population response matrix
print("\nPopulation Vector Decoding:")
print(f"{'True Ori':>9}  {'Decoded Ori':>12}  {'Error':>8}")
print("-" * 35)
for j, ori in enumerate(orientations):
    rates = R[:, j]
    decoded = population_vector_decode(rates, preferred_oris)
    error = abs(ori % 180 - decoded)
    error = min(error, 180 - error)  # circular distance
    print(f"{ori:>8}°  {decoded:>11.1f}°  {error:>7.1f}°")
print()

# --------------------------------
# Population Firing Rate Over Time


def population_rate_over_time(
    spike_data_neuron_ori, n_neurons, orientations, stim_duration, sigma_ms=25.0
):
    """
    Compute population-average firing rate over time for each orientation.

    Returns
    -------
    time_axis   : 1D array (seconds)
    pop_rates   : array of shape (n_orientations, n_time_bins)
    """
    dt_s = 0.001
    n_samp = int(stim_duration / dt_s)
    time_axis = np.arange(n_samp) * dt_s
    sigma_samp = sigma_ms / (dt_s * 1000)
    pop_rates = np.zeros((len(orientations), n_samp))

    for j, ori in enumerate(orientations):
        neuron_rates = np.zeros((n_neurons, n_samp))
        for n in range(n_neurons):
            # Average binary spike train across trials
            avg_binary = np.zeros(n_samp)
            for spikes in spike_data_neuron_ori[n][ori]:
                idx = (spikes / dt_s).astype(int)
                idx = idx[idx < n_samp]
                avg_binary[idx] += 1.0
            avg_binary /= n_trials
            smoothed = gaussian_filter1d(avg_binary, sigma=sigma_samp)
            neuron_rates[n] = smoothed / dt_s
        pop_rates[j] = neuron_rates.mean(axis=0)

    return time_axis, pop_rates


time_axis, pop_rates = population_rate_over_time(
    spike_data, n_neurons, orientations, stim_duration, sigma_ms=25.0
)

fig, ax = plt.subplots(figsize=(10, 5))
colors = plt.cm.hsv(np.linspace(0, 1, len(orientations)))
for j, ori in enumerate(orientations):
    ax.plot(time_axis * 1000, pop_rates[j], color=colors[j], linewidth=1.8, label=f"{ori}°")
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Population Mean Firing Rate (Hz)")
ax.set_title("Population Firing Rate Over Time — All Orientations")
ax.legend(title="Orientation", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig("figure_12-7-2_population_rate_over_time.png", dpi=150, bbox_inches="tight")
print("Population rate over time example completed...")

# ---------------------------------
# Dimensionality Reduction with PCA

# R has shape (n_neurons, n_orientations)
# For PCA we want each orientation to be a point in neuron-space
# So we transpose: X has shape (n_orientations, n_neurons)
X = R.T  # shape: (8 orientations, 8 neurons)

# Standardize across neurons (each neuron has unit variance)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

explained = pca.explained_variance_ratio_ * 100

print("\nPCA Explained Variance:")
for i, ev in enumerate(explained):
    bar = "█" * int(ev / 2)
    print(f" PC{i + 1}: {ev:5.1f}% {bar}")
print(f"  PC1 + PC2: {explained[0] + explained[1]:.1f}%")

# Plot the population trajectory in PC1-PC2 space
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

colors = plt.cm.hsv(np.linspace(0, 1, len(orientations)))

# --- Left: PC1 vs PC2 scatter ---
for j, ori in enumerate(orientations):
    axes[0].scatter(X_pca[j, 0], X_pca[j, 1], color=colors[j], s=120, zorder=5, label=f"{ori}°")
    axes[0].annotate(
        f"{ori}°", (X_pca[j, 0], X_pca[j, 1]), textcoords="offset points", xytext=(6, 4), fontsize=8
    )

# Connect points in order to show the circular trajectory
xy = np.vstack([X_pca[:, 0], X_pca[:, 1]]).T
xy_closed = np.vstack([xy, xy[0]])  # close the loop
axes[0].plot(xy_closed[:, 0], xy_closed[:, 1], "k--", linewidth=1.0, alpha=0.5)
axes[0].set_xlabel(f"PC1 ({explained[0]:.1f}% variance)")
axes[0].set_ylabel(f"PC2 ({explained[1]:.1f}% variance)")
axes[0].set_title("Population Responses in PC Space")
axes[0].axhline(0, color="gray", linewidth=0.6)
axes[0].axvline(0, color="gray", linewidth=0.6)

# --- Right: Scree plot ---
axes[1].bar(range(1, len(explained) + 1), explained, color="steelblue", edgecolor="white")
axes[1].plot(
    range(1, len(explained) + 1),
    np.cumsum(explained),
    "ro-",
    linewidth=1.5,
    markersize=6,
    label="Cumulative variance",
)
axes[1].set_xlabel("Principal Component")
axes[1].set_ylabel("Explained Variance (%)")
axes[1].set_title("Scree Plot — Population Response Matrix")
axes[1].legend()
axes[1].set_ylim(0, 105)

plt.tight_layout()
plt.savefig("figure_12-7-3_population_pca.png", dpi=150, bbox_inches="tight")
print("PCA example completed...\n")

# ----------------------------
# Using the Complete Framework


def week12_population_summary(spike_data, n_neurons, orientations, stim_duration, preferred_oris):
    """
    Compute and print a full population summary for a tuning experiment.

    Covers: per-neuron ISI stats, mean tuning curves, population vector
    decoding accuracy, and PCA dimensionality.
    """
    print("\n" + "=" * 55)
    print("  Week 12 Population Analysis Summary")
    print("=" * 55)

    # --- Per-neuron mean rate and CV ---
    print("\nPer-Neuron Firing Statistics:")
    print(f"  {'Neuron':>6}  {'Pref':>6}  {'Mean Rate':>10}  {'CV':>6}")
    print("  " + "-" * 35)
    for n in range(n_neurons):
        all_spikes = np.concatenate(
            [spikes for ori in orientations for spikes in spike_data[n][ori]]
        )
        all_spikes = np.sort(all_spikes)
        mean_rate = len(all_spikes) / (stim_duration * len(orientations) * n_trials)
        isis = np.diff(all_spikes)
        cv = isis.std() / isis.mean() if len(isis) > 1 else np.nan
        print(f"  {n:>6}  {preferred_oris[n]:>5.0f}°  " f"{mean_rate:>9.1f} Hz  {cv:>6.3f}")

    # --- Population matrix and decoding ---
    R = build_population_matrix(spike_data, n_neurons, orientations, stim_duration)

    errors = []
    for j, ori in enumerate(orientations):
        decoded = population_vector_decode(R[:, j], preferred_oris)
        err = abs(ori % 180 - decoded)
        errors.append(min(err, 180 - err))
    print("\nPopulation vector decoding:")
    print(f"  Mean absolute error:  {np.mean(errors):.1f}°")
    print(f"  Max absolute error:   {np.max(errors):.1f}°")

    # --- PCA ---
    X_scaled = StandardScaler().fit_transform(R.T)
    pca = PCA()
    pca.fit(X_scaled)
    ev = pca.explained_variance_ratio_ * 100
    print("\nPCA dimensionality:")
    print(f"  PC1 + PC2 capture:  {ev[0] + ev[1]:.1f}% of variance")
    print(f"  PCs needed for 90%: " f"{np.argmax(np.cumsum(ev) >= 90) + 1}")

    print("\n" + "=" * 55)


week12_population_summary(spike_data, n_neurons, orientations, stim_duration, preferred_oris)
print("\nComplete Population analysis example completed...")
