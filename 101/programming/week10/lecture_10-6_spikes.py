"""
Lecture 10.6: Spike Detection from Raw Voltage Traces
"""

import matplotlib.pyplot as plt
import numpy as np

# from scipy import signal as sp_signal
from scipy.signal import butter, sosfiltfilt

np.random.seed(42)
fs = 30000  # Hz — standard spike sorting sampling rate
duration = 5  # seconds
t = np.arange(0, duration, 1 / fs)
n_samples = len(t)

print(f"Recording: {n_samples:,} samples at {fs} Hz ({duration} s)")
print(f"Time resolution: {1 / fs * 1000:.4f} ms per sample\n")


def make_spike_waveform(fs, duration_ms=2.5, amplitude=200):
    """
    Generate a realistic biphasic extracellular spike waveform.

    The waveform has a sharp negative trough (~0.4 ms post-onset),
    a positive rebound (~1.0 ms post-onset), and a slow return to baseline.

    Parameters
    ----------
    fs : float
        Sampling rate in Hz
    duration_ms : float
        Total waveform duration in milliseconds
    amplitude : float
        Peak-to-trough amplitude in µV

    Returns
    -------
    np.ndarray
        Spike waveform array
    """
    n = int(duration_ms * fs / 1000)
    t_wf = np.linspace(0, duration_ms, n)

    # Biphasic shape: negative trough + positive rebound
    trough = -amplitude * np.exp(-((t_wf - 0.4) ** 2) / (2 * 0.12**2))
    rebound = amplitude * 0.35 * np.exp(-((t_wf - 1.1) ** 2) / (2 * 0.25**2))
    slow_pos = amplitude * 0.08 * np.exp(-((t_wf - 2.0) ** 2) / (2 * 0.5**2))

    waveform = trough + rebound + slow_pos
    return waveform


# Visualize the canonical spike waveform
wf = make_spike_waveform(fs, amplitude=200)
t_wf_ms = np.linspace(0, 2.5, len(wf))

plt.figure(figsize=(7, 3.5))
plt.plot(t_wf_ms, wf, color="#2c4a8c", linewidth=2.0)
plt.axhline(0, color="gray", linewidth=0.5, linestyle="--")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (µV)")
plt.title("Canonical Extracellular Spike Waveform (Biphasic)")
plt.axvline(0.4, color="red", linewidth=0.7, linestyle=":", alpha=0.7, label="Trough")
plt.axvline(1.1, color="orange", linewidth=0.7, linestyle=":", alpha=0.7, label="Rebound")
plt.legend(fontsize=9)
plt.tight_layout()
plt.savefig("figure_10-6-1_spike_waveform_template.png", dpi=150)
print()


def simulate_neuron_spikes(firing_rate, duration, fs, refractory_ms=2.0, seed=None):
    """
    Generate spike times for a simulated neuron using a refractory Poisson process.

    Parameters
    ----------
    firing_rate : float
        Mean firing rate in Hz
    duration : float
        Recording duration in seconds
    fs : float
        Sampling rate in Hz
    refractory_ms : float
        Absolute refractory period in milliseconds
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    np.ndarray
        Array of spike times in seconds
    """
    rng = np.random.default_rng(seed)
    refractory_s = refractory_ms / 1000
    spike_times = []
    t_now = rng.exponential(1 / firing_rate)  # first spike

    while t_now < duration:
        spike_times.append(t_now)
        # Next spike: refractory + exponential waiting time
        isi = refractory_s + rng.exponential(1 / firing_rate)
        t_now += isi

    return np.array(spike_times)


# Two neurons: one close (large amplitude), one farther (small amplitude)
spike_times_1 = simulate_neuron_spikes(firing_rate=15, duration=duration, fs=fs, seed=1)
spike_times_2 = simulate_neuron_spikes(firing_rate=8, duration=duration, fs=fs, seed=2)

print(f"Neuron 1: {len(spike_times_1)} spikes, mean rate = {len(spike_times_1) / duration:.1f} Hz")
print(f"Neuron 2: {len(spike_times_2)} spikes, mean rate = {len(spike_times_2) / duration:.1f} Hz")

# Build the full broadband recording
wf_template_1 = make_spike_waveform(fs, amplitude=250)  # large, close neuron
wf_template_2 = make_spike_waveform(fs, amplitude=90)  # small, farther neuron
wf_len = len(wf_template_1)

