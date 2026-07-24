"""
Lecture 10.5: LFP (Local Field Potential) Oscillations and
Frequency Bands (Delta, Theta, Alpha, Beta, Gamma)
"""

from typing import cast

# import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sp_signal
from scipy.ndimage import gaussian_filter1d
from scipy.signal import butter, hilbert, sosfiltfilt

# Canonical frequency bands with neuroscience context
frequency_bands = {
    "Delta": {
        "range": (0.5, 4),
        "color": "#4a90d9",
        "description": "Slow-wave sleep, thalamocortical",
    },
    "Theta": {
        "range": (4, 8),
        "color": "#5cb85c",
        "description": "Hippocampal navigation, REM sleep, memory",
    },
    "Alpha": {
        "range": (8, 13),
        "color": "#f0ad4e",
        "description": "Relaxed wakefulness, visual cortex idling",
    },
    "Beta": {
        "range": (13, 30),
        "color": "#d9534f",
        "description": "Motor planning, active cognition",
    },
    "Low Gamma": {
        "range": (30, 70),
        "color": "#9b59b6",
        "description": "Local computation, attention, binding",
    },
    "High Gamma": {
        "range": (70, 150),
        "color": "#6c3483",
        "description": "Spiking correlate, cortical arousal",
    },
}

print(f"{'Band':<12} {'Range':<12} {'Key associations'}")
print("-" * 65)
for band, info in frequency_bands.items():
    lo, hi = info["range"]
    print(f"{band:<12} {f'{lo}–{hi} Hz':<12} {info['description']}")

# Visual frequency band map
fig, ax = plt.subplots(figsize=(12, 2.5))
ax.set_xlim(0, 150)
ax.set_ylim(0, 1)
ax.set_xlabel("Frequency (Hz)", fontsize=12)
ax.set_title("Neural Frequency Band Map", fontsize=13)
ax.set_yticks([])

