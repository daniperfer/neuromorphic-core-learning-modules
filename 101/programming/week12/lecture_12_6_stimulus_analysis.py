"""
Lecture 12.6: Tuning Curves and Stimulus-Response Analysis
"""

import matplotlib.pyplot as plt
import numpy as np

# from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit

np.random.seed(21)

# --- Experiment parameters ---
orientations = np.arange(0, 360, 45)  # degrees: 0, 45, 90, ..., 315
n_trials = 15
stim_duration = 0.5  # seconds per trial
baseline_rate = 5.0  # Hz (spontaneous firing)
peak_rate = 40.0  # Hz (response at preferred orientation)
preferred_ori = 90.0  # degrees
kappa = 2.5  # von Mises concentration (higher = sharper tuning)


def von_mises_rate(orientation_deg, preferred_deg, peak_rate, baseline_rate, kappa):
    """
    Compute expected firing rate for a given orientation.
    Uses a von Mises (circular Gaussian) tuning function.
    """
    diff_rad = np.deg2rad(orientation_deg - preferred_deg)
    tuning = np.exp(kappa * np.cos(diff_rad)) / np.exp(kappa)
    return baseline_rate + (peak_rate - baseline_rate) * tuning


def simulate_tuning_trial(rate_hz, duration):
    """Simulate a single Poisson spike train of given duration."""
    if rate_hz <= 0:
        return np.array([])
    n_expected = int(rate_hz * duration * 3)
    isis = np.random.exponential(1.0 / rate_hz, size=n_expected)
    times = np.cumsum(isis)
    return times[times < duration]


# --- Generate all trials ---
# spike_data[orientation][trial] = array of spike times
spike_data = {}
for ori in orientations:
    rate = von_mises_rate(ori, preferred_ori, peak_rate, baseline_rate, kappa)
    spike_data[ori] = [simulate_tuning_trial(rate, stim_duration) for _ in range(n_trials)]

# --- Preview: print mean spike counts ---
print(f"{'Orientation':>12}  {'Expected Rate':>14}  {'Observed Rate':>14}")
print("-" * 45)
for ori in orientations:
    expected = von_mises_rate(ori, preferred_ori, peak_rate, baseline_rate, kappa)
    counts = [len(t) for t in spike_data[ori]]
    observed = np.mean(counts) / stim_duration
    print(f"{ori:>11}°  {expected:>13.1f} Hz  {observed:>13.1f} Hz")
print()

# --------------------------
# Computing the Tuning Curve


def compute_tuning_curve(spike_data, orientations, stim_duration):
    """
    Compute mean firing rate and SEM for each stimulus condition.

    Params
    ------
    spike_data    : dict mapping orientation (degrees) → list of spike arrays
    orientations  : array of stimulus orientations in degrees
    stim_duration : float, duration of each stimulus presentation in seconds

    Returns
    -------
    mean_rates : 1D array of mean firing rate per orientation (Hz)
    sem_rates  : 1D array of standard error of the mean (Hz)
    """
    mean_rates = np.zeros(len(orientations))
    sem_rates = np.zeros(len(orientations))

    for i, ori in enumerate(orientations):
        counts = np.array([len(spikes) for spikes in spike_data[ori]])
        rates = counts / stim_duration
        mean_rates[i] = rates.mean()
        sem_rates[i] = rates.std(ddof=1) / np.sqrt(len(rates))

    return mean_rates, sem_rates


mean_rates, sem_rates = compute_tuning_curve(spike_data, orientations, stim_duration)

# Print the tuning curve data
print(f"\n{'Orientation':>12}  {'Mean Rate (Hz)':>15}  {'SEM':>8}")
print("-" * 40)
for ori, mu, se in zip(orientations, mean_rates, sem_rates):
    bar = "█" * int(mu / 2)
    print(f"{ori:>11}°  {mu:>14.2f}  {se:>7.2f}  {bar}")
print()

# -------------------------
# Plotting the Tuning Curve

# --- Prepare a smooth interpolated curve for overlay ---
ori_fine = np.linspace(0, 315, 500)
rate_fine = np.array(
    [von_mises_rate(o, preferred_ori, peak_rate, baseline_rate, kappa) for o in ori_fine]
)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# --- Left panel: Cartesian tuning curve ---
axes[0].bar(
    orientations, mean_rates, width=30, color="steelblue", alpha=0.7, label="Observed mean ± SEM"
)
axes[0].errorbar(
    orientations, mean_rates, yerr=sem_rates, fmt="none", color="black", capsize=4, linewidth=1.5
)
axes[0].plot(ori_fine, rate_fine, "r--", linewidth=2.0, label="True von Mises")
axes[0].set_xlabel("Orientation (degrees)")
axes[0].set_ylabel("Firing Rate (Hz)")
axes[0].set_xticks(orientations)
axes[0].set_title("Orientation Tuning Curve")
axes[0].legend()
axes[0].set_ylim(0, None)

# --- Right panel: Polar plot ---
# Duplicate the first point to close the circle
theta = np.deg2rad(np.append(orientations, orientations[0]))
r = np.append(mean_rates, mean_rates[0])
r_true = np.append(
    [von_mises_rate(o, preferred_ori, peak_rate, baseline_rate, kappa) for o in orientations],
    von_mises_rate(orientations[0], preferred_ori, peak_rate, baseline_rate, kappa),
)