# Start with thermal noise
noise_std = 25  # µV — typical electrode noise floor
raw_signal = noise_std * np.random.randn(n_samples)

# Add LFP background (low frequency, large amplitude)
lfp_bg = 80 * np.sin(2 * np.pi * 8 * t) + 40 * np.sin(2 * np.pi * 2 * t)
raw_signal += lfp_bg


# Embed spike waveforms at the simulated spike times
def embed_waveforms(signal, spike_times, waveform, fs):
    """Insert spike waveforms into the signal at the given spike times."""
    for st in spike_times:
        idx = int(st * fs)
        end = idx + len(waveform)
        if end < len(signal):
            signal[idx:end] += waveform
    return signal


raw_signal = embed_waveforms(raw_signal, spike_times_1, wf_template_1, fs)
raw_signal = embed_waveforms(raw_signal, spike_times_2, wf_template_2, fs)

print(f"\nRaw broadband signal: {len(raw_signal):,} samples")
print(f"Signal std: {np.std(raw_signal):.1f} µV")
print(f"Signal range: [{raw_signal.min():.1f}, {raw_signal.max():.1f}] µV")

# ---------------------------------------------
# High-Pass Filtering to Isolate Spike Activity


def highpass_filter(signal, cutoff_hz, fs, order=4):
    """Apply a zero-phase high-pass Butterworth filter."""
    nyquist = fs / 2
    sos = butter(order, cutoff_hz / nyquist, btype="high", output="sos")
    return sosfiltfilt(sos, signal)


# High-pass filter above 300 Hz to isolate spike activity
hp_signal = highpass_filter(raw_signal, cutoff_hz=300, fs=fs)

print(f"High-pass filtered signal std: {np.std(hp_signal):.1f} µV")

# Visualize 200 ms of raw and filtered signals
window_ms = 200
window_samples = int(window_ms * fs / 1000)
t_ms = t[:window_samples] * 1000

fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=True)

axes[0].plot(t_ms, raw_signal[:window_samples], color="#555555", linewidth=0.6)
axes[0].set_ylabel("Voltage (µV)")
axes[0].set_title("Broadband Recording (LFP + Spikes + Noise)")

axes[1].plot(t_ms, hp_signal[:window_samples], color="#2c4a8c", linewidth=0.6)
axes[1].set_ylabel("Voltage (µV)")
axes[1].set_xlabel("Time (ms)")
axes[1].set_title("High-Pass Filtered (> 300 Hz) — Spikes Visible Above Noise Floor")

# Mark known spike times from neuron 1 that fall in this window
for st in spike_times_1:
    st_ms = st * 1000
    if st_ms < window_ms:
        axes[1].axvline(st_ms, color="red", alpha=0.5, linewidth=0.8)
for st in spike_times_2:
    st_ms = st * 1000
    if st_ms < window_ms:
        axes[1].axvline(st_ms, color="orange", alpha=0.5, linewidth=0.8)

plt.tight_layout()
plt.savefig("figure_10-6-2_raw_vs_highpass.png", dpi=150)
print()

# -------------------------------
# Threshold-Based Spike Detection


def estimate_noise_std(signal):
    """
    Robust noise standard deviation estimate using the median absolute deviation.
    Insensitive to spike contamination of the signal.

    Reference: Quiroga et al., Neural Computation, 2004.
    """
    return np.median(np.abs(signal)) / 0.6745


def detect_spikes(signal, fs, threshold_multiplier=4.0, refractory_ms=2.0):
    """
    Detect spikes by negative threshold crossing with refractory period.

    Parameters
    ----------
    signal : np.ndarray
        High-pass filtered voltage trace
    fs : float
        Sampling rate in Hz
    threshold_multiplier : float
        Threshold = -threshold_multiplier * noise_std
        4.0 is the standard default (Quiroga et al. 2004)
    refractory_ms : float
        Minimum inter-spike interval in milliseconds

    Returns
    -------
    spike_samples : np.ndarray
        Sample indices of detected spike peaks
    threshold : float
        Threshold value used (in µV)
    noise_std : float
        Estimated noise standard deviation
    """
    noise_std = estimate_noise_std(signal)
    threshold = -threshold_multiplier * noise_std

    refractory_samples = int(refractory_ms * fs / 1000)

    spike_samples = []
    i = 0

    while i < len(signal) - 1:
        # Detect negative threshold crossing
        if signal[i] <= threshold:
            # Find the minimum (trough) within the next 2 ms
            search_end = min(i + int(2 * fs / 1000), len(signal))
            local_min_idx = i + np.argmin(signal[i:search_end])
            spike_samples.append(local_min_idx)
            # Enforce refractory period
            i = local_min_idx + refractory_samples
        else:
            i += 1

    return np.array(spike_samples), threshold, noise_std