for band, info in frequency_bands.items():
    (lo, hi) = cast(tuple[float, float], info["range"])
    ax.axvspan(lo, hi, alpha=0.6, color=info["color"])
    mid = (lo + hi) / 2
    ax.text(mid, 0.55, band, ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    ax.text(mid, 0.2, f"{lo}–{hi} Hz", ha="center", va="center", fontsize=7, color="white")

ax.set_xticks([0.5, 4, 8, 13, 30, 70, 150])
plt.tight_layout()
plt.savefig("figure_10-5-1_frequency_band_map.png", dpi=150)
print("Frequency Band Map example completed...\n")

# ------------------------------------------
# Delta (0.5–4 Hz): The Rhythm of Deep Sleep

# Simulate a cortical delta oscillation with UP/DOWN state transitions
np.random.seed(10)
fs = 1000
duration = 8
t = np.arange(0, duration, 1 / fs)

# Delta: sharp transitions characteristic of UP/DOWN states
# Model as a distorted sine with asymmetric rise/fall
delta_freq = 1.5  # Hz
delta_phase = 2 * np.pi * delta_freq * t
delta_wave = np.sin(delta_phase) + 0.4 * np.sin(2 * delta_phase + 0.3)
delta_wave = 80 * delta_wave / np.max(np.abs(delta_wave))  # scale to ~80 µV

# Add realistic noise
noise = 8 * np.random.randn(len(t))
delta_signal = delta_wave + noise

# Compute power spectrum
freqs_w, psd_w = sp_signal.welch(delta_signal, fs=fs, nperseg=2048, noverlap=1536)

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

axes[0].plot(t[:4000], delta_signal[:4000], color="#4a90d9", linewidth=0.8)
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Voltage (µV)")
axes[0].set_title("Simulated Cortical Delta (slow-wave sleep)")
axes[0].axhline(0, color="gray", linewidth=0.5, linestyle="--")

axes[1].semilogy(freqs_w[:50], psd_w[:50], color="#4a90d9", linewidth=1.5)
axes[1].axvspan(0.5, 4, alpha=0.15, color="#4a90d9", label="Delta band")
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("PSD (µV²/Hz)")
axes[1].set_title("Power Spectrum — Delta Peak at 1.5 Hz")
axes[1].legend()

plt.tight_layout()
plt.savefig("figure_10-5-2_delta_oscillation.png", dpi=150)

# Quantify delta power
delta_mask = (freqs_w >= 0.5) & (freqs_w <= 4)
delta_power = np.trapezoid(psd_w[delta_mask], freqs_w[delta_mask])
total_power = np.trapezoid(
    psd_w[(freqs_w >= 0.5) & (freqs_w <= 100)], freqs_w[(freqs_w >= 0.5) & (freqs_w <= 100)]
)
print(f"Delta power: {delta_power:.2f} µV²")
print(f"Delta as % of total (0.5–100 Hz): {100 * delta_power / total_power:.1f}%")
print("Delta Band example completed...\n")

# --------------------------------------
# Theta (4–8 Hz): The Hippocampal Rhythm

# Simulate hippocampal theta during a navigation epoch
np.random.seed(20)
fs = 1000
duration = 10
t = np.arange(0, duration, 1 / fs)

# Theta appears during movement epochs (seconds 1–4 and 6–9)
theta_envelope = np.zeros_like(t)
theta_envelope[(t >= 1) & (t < 4)] = 1.0
theta_envelope[(t >= 6) & (t < 9)] = 1.0

# Smooth the envelope to avoid abrupt onset/offset
theta_envelope_smooth = gaussian_filter1d(theta_envelope, sigma=50)

theta_freq = 8  # Hz
theta_signal = theta_envelope_smooth * 40 * np.sin(2 * np.pi * theta_freq * t)

# Add delta background and noise
delta_bg = 15 * np.sin(2 * np.pi * 1.5 * t)
noise = 5 * np.random.randn(len(t))
hpc_lfp = theta_signal + delta_bg + noise

# Spectrogram to visualize the navigation-locked theta
freqs_s, times_s, Sxx = sp_signal.spectrogram(
    hpc_lfp, fs=fs, window="hann", nperseg=256, noverlap=224, scaling="density"
)

fig, axes = plt.subplots(2, 1, figsize=(12, 7), gridspec_kw={"height_ratios": [1, 2]})

axes[0].plot(t, hpc_lfp, color="#5cb85c", linewidth=0.7)
axes[0].set_ylabel("Voltage (µV)")
axes[0].set_title("Simulated Hippocampal LFP — Theta During Navigation Epochs")
axes[0].axvspan(1, 4, alpha=0.1, color="#5cb85c", label="Movement")
axes[0].axvspan(6, 9, alpha=0.1, color="#5cb85c")
axes[0].legend()
axes[0].set_xlim(0, duration)

im = axes[1].pcolormesh(
    times_s, freqs_s, 10 * np.log10(Sxx + 1e-12), shading="gouraud", cmap="inferno"
)
axes[1].set_ylim(0, 30)
axes[1].set_ylabel("Frequency (Hz)")
axes[1].set_xlabel("Time (s)")
axes[1].set_title("Spectrogram — Theta Power Locked to Movement")
axes[1].axhline(8, color="lime", linewidth=0.8, alpha=0.6, linestyle="--", label="8 Hz theta")
axes[1].legend(fontsize=9)
plt.colorbar(im, ax=axes[1], label="dB")

plt.tight_layout()
plt.savefig("figure_10-5-3_theta_navigation.png", dpi=150)
print("Theta Band example completed...\n")

# ----------------------------------
# Alpha (8–13 Hz): The Idling Rhythm

# Simulate alpha lateralization during a visual attention task
np.random.seed(30)
fs = 1000
duration = 12
t = np.arange(0, duration, 1 / fs)

# Eyes-closed baseline: strong bilateral alpha (0–3 s)
# Attend LEFT (3–7 s): alpha suppressed in right hemisphere (contralateral)
# Attend RIGHT (7–11 s): alpha suppressed in left hemisphere (contralateral)


def make_alpha_lfp(alpha_amplitudes, t, fs):
    """Build an LFP with time-varying alpha amplitude."""
    signal = np.zeros_like(t)
    alpha_env = np.zeros_like(t)
    for start, end, amp in alpha_amplitudes:
        mask = (t >= start) & (t < end)
        alpha_env[mask] = amp
    alpha_env = gaussian_filter1d(alpha_env, sigma=80)
    signal = alpha_env * np.sin(2 * np.pi * 10 * t)
    signal += 3 * np.random.randn(len(t))
    return signal


# Right hemisphere LFP (contralateral to LEFT hemifield)
right_lfp = make_alpha_lfp(
    [(0, 3, 30), (3, 7, 5), (7, 11, 30)], t, fs  # suppressed when attending left
)

# Left hemisphere LFP (contralateral to RIGHT hemifield)
left_lfp = make_alpha_lfp(
    [(0, 3, 30), (3, 7, 30), (7, 11, 5)], t, fs  # suppressed when attending right
)

# Compute spectrograms for both hemispheres
f_r, t_r, Sxx_r = sp_signal.spectrogram(right_lfp, fs=fs, nperseg=256, noverlap=224)
f_l, t_l, Sxx_l = sp_signal.spectrogram(left_lfp, fs=fs, nperseg=256, noverlap=224)

fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
fig.suptitle("Alpha Lateralization in Visual Attention Task", fontsize=12)

for ax, (f, t_s, Sxx, title) in zip(
    axes,
    [
        (f_r, t_r, Sxx_r, "Right Hemisphere — Alpha suppressed when attending LEFT"),
        (f_l, t_l, Sxx_l, "Left Hemisphere — Alpha suppressed when attending RIGHT"),
    ],
):
    im = ax.pcolormesh(
        t_s, f, 10 * np.log10(Sxx + 1e-12), shading="gouraud", cmap="inferno", vmin=-5, vmax=30
    )
    ax.set_ylim(0, 25)
    ax.axvline(3, color="white", linewidth=1.0, linestyle="--", alpha=0.7)
    ax.axvline(7, color="white", linewidth=1.0, linestyle="--", alpha=0.7)
    ax.axvline(11, color="white", linewidth=1.0, linestyle="--", alpha=0.7)
    ax.axhline(10, color="lime", linewidth=0.7, alpha=0.5, linestyle=":")
    ax.set_ylabel("Freq (Hz)")
    ax.set_title(title)
    plt.colorbar(im, ax=ax, label="dB")

axes[-1].set_xlabel("Time (s)")
for ax in axes:
    for x, lbl in [(1.5, "Eyes\nclosed"), (5, "Attend\nLEFT"), (9, "Attend\nRIGHT")]:
        ax.text(x, 22, lbl, ha="center", fontsize=8, color="white")

plt.tight_layout()
plt.savefig("figure_10-5-4_alpha_lateralization.png", dpi=150)
print("Alpha Band example completed...\n")

# ---------------------------------------------
# Beta (13–30 Hz): The Motor and Cognitive Band

# Simulate motor cortex beta ERD/PMBR around a voluntary movement
np.random.seed(40)
fs = 1000
duration = 8
t = np.arange(0, duration, 1 / fs)

# Movement occurs at t=4 s, duration ~0.5 s
# ERD starts ~1 s before movement, PMBR peaks ~1.5 s after
beta_envelope = np.ones_like(t) * 25  # baseline beta amplitude (µV)

# Pre-movement suppression (ERD): ramps down from t=3 to t=4
erd_mask = (t >= 3) & (t < 4.5)
beta_envelope[erd_mask] = 25 * (1 - 0.85 * np.sin(np.pi * (t[erd_mask] - 3) / 1.5))

# Movement period: beta nearly absent
move_mask = (t >= 4.5) & (t < 5)
beta_envelope[move_mask] = 3

# PMBR: rebounds above baseline
pmbr_mask = (t >= 5) & (t < 7)
pmbr_t = t[pmbr_mask] - 5
beta_envelope[pmbr_mask] = 25 + 15 * np.exp(-((pmbr_t - 0.8) ** 2) / (2 * 0.3**2))

beta_envelope = gaussian_filter1d(beta_envelope, sigma=30)
motor_lfp = beta_envelope * np.sin(2 * np.pi * 20 * t)
motor_lfp += 4 * np.random.randn(len(t))


# Time-resolved beta power via Hilbert amplitude envelope
def bandpass_envelope(signal, lo, hi, fs):
    """Extract the instantaneous amplitude envelope of a frequency band."""
    sos = butter(4, [lo / (fs / 2), hi / (fs / 2)], btype="bandpass", output="sos")
    filtered = sosfiltfilt(sos, signal)
    analytic = hilbert(filtered)
    envelope = np.abs(analytic)
    return filtered, envelope


beta_filtered, beta_env = bandpass_envelope(motor_lfp, 13, 30, fs)

fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

axes[0].plot(t, motor_lfp, color="#d9534f", linewidth=0.7)
axes[0].axvline(4, color="black", linewidth=1.2, linestyle="--", label="Movement onset")
axes[0].set_ylabel("Voltage (µV)")
axes[0].set_title("Simulated Motor Cortex LFP")
axes[0].legend()

axes[1].plot(t, beta_filtered, color="#d9534f", linewidth=0.6, alpha=0.7)
axes[1].plot(t, beta_env, color="#8b0000", linewidth=1.5, label="Beta envelope")
axes[1].axvline(4, color="black", linewidth=1.0, linestyle="--")
axes[1].set_ylabel("Beta (µV)")
axes[1].set_title("Beta Band (13–30 Hz) with Hilbert Envelope")
axes[1].legend()

axes[2].plot(t, beta_env**2, color="#8b0000", linewidth=1.2)
axes[2].axhline(
    np.mean(beta_env[:2000] ** 2),
    color="gray",
    linewidth=0.8,
    linestyle="--",
    label="Baseline power",
)
axes[2].axvline(4, color="black", linewidth=1.0, linestyle="--", label="Movement")
axes[2].fill_between(t, beta_env**2, alpha=0.3, color="#d9534f")
axes[2].set_ylabel("Beta power (µV²)")
axes[2].set_xlabel("Time (s)")
axes[2].set_title("Beta Power: ERD Before Movement, PMBR After")
axes[2].legend()

for ax in axes:
    ax.axvspan(3, 4, alpha=0.08, color="blue", label="ERD window")
    ax.axvspan(5, 7, alpha=0.08, color="orange", label="PMBR window")

plt.tight_layout()
plt.savefig("figure_10-5-5_beta_erd_pmbr.png", dpi=150)
print("Beta Band example completed...\n")

# -------------------------------------------
# Gamma (30–80 Hz) and High Gamma (70–150 Hz)

# Quantify gamma power changes in response to a simulated visual stimulus
np.random.seed(50)
fs = 1000
duration = 6
t = np.arange(0, duration, 1 / fs)

# Baseline: low gamma, high alpha
baseline_alpha = 20 * np.sin(2 * np.pi * 10 * t)
baseline_gamma = 2 * np.sin(2 * np.pi * 50 * t)

# Stimulus at t=2 s: gamma increases, alpha desynchronizes
stim_onset = 2.0
stim_duration = 1.5

stim_gamma_env = np.zeros_like(t)
stim_mask = (t >= stim_onset) & (t < stim_onset + stim_duration)
stim_gamma_env[stim_mask] = 12  # 6x increase in gamma amplitude
stim_gamma_env = gaussian_filter1d(stim_gamma_env, sigma=20)

alpha_suppression = np.ones_like(t)
alpha_suppression[stim_mask] = 0.2
alpha_suppression = gaussian_filter1d(alpha_suppression, sigma=25)

visual_lfp = (
    alpha_suppression * baseline_alpha
    + baseline_gamma
    + stim_gamma_env * np.sin(2 * np.pi * 50 * t)
    + 3 * np.random.randn(len(t))
)

# Extract band envelopes
_, alpha_env_v = bandpass_envelope(visual_lfp, 8, 13, fs)
_, gamma_env_v = bandpass_envelope(visual_lfp, 30, 70, fs)

# Normalize to pre-stimulus baseline
baseline_idx = t < stim_onset
alpha_norm = alpha_env_v**2 / np.mean(alpha_env_v[baseline_idx] ** 2)
gamma_norm = gamma_env_v**2 / np.mean(gamma_env_v[baseline_idx] ** 2)

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

axes[0].plot(t, alpha_norm, color="#f0ad4e", linewidth=1.3, label="Alpha power (normalized)")
axes[0].plot(t, gamma_norm, color="#9b59b6", linewidth=1.3, label="Gamma power (normalized)")
axes[0].axvline(stim_onset, color="red", linewidth=1.2, linestyle="--", label="Stimulus onset")
axes[0].axvline(
    stim_onset + stim_duration, color="red", linewidth=0.8, linestyle=":", label="Stimulus offset"
)
axes[0].axhline(1.0, color="gray", linewidth=0.7, linestyle=":")
axes[0].set_ylabel("Normalized power")
axes[0].set_title("Visual Cortex: Alpha Desynchronization & Gamma Synchronization")
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.2)