ax_polar = fig.add_subplot(1, 2, 2, projection="polar")
ax_polar.plot(theta, r, "o-", color="steelblue", linewidth=2.0, markersize=7, label="Observed")
ax_polar.plot(np.deg2rad(ori_fine), rate_fine, "r--", linewidth=1.5, label="True tuning")
ax_polar.fill(theta, r, alpha=0.2, color="steelblue")
ax_polar.set_title("Polar Tuning Curve", pad=15)
ax_polar.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

# Remove the default subplot 122 that we replaced with polar
fig.delaxes(axes[1])

plt.tight_layout()
plt.savefig("figure_12-6-1_tuning_curve.png", dpi=150, bbox_inches="tight")
print("Plotting tuning curve example completed...")

# ------------------------
# Fitting the Tuning Curve


def von_mises_func(ori_deg, preferred_deg, peak_rate, baseline_rate, kappa):
    """Von Mises tuning function for curve fitting."""
    diff_rad = np.deg2rad(ori_deg - preferred_deg)
    tuning = np.exp(kappa * np.cos(diff_rad)) / np.exp(kappa)
    return baseline_rate + (peak_rate - baseline_rate) * tuning


# Initial parameter guesses
p0 = [
    orientations[np.argmax(mean_rates)],  # preferred orientation
    mean_rates.max(),  # peak rate
    mean_rates.min(),  # baseline rate
    2.0,
]  # kappa

# Parameter bounds: preferred in [0,360], rates >= 0, kappa > 0
bounds = ([0, 0, 0, 0.1], [360, 200, 200, 20.0])

try:
    popt, pcov = curve_fit(
        von_mises_func, orientations, mean_rates, p0=p0, bounds=bounds, maxfev=5000
    )
    perr = np.sqrt(np.diag(pcov))

    print("\nVon Mises Fit Results:")
    print(f"  Preferred orientation:  {popt[0]:.1f} ± {perr[0]:.1f}°  (true: {preferred_ori}°)")
    print(f"  Peak firing rate:       {popt[1]:.1f} ± {perr[1]:.1f} Hz (true: {peak_rate} Hz)")
    print(f"  Baseline firing rate:   {popt[2]:.1f} ± {perr[2]:.1f} Hz (true: {baseline_rate} Hz)")
    print(f"  Kappa (concentration):  {popt[3]:.2f} ± {perr[3]:.2f}  (true: {kappa})")

    # Plot fit overlay
    ori_fit = np.linspace(0, 360, 500)
    rate_fit = von_mises_func(ori_fit, *popt)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(
        orientations,
        mean_rates,
        width=30,
        color="steelblue",
        alpha=0.6,
        label="Observed mean ± SEM",
    )
    ax.errorbar(orientations, mean_rates, yerr=sem_rates, fmt="none", color="black", capsize=4)
    ax.plot(ori_fit, rate_fit, "r-", linewidth=2.5, label="Von Mises fit")
    ax.set_xlabel("Orientation (degrees)")
    ax.set_ylabel("Firing Rate (Hz)")
    ax.set_title(
        f"Tuning Curve Fit — Preferred: {popt[0]:.0f}°, "
        f"Peak: {popt[1]:.1f} Hz, κ = {popt[3]:.2f}"
    )
    ax.legend()
    plt.tight_layout()
    plt.savefig("figure_12-6-2_tuning_curve_fit.png", dpi=150, bbox_inches="tight")

except RuntimeError as e:
    print(f"Curve fit did not converge: {e}")
print("Fitting curve example completed...")

# ------------------------------------
# The Raster + PSTH View Per Condition

fig, axes = plt.subplots(4, 2, figsize=(13, 14))
axes = axes.flatten()

bin_width = 0.025  # 25 ms bins

for idx, ori in enumerate(orientations):
    ax = axes[idx]
    trials = spike_data[ori]
    n_t = len(trials)

    # PSTH counts
    edges = np.arange(0, stim_duration + bin_width, bin_width)
    psth = np.zeros(len(edges) - 1)
    for spikes in trials:
        counts, _ = np.histogram(spikes, bins=edges)
        psth += counts
    psth_rate = psth / (n_t * bin_width)
    bin_centers = (edges[:-1] + edges[1:]) / 2

    # Raster (offset each trial vertically)
    for t_idx, spikes in enumerate(trials):
        ax.eventplot(spikes, lineoffsets=t_idx + 1, linelengths=0.7, color="black", linewidths=0.5)

    # PSTH overlaid as filled area (scaled to fit raster y-range)
    ax_twin = ax.twinx()
    ax_twin.fill_between(bin_centers, psth_rate, alpha=0.3, color="steelblue")
    ax_twin.plot(bin_centers, psth_rate, color="steelblue", linewidth=1.2)
    ax_twin.set_ylim(0, peak_rate * 1.5)
    ax_twin.set_ylabel("Rate (Hz)", color="steelblue", fontsize=8)

    expected = von_mises_rate(ori, preferred_ori, peak_rate, baseline_rate, kappa)
    ax.set_title(f"{ori}°  (expected: {expected:.0f} Hz)", fontsize=9)
    ax.set_xlim(0, stim_duration)
    ax.set_ylim(0, n_t + 1)
    ax.set_xlabel("Time (s)", fontsize=8)
    ax.set_ylabel("Trial", fontsize=8)

plt.suptitle("Raster + PSTH Per Orientation — All 8 Conditions", fontsize=12, y=1.01)
plt.tight_layout()
plt.savefig("figure_12-6-3_raster_psth_per_condition.png", dpi=150, bbox_inches="tight")
print("Raster + PSTH example completed...")