# Detect spikes
spike_samples, threshold, noise_std = detect_spikes(hp_signal, fs, threshold_multiplier=4.0)
spike_times_detected = spike_samples / fs

print(f"Noise std estimate: {noise_std:.2f} µV")
print(f"Detection threshold: {threshold:.2f} µV")
print(f"Detected spikes: {len(spike_samples)}")
print(f"True spikes (both neurons): {len(spike_times_1) + len(spike_times_2)}")


# Evaluate detection accuracy
def count_matches(detected_times, true_times, tolerance_ms=1.5):
    """Count how many detected spikes match a true spike within tolerance."""
    tolerance_s = tolerance_ms / 1000
    matches = 0
    for dt in detected_times:
        if np.any(np.abs(true_times - dt) <= tolerance_s):
            matches += 1
    return matches


n_true_total = len(spike_times_1) + len(spike_times_2)
n_detected = len(spike_times_detected)
n_true_hits = count_matches(spike_times_detected, np.concatenate([spike_times_1, spike_times_2]))

precision = n_true_hits / n_detected if n_detected > 0 else 0
recall = n_true_hits / n_true_total if n_true_total > 0 else 0

print("\nDetection performance (tolerance: 1.5 ms):")
print(f"  Precision: {precision:.3f}  ({n_true_hits}/{n_detected} detected were real)")
print(f"  Recall:    {recall:.3f}  ({n_true_hits}/{n_true_total} real spikes found)")
print(f"  F1 score:  {2 * precision * recall / (precision + recall):.3f}\n")

# -----------------------------------
# Visualizing Detection on the Signal

# Plot detection results over a 500 ms window
window_ms = 500
window_samples = int(window_ms * fs / 1000)
t_ms_500 = t[:window_samples] * 1000

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(t_ms_500, hp_signal[:window_samples], color="#2c4a8c", linewidth=0.5, alpha=0.8)
ax.axhline(
    threshold,
    color="red",
    linewidth=1.2,
    linestyle="--",
    label=f"Threshold: {threshold:.1f} µV ({4.0}σ)",
)
ax.axhline(0, color="gray", linewidth=0.4, linestyle=":")

# Mark detected spikes
detected_in_window = spike_samples[spike_samples < window_samples]
ax.scatter(
    detected_in_window / fs * 1000,
    hp_signal[detected_in_window],
    color="red",
    s=30,
    zorder=5,
    label=f"Detected spikes ({len(detected_in_window)})",
)

ax.set_xlabel("Time (ms)")
ax.set_ylabel("Voltage (µV)")
ax.set_title("Spike Detection: Threshold Crossing on High-Pass Filtered Signal")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("figure_10-6-3_spike_detection_result.png", dpi=150)
print()

# ---------------------------------------
# Extracting and Aligning Spike Waveforms


def extract_waveforms(signal, spike_samples, fs, pre_ms=0.5, post_ms=2.0):
    """
    Extract spike waveform snippets centered on detected spike troughs.

    Parameters
    ----------
    signal : np.ndarray
        High-pass filtered recording
    spike_samples : np.ndarray
        Sample indices of detected spike peaks (troughs)
    fs : float
        Sampling rate in Hz
    pre_ms : float
        Time before the trough to include (ms)
    post_ms : float
        Time after the trough to include (ms)

    Returns
    -------
    waveforms : np.ndarray
        Shape (n_spikes, n_samples_per_waveform)
    wf_time_ms : np.ndarray
        Time axis for waveforms in ms (0 = trough)
    """
    pre_samples = int(pre_ms * fs / 1000)
    post_samples = int(post_ms * fs / 1000)
    wf_len = pre_samples + post_samples

    waveforms = []
    valid_spikes = []

    for idx in spike_samples:
        start = idx - pre_samples
        end = idx + post_samples
        if start >= 0 and end < len(signal):
            waveforms.append(signal[start:end])
            valid_spikes.append(idx)

    waveforms = np.array(waveforms)
    wf_time_ms = np.linspace(-pre_ms, post_ms, wf_len)

    return waveforms, wf_time_ms, np.array(valid_spikes)