f_v, t_v, Sxx_v = sp_signal.spectrogram(visual_lfp, fs=fs, nperseg=128, noverlap=112)
im = axes[1].pcolormesh(t_v, f_v, 10 * np.log10(Sxx_v + 1e-12), shading="gouraud", cmap="inferno")
axes[1].set_ylim(0, 80)
axes[1].axvline(stim_onset, color="white", linewidth=1.0, linestyle="--")
axes[1].set_ylabel("Freq (Hz)")
axes[1].set_xlabel("Time (s)")
axes[1].set_title("Spectrogram: Alpha Suppression and Gamma Enhancement Post-Stimulus")
plt.colorbar(im, ax=axes[1], label="dB")

plt.tight_layout()
plt.savefig("figure_10-5-6_gamma_visual_stimulus.png", dpi=150)

print("Band power changes triggered by visual stimulus:")
stim_t = (t >= stim_onset) & (t < stim_onset + stim_duration)
print(f"  Alpha suppression: {np.mean(alpha_norm[stim_t]):.2f}x baseline")
print(f"  Gamma enhancement: {np.mean(gamma_norm[stim_t]):.2f}x baseline")
print("Gamma Bands example completed...\n")

# ------------------------------
# A Unified Band Power Dashboard


def lfp_band_dashboard(signal, fs, title="LFP Band Power Dashboard"):
    """
    Compute and visualize all canonical frequency band powers for an LFP recording.

    Parameters
    ----------
    signal : np.ndarray
        1D LFP voltage array
    fs : float
        Sampling rate in Hz
    title : str
        Plot title

    Returns
    -------
    dict
        Band name → (power_µV2, fraction_of_total, envelope_array)
    """
    t_sig = np.arange(len(signal)) / fs

    bands = {
        "Delta": (0.5, 4, "#4a90d9"),
        "Theta": (4, 8, "#5cb85c"),
        "Alpha": (8, 13, "#f0ad4e"),
        "Beta": (13, 30, "#d9534f"),
        "Low Gamma": (30, 70, "#9b59b6"),
        "High Gamma": (70, 150, "#6c3483"),
    }

    # Compute Welch PSD once
    freqs_w, psd = sp_signal.welch(signal, fs=fs, nperseg=min(2048, len(signal) // 2))
    total_power = np.trapezoid(
        psd[(freqs_w >= 0.5) & (freqs_w <= 150)], freqs_w[(freqs_w >= 0.5) & (freqs_w <= 150)]
    )

    results = {}
    envelopes = {}

    for band_name, (lo, hi, color) in bands.items():
        mask = (freqs_w >= lo) & (freqs_w <= hi)
        bp = np.trapezoid(psd[mask], freqs_w[mask])
        _, env = bandpass_envelope(signal, lo, min(hi, fs / 2 - 1), fs)
        results[band_name] = (bp, bp / total_power, color)
        envelopes[band_name] = env

    # Plot
    fig, axes = plt.subplots(3, 1, figsize=(13, 10))
    fig.suptitle(title, fontsize=13)

    # Panel 1: raw signal
    axes[0].plot(t_sig, signal, color="#333333", linewidth=0.6)
    axes[0].set_ylabel("Voltage (µV)")
    axes[0].set_title("Raw LFP")
    axes[0].set_xlim(t_sig[0], t_sig[-1])

    # Panel 2: band envelopes over time
    for band_name, (_, _, color) in bands.items():
        axes[1].plot(
            t_sig, envelopes[band_name], color=color, linewidth=0.9, alpha=0.85, label=band_name
        )
    axes[1].set_ylabel("Amplitude (µV)")
    axes[1].set_title("Band Amplitude Envelopes Over Time")
    axes[1].legend(fontsize=8, loc="upper right", ncol=2)
    axes[1].set_xlim(t_sig[0], t_sig[-1])

    # Panel 3: bar chart of relative band powers
    names = list(results.keys())
    _ = [results[n][0] for n in names]
    fracs = [results[n][1] * 100 for n in names]
    colors = [results[n][2] for n in names]

    bars = axes[2].bar(names, fracs, color=colors, edgecolor="white", linewidth=1.0)
    axes[2].set_ylabel("% of Total Power (0.5–150 Hz)")
    axes[2].set_title("Relative Band Power Distribution")
    for bar, pct in zip(bars, fracs):
        axes[2].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{pct:.1f}%",
            ha="center",
            fontsize=9,
        )
    axes[2].set_ylim(0, max(fracs) * 1.2)

    plt.tight_layout()
    plt.savefig("figure_10-5-7_lfp_band_dashboard.png", dpi=150)

    print(f"\n{title}")
    print(f"{'Band':<14} {'Power (µV²)':<15} {'% of Total'}")
    print("-" * 40)
    for name in names:
        bp, frac, _ = results[name]
        print(f"{name:<14} {bp:<15.4f} {frac * 100:.1f}%")

    return results


# Apply to our dynamic LFP from Lecture 10.4
try:
    lfp_dynamic = np.load("week10_simulated_lfp_dynamic.npy")
    fs_d = 1000
    band_results = lfp_band_dashboard(lfp_dynamic, fs_d, "Dynamic LFP — Full Band Power Dashboard")
except FileNotFoundError:
    # Fall back to the static LFP
    lfp_static = np.load("week10_simulated_lfp.npy") if True else None
    band_results = lfp_band_dashboard(lfp_static, 1000, "Simulated LFP — Full Band Power Dashboard")
print()
