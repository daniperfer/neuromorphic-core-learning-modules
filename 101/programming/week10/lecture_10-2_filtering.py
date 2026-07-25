"""
Lecture 10.2: Filtering Neural Signals (Low-Pass, High-Pass, Band-Pass)
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import rfft, rfftfreq
from scipy import signal as sp_signal

# Load the simulated LFP from Lecture 10.1
# If you don't have the file, regenerate it:
filename_signal = "week10_simulated_lfp.npy"
filename_time = "week10_time_axis.npy"
try:
    lfp = np.load(f"{filename_signal}")
    t = np.load(f"{filename_time}")
    fs = 1000  # Hz
    print(f"Loaded LFP: {len(lfp)} samples, {len(lfp) / fs:.1f} s at {fs} Hz")
except FileNotFoundError:
    # Regenerate the signal from Lecture 10.1
    np.random.seed(42)
    fs = 1000
    duration = 5
    t = np.arange(0, duration, 1 / fs)
    delta = 3.0 * np.sin(2 * np.pi * 2 * t)
    theta = 2.0 * np.sin(2 * np.pi * 8 * t)
    alpha = 1.5 * np.sin(2 * np.pi * 12 * t)
    beta = 0.8 * np.sin(2 * np.pi * 25 * t)
    gamma = 0.4 * np.sin(2 * np.pi * 60 * t)
    freqs = np.fft.rfftfreq(len(t), d=1 / fs)
    freqs[0] = 1
    noise_spectrum = np.random.randn(len(freqs)) + 1j * np.random.randn(len(freqs))
    noise_spectrum /= np.sqrt(freqs)
    pink_noise = np.fft.irfft(noise_spectrum, n=len(t))
    pink_noise = 1.0 * (pink_noise / np.std(pink_noise))
    lfp = delta + theta + alpha + beta + gamma + pink_noise
    print(f"Regenerated LFP: {len(lfp)} samples")
print()

# -------------------------------------
# Butterworth Filters with scipy.signal


def butter_filter(data, cutoff, fs, filter_type, order=4):
    """
    Apply a Butterworth filter to neural data.

    Parameters
    ----------
    data : np.ndarray
        1D array of voltage samples
    cutoff : float or list of two floats
        Cutoff frequency in Hz. For 'bandpass' and 'bandstop',
        provide [low_cutoff, high_cutoff].
    fs : float
        Sampling rate in Hz
    filter_type : str
        One of: 'low', 'high', 'bandpass', 'bandstop'
    order : int
        Filter order — higher = steeper rolloff, more phase distortion

    Returns
    -------
    np.ndarray
        Filtered signal, same shape as input
    """
    nyquist = fs / 2

    if filter_type in ("bandpass", "bandstop"):
        normalized_cutoff = [c / nyquist for c in cutoff]
    else:
        normalized_cutoff = cutoff / nyquist

    # Design filter as second-order sections (sos) — numerically stable
    sos = sp_signal.butter(order, normalized_cutoff, btype=filter_type, output="sos")

    # filtfilt applies the filter forwards then backwards — zero phase distortion
    filtered = sp_signal.sosfiltfilt(sos, data)

    return filtered


# -------------------------------
# Applying the Three Filter Types

# --- Low-pass filter: keep everything below 30 Hz ---
lfp_lowpass = butter_filter(lfp, cutoff=30, fs=fs, filter_type="low")

# --- High-pass filter: keep everything above 15 Hz ---
lfp_highpass = butter_filter(lfp, cutoff=15, fs=fs, filter_type="high")

# --- Band-pass filter: keep the theta band (6–10 Hz) ---
lfp_theta = butter_filter(lfp, cutoff=[6, 10], fs=fs, filter_type="bandpass")

# --- Band-pass filter: keep the gamma band (30–80 Hz) ---
lfp_gamma = butter_filter(lfp, cutoff=[30, 80], fs=fs, filter_type="bandpass")

# Visualize all four
fig, axes = plt.subplots(5, 1, figsize=(12, 12), sharex=True)
plot_window = t < 2  # show first 2 seconds

axes[0].plot(t[plot_window], lfp[plot_window], color="#333333", linewidth=0.8)
axes[0].set_title("Raw LFP (all frequencies)")
axes[0].set_ylabel("µV")

axes[1].plot(t[plot_window], lfp_lowpass[plot_window], color="#2c4a8c", linewidth=1.0)
axes[1].set_title("Low-pass filtered (< 30 Hz) — slow oscillations only")
axes[1].set_ylabel("µV")

axes[2].plot(t[plot_window], lfp_highpass[plot_window], color="#8c2c2c", linewidth=0.8)
axes[2].set_title("High-pass filtered (> 15 Hz) — fast components only")
axes[2].set_ylabel("µV")

axes[3].plot(t[plot_window], lfp_theta[plot_window], color="#2c8c4a", linewidth=1.0)
axes[3].set_title("Band-pass filtered: Theta (6-10 Hz)")
axes[3].set_ylabel("µV")

axes[4].plot(t[plot_window], lfp_gamma[plot_window], color="#8c6a2c", linewidth=0.8)
axes[4].set_title("Band-pass filtered: Gamma (30-80 Hz)")
axes[4].set_ylabel("µV")
axes[4].set_xlabel("Time (s)")

plt.tight_layout()
plt.savefig("figure_10-2-1_filtered_lfp_comparison.png", dpi=150)
print("Filtering example completed...\n")

# --------------------------
# Understanding Filter Order

# Comparing filter orders — how sharp is the transition?
fig, ax = plt.subplots(figsize=(10, 5))

orders = [2, 4, 6, 8]
colors = ["#add8e6", "#4682b4", "#00008b", "#000033"]
cutoff_hz = 30  # Hz
nyquist = fs / 2

freqs_plot = np.linspace(0, 200, 1000)

for order, color in zip(orders, colors):
    sos = sp_signal.butter(order, cutoff_hz / nyquist, btype="low", output="sos")
    w, h = sp_signal.sosfreqz(sos, worN=1000, fs=fs)
    ax.plot(w, 20 * np.log10(np.abs(h) + 1e-10), color=color, linewidth=1.8, label=f"Order {order}")

ax.axvline(cutoff_hz, color="red", linestyle="--", alpha=0.7, label=f"Cutoff ({cutoff_hz} Hz)")
ax.axhline(-3, color="gray", linestyle=":", alpha=0.7, label="-3 dB point")
ax.set_xlim(0, 200)
ax.set_ylim(-80, 5)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("Low-pass Butterworth Filter: Effect of Filter Order")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("figure_10-2-2_filter_order_comparison.png", dpi=150)
print("Filter order example completed...\n")

# ------------------------------------------
# Notch Filtering: Removing Power Line Noise


def notch_filter(data, notch_freq, fs, quality_factor=30):
    """
    Remove a narrow frequency band (e.g., 60 Hz power line noise).

    Parameters
    ----------
    data : np.ndarray
        Input signal
    notch_freq : float
        Frequency to remove, in Hz
    fs : float
        Sampling rate in Hz
    quality_factor : float
        Higher Q = narrower notch. Q=30 is a good default.
    """
    b, a = sp_signal.iirnotch(notch_freq, quality_factor, fs)
    return sp_signal.filtfilt(b, a, data)


# Add artificial 60 Hz noise to simulate power line contamination
noise_60hz = 2.0 * np.sin(2 * np.pi * 60 * t)
lfp_contaminated = lfp + noise_60hz

# Apply notch filter
lfp_notched = notch_filter(lfp_contaminated, notch_freq=60, fs=fs)

# Compare power at 60 Hz before and after
freqs_fft = rfftfreq(len(t), d=1 / fs)
power_before = np.abs(rfft(lfp_contaminated)) ** 2
power_after = np.abs(rfft(lfp_notched)) ** 2

# Find the 60 Hz bin
idx_60 = np.argmin(np.abs(freqs_fft - 60))
print(f"Power at 60 Hz BEFORE notch: {power_before[idx_60]:.1f}")
print(f"Power at 60 Hz AFTER notch:  {power_after[idx_60]:.1f}")
print(f"Reduction factor: {power_before[idx_60] / power_after[idx_60]:.0f}x")

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
mask = t < 0.5
axes[0].plot(t[mask], lfp_contaminated[mask], color="#8c2c2c", linewidth=0.8)
axes[0].set_title("LFP with 60 Hz Power Line Contamination")
axes[0].set_ylabel("µV")

axes[1].plot(t[mask], lfp_notched[mask], color="#2c4a8c", linewidth=0.8)
axes[1].set_title("After 60 Hz Notch Filter")
axes[1].set_ylabel("µV")
axes[1].set_xlabel("Time (s)")
plt.tight_layout()
plt.savefig("figure_10-2-3_notch_filter_demo.png", dpi=150)
print("Notch filtering example completed...\n")

# -----------------------------------------------
# A Complete Neural Signal Preprocessing Pipeline


def preprocess_neural_recording(raw_signal, fs):
    """
    Standard preprocessing pipeline for broadband neural recordings.

    Extracts two signals from a single raw recording:
    1. LFP: band-pass 1-300 Hz, down-sampled to 1000 Hz
    2. MUA: high-pass > 300 Hz (for spike detection in later steps)

    Parameters
    ----------
    raw_signal : np.ndarray
        Raw voltage trace sampled at fs Hz
    fs : float
        Sampling rate of the raw signal (typically 30000 Hz)

    Returns
    -------
    dict with keys 'lfp', 'mua', 'fs_lfp', 'fs_mua'
    """
    print(f"Input: {len(raw_signal)} samples at {fs} Hz")

    # Step 1: Remove DC offset (very slow drift, < 0.5 Hz)
    signal_dc_removed = butter_filter(raw_signal, cutoff=0.5, fs=fs, filter_type="high")
    print("Step 1: DC removal (high-pass 0.5 Hz) — done")

    # Step 2: Notch filter for power line noise
    signal_clean = notch_filter(signal_dc_removed, notch_freq=60, fs=fs)
    print("Step 2: 60 Hz notch filter — done")

    # Step 3: Extract LFP (1–300 Hz, then downsample)
    lfp_signal = butter_filter(signal_clean, cutoff=[1, 300], fs=fs, filter_type="bandpass")
    # Downsample to 1000 Hz (every 30th sample if fs=30000)
    downsample_factor = int(fs / 1000)
    lfp_downsampled = lfp_signal[::downsample_factor]
    fs_lfp = fs / downsample_factor
    print(f"Step 3: LFP extraction (1–300 Hz, downsampled to {fs_lfp:.0f} Hz) — done")

    # Step 4: Extract MUA (high-pass > 300 Hz for spike detection)
    mua_signal = butter_filter(signal_clean, cutoff=300, fs=fs, filter_type="high")
    print(f"Step 4: MUA extraction (high-pass 300 Hz, kept at {fs} Hz) — done")

    return {"lfp": lfp_downsampled, "mua": mua_signal, "fs_lfp": fs_lfp, "fs_mua": fs}


# Demonstrate with our simulated signal (pretending it was sampled at 30000 Hz)
# For illustration we'll use our 1000 Hz signal and skip the downsampling meaningfully
result = preprocess_neural_recording(lfp, fs=fs)
print(f"\nOutput LFP samples: {len(result['lfp'])} at {result['fs_lfp']:.0f} Hz")
print(f"Output MUA samples: {len(result['mua'])} at {result['fs_mua']:.0f} Hz")
print()