# Extract waveforms
waveforms, wf_time_ms, valid_spike_samples = extract_waveforms(
    hp_signal, spike_samples, fs, pre_ms=0.5, post_ms=2.0
)

print(f"Extracted {waveforms.shape[0]} waveforms")
print(f"Waveform length: {waveforms.shape[1]} samples ({waveforms.shape[1] / fs * 1000:.1f} ms)")

# Plot all waveforms overlaid
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# All waveforms overlaid
axes[0].plot(wf_time_ms, waveforms[:200].T, color="#2c4a8c", alpha=0.08, linewidth=0.5)
axes[0].plot(
    wf_time_ms, np.mean(waveforms, axis=0), color="red", linewidth=2.0, label="Mean waveform"
)
axes[0].axvline(0, color="gray", linewidth=0.7, linestyle="--", label="Trough (t=0)")
axes[0].set_xlabel("Time (ms)")
axes[0].set_ylabel("Voltage (µV)")
axes[0].set_title(f"All Detected Spike Waveforms (n={len(waveforms)}, first 200 shown)")
axes[0].legend(fontsize=9)

# Waveform feature space: trough depth vs. peak amplitude
trough_depths = waveforms.min(axis=1)
peak_heights = waveforms.max(axis=1)

axes[1].scatter(trough_depths, peak_heights, alpha=0.3, s=12, color="#2c4a8c", edgecolors="none")
axes[1].set_xlabel("Trough depth (µV)")
axes[1].set_ylabel("Peak height (µV)")
axes[1].set_title("Waveform Feature Space\n(Hint of two clusters = two neurons)")
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figure_10-6-4_spike_waveforms.png", dpi=150)

# Separate the two clusters roughly by trough depth
cluster_1 = waveforms[trough_depths < np.percentile(trough_depths, 40)]
cluster_2 = waveforms[trough_depths >= np.percentile(trough_depths, 40)]

print("\nWaveform cluster sizes:")
print(f"  Cluster 1 (deep trough, close neuron): {len(cluster_1)}")
print(f"  Cluster 2 (shallow trough, far neuron): {len(cluster_2)}\n")

# -----------------------------
# Inter-Spike Interval Analysis


def analyze_isi(spike_times, title="ISI Distribution"):
    """
    Compute and plot the inter-spike interval distribution.

    Parameters
    ----------
    spike_times : np.ndarray
        Spike times in seconds
    title : str
        Plot title

    Returns
    -------
    dict with keys: isis, mean_rate, cv, refractory_violations
    """
    if len(spike_times) < 2:
        print("Not enough spikes for ISI analysis.")
        return {}

    isis_ms = np.diff(np.sort(spike_times)) * 1000  # convert to ms

    mean_isi_ms = np.mean(isis_ms)
    mean_rate = 1000 / mean_isi_ms  # Hz
    cv = np.std(isis_ms) / mean_isi_ms  # coefficient of variation
    refract_violations = np.sum(isis_ms < 2.0)
    refract_pct = 100 * refract_violations / len(isis_ms)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # ISI histogram
    bins = np.arange(0, 200, 2)
    axes[0].hist(isis_ms, bins=bins, color="#2c4a8c", edgecolor="white", linewidth=0.3)
    axes[0].axvline(
        2.0,
        color="red",
        linewidth=1.2,
        linestyle="--",
        label=f"Refractory (2 ms)\n{refract_violations} violations ({refract_pct:.1f}%)",
    )
    axes[0].set_xlabel("ISI (ms)")
    axes[0].set_ylabel("Count")
    axes[0].set_title(f"{title}\nMean rate: {mean_rate:.1f} Hz | CV: {cv:.2f}")
    axes[0].set_xlim(0, 200)
    axes[0].legend(fontsize=8)

    # Log-scale ISI histogram (reveals the full distribution)
    log_bins = np.logspace(np.log10(1), np.log10(2000), 60)
    axes[1].hist(isis_ms, bins=log_bins, color="#2c4a8c", edgecolor="white", linewidth=0.3)
    axes[1].set_xscale("log")
    axes[1].set_xlabel("ISI (ms) — log scale")
    axes[1].set_ylabel("Count")
    axes[1].set_title("ISI Distribution (Log Scale)")
    axes[1].axvline(2.0, color="red", linewidth=1.0, linestyle="--")

    plt.tight_layout()
    plt.savefig("figure_10-6-5_isi_distribution.png", dpi=150)

    print(f"\n{title}:")
    print(f"  Total spikes:          {len(spike_times)}")
    print(f"  Mean ISI:              {mean_isi_ms:.2f} ms")
    print(f"  Mean firing rate:      {mean_rate:.2f} Hz")
    print(f"  ISI CV:                {cv:.3f}  (1.0 = Poisson, <1 = regular, >1 = bursty)")
    print(f"  Refractory violations: {refract_violations} ({refract_pct:.1f}%)")

    return {
        "isis": isis_ms,
        "mean_rate": mean_rate,
        "cv": cv,
        "refractory_violations": refract_violations,
    }


# Analyze ISI for all detected spikes
isi_results = analyze_isi(spike_times_detected, "All Detected Spikes (both neurons mixed)")
print("Analyze ISI completed...\n")

# -----------------------------------
# Building a Simple Spike Raster Plot

# Simulate 20 trials: neuron fires more during a stimulus (0.5–1.5 s)
np.random.seed(99)
n_trials = 20
trial_duration = 3  # seconds per trial
stimulus_on = 0.5  # s
stimulus_off = 1.5  # s

all_trial_spikes = []
for trial in range(n_trials):
    # Baseline firing: 5 Hz; stimulus-evoked: 25 Hz
    baseline_times = simulate_neuron_spikes(5, trial_duration, fs=1000, seed=trial * 3)
    stim_times = simulate_neuron_spikes(25, trial_duration, fs=1000, seed=trial * 3 + 1)

    # Keep baseline spikes outside stimulus window, stim spikes inside
    baseline_valid = baseline_times[
        (baseline_times < stimulus_on) | (baseline_times > stimulus_off)
    ]
    stim_valid = stim_times[(stim_times >= stimulus_on) & (stim_times <= stimulus_off)]

    trial_spikes = np.sort(np.concatenate([baseline_valid, stim_valid]))
    all_trial_spikes.append(trial_spikes)

# Plot raster + PSTH (peri-stimulus time histogram)
fig, axes = plt.subplots(
    2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1.5]}
)

# Raster
for trial_idx, spikes in enumerate(all_trial_spikes):
    axes[0].scatter(
        spikes,
        np.full_like(spikes, trial_idx + 1),
        marker="|",
        s=50,
        color="#2c4a8c",
        linewidth=0.8,
    )

axes[0].axvspan(stimulus_on, stimulus_off, alpha=0.1, color="orange", label="Stimulus")
axes[0].set_ylabel("Trial")
axes[0].set_title("Spike Raster Plot — Stimulus-Evoked Firing")
axes[0].set_ylim(0.5, n_trials + 0.5)
axes[0].legend(fontsize=9)

# PSTH (peri-stimulus time histogram)
all_spikes_flat = np.concatenate(all_trial_spikes)
bins = np.arange(0, trial_duration + 0.05, 0.05)  # 50 ms bins
counts, bin_edges = np.histogram(all_spikes_flat, bins=bins)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
firing_rate_hz = counts / (n_trials * 0.05)  # spikes per trial per bin_width

axes[1].bar(bin_centers, firing_rate_hz, width=0.045, color="#2c4a8c", edgecolor="none", alpha=0.8)
axes[1].axvspan(stimulus_on, stimulus_off, alpha=0.1, color="orange")
axes[1].set_ylabel("Firing rate (Hz)")
axes[1].set_xlabel("Time (s)")
axes[1].set_title("PSTH (Peri-Stimulus Time Histogram, 50 ms bins)")

plt.tight_layout()
plt.savefig("figure_10-6-6_raster_psth.png", dpi=150)

# Quantify the stimulus response
baseline_rate = np.mean(firing_rate_hz[bin_centers < stimulus_on])
stim_rate = np.mean(firing_rate_hz[(bin_centers >= stimulus_on) & (bin_centers <= stimulus_off)])
print(f"Baseline firing rate: {baseline_rate:.1f} Hz")
print(f"Stimulus-evoked rate: {stim_rate:.1f} Hz")
print(f"Modulation index: {(stim_rate - baseline_rate) / (stim_rate + baseline_rate):.3f}\n")
