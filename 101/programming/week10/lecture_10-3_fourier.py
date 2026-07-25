"""
Lecture 10.3: The Fourier Transform and Power Spectra
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sp_signal
from scipy.stats import linregress

filename_signal = "week10_simulated_lfp.npy"
filename_time = "week10_time_axis.npy"
try:
    lfp = np.load(f"{filename_signal}")
    t = np.load(f"{filename_time}")
    fs = 1000  # Hz
    print(f"Loaded LFP: {len(lfp)} samples, {len(lfp) / fs:.1f} s at {fs} Hz\n")
except FileNotFoundError:
    np.random.seed(42)
    fs = 1000
    duration = 5
    t = np.arange(0, duration, 1 / fs)
    delta = 3.0 * np.sin(2 * np.pi * 2 * t)
    theta = 2.0 * np.sin(2 * np.pi * 8 * t)
    alpha = 1.5 * np.sin(2 * np.pi * 12 * t)
    beta = 0.8 * np.sin(2 * np.pi * 25 * t)
    gamma = 0.4 * np.sin(2 * np.pi * 60 * t)
    freqs_n = np.fft.rfftfreq(len(t), d=1 / fs)
    freqs_n[0] = 1
    ns = np.random.randn(len(freqs_n)) + 1j * np.random.randn(len(freqs_n))
    ns /= np.sqrt(freqs_n)
    pink_noise = np.fft.irfft(ns, n=len(t))
    pink_noise = 1.0 * (pink_noise / np.std(pink_noise))
    lfp = delta + theta + alpha + beta + gamma + pink_noise
    print(f"Regenerated LFP: {len(lfp)} samples\n")
print()

# Compute the FFT
N = len(lfp)  # number of samples
fft_result = np.fft.rfft(lfp)  # complex-valued spectrum
freqs = np.fft.rfftfreq(N, d=1 / fs)  # frequency axis in Hz

# The FFT returns complex numbers: amplitude AND phase
# For the power spectrum, we want amplitude squared
power = np.abs(fft_result) ** 2

# Normalize: divide by N^2 to get power in µV²
# Then multiply by 2 (except DC and Nyquist) to account for one-sided spectrum
power_normalized = (2 * power) / (N**2)
power_normalized[0] /= 2  # DC component — don't double
power_normalized[-1] /= 2  # Nyquist component — don't double

print(f"FFT output length: {len(fft_result)} complex values")
print(f"Frequency resolution: {freqs[1] - freqs[0]:.4f} Hz")
print(f"Frequency range: {freqs[0]:.1f} – {freqs[-1]:.1f} Hz")
print(f"Total power: {np.sum(power_normalized):.4f} µV²")

# Plot the power spectrum
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Linear scale
axes[0].plot(freqs, power_normalized, color="#2c4a8c", linewidth=1.0)
axes[0].set_xlim(0, 100)
axes[0].set_xlabel("Frequency (Hz)")
axes[0].set_ylabel("Power (µV²)")
axes[0].set_title("Power Spectrum — Linear Scale")
for f, label in [(2, "δ"), (8, "θ"), (12, "α"), (25, "β"), (60, "γ")]:
    axes[0].axvline(f, color="red", alpha=0.4, linestyle="--", linewidth=0.8)
    axes[0].text(f + 0.5, axes[0].get_ylim()[1] * 0.9, label, color="red", fontsize=9)

# Log scale — much more informative for neural data
axes[1].semilogy(freqs[1:], power_normalized[1:], color="#2c4a8c", linewidth=1.0)
axes[1].set_xlim(0, 200)
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("Power (µV²) — log scale")
axes[1].set_title("Power Spectrum — Log Scale (standard for neural data)")
for f, label in [(2, "δ"), (8, "θ"), (12, "α"), (25, "β"), (60, "γ")]:
    axes[1].axvline(f, color="red", alpha=0.4, linestyle="--", linewidth=0.8)
    axes[1].text(f + 0.5, axes[1].get_ylim()[1] * 0.5, label, color="red", fontsize=9)

plt.tight_layout()
plt.savefig("figure_10-3-1_power_spectrum_fft.png", dpi=150)
print("FFT example completed...\n")

# ------------------------------------------------
# Frequency Resolution and the Trade-off with Time

# Demonstrating the frequency resolution trade-off
durations = [0.5, 1.0, 2.0, 5.0]
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Frequency Resolution vs. Recording Duration", fontsize=13)

for ax, dur in zip(axes.flat, durations):
    n_samples = int(dur * fs)
    seg = lfp[:n_samples]
    freqs_seg = np.fft.rfftfreq(n_samples, d=1 / fs)
    power_seg = np.abs(np.fft.rfft(seg)) ** 2
    power_seg = (2 * power_seg) / (n_samples**2)

    freq_res = 1.0 / dur

    ax.semilogy(freqs_seg[1:], power_seg[1:], color="#2c4a8c", linewidth=1.0)
    ax.set_xlim(0, 30)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power (µV²)")
    ax.set_title(f"Duration: {dur:.1f} s → Freq resolution: {freq_res:.2f} Hz")
    ax.grid(True, alpha=0.3)
    for f in [2, 8, 12]:
        ax.axvline(f, color="red", alpha=0.3, linewidth=0.7)

plt.tight_layout()
plt.savefig("figure_10-3-2_frequency_resolution_tradeoff.png", dpi=150)
print("Frequency resolution example completed...\n")

# -----------------------------------------------------------
# Welch’s Method: The Standard Power Spectrum for Neural Data

# Welch's method via scipy.signal.welch
freqs_welch, psd_welch = sp_signal.welch(
    lfp,
    fs=fs,
    window="hann",  # Hann window reduces spectral leakage
    nperseg=512,  # window length in samples (0.512 s at 1000 Hz)
    noverlap=256,  # 50% overlap between windows
    scaling="density",  # returns power spectral DENSITY (µV²/Hz)
)

# Compare raw FFT vs Welch
freqs_raw = np.fft.rfftfreq(len(lfp), d=1 / fs)
power_raw = (2 * np.abs(np.fft.rfft(lfp)) ** 2) / (len(lfp) ** 2)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].semilogy(
    freqs_raw[1:200], power_raw[1:200], color="#8c2c2c", linewidth=0.7, alpha=0.8, label="Raw FFT"
)
axes[0].semilogy(freqs_welch[1:], psd_welch[1:], color="#2c4a8c", linewidth=2.0, label="Welch PSD")
axes[0].set_xlim(1, 100)
axes[0].set_xlabel("Frequency (Hz)")
axes[0].set_ylabel("Power Spectral Density (µV²/Hz)")
axes[0].set_title("Raw FFT vs. Welch's Method")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Log-log plot: reveals the 1/f background
axes[1].loglog(freqs_welch[1:], psd_welch[1:], color="#2c4a8c", linewidth=1.5)
axes[1].set_xlabel("Frequency (Hz) — log scale")
axes[1].set_ylabel("PSD (µV²/Hz) — log scale")
axes[1].set_title("Welch PSD — Log-Log Scale (reveals 1/f background)")
axes[1].grid(True, alpha=0.3, which="both")

# Annotate neural frequency bands
band_colors = {
    "δ (1–4)": (1, 4, "#6699cc"),
    "θ (4–8)": (4, 8, "#66bb66"),
    "α (8–13)": (8, 13, "#ddaa44"),
    "β (13–30)": (13, 30, "#dd6644"),
    "γ (30–80)": (30, 80, "#aa44aa"),
}
for label, (lo, hi, color) in band_colors.items():
    axes[1].axvspan(lo, hi, alpha=0.1, color=color, label=label)
axes[1].legend(fontsize=8, loc="lower left")

plt.tight_layout()
plt.savefig("figure_10-3-3_welch_psd.png", dpi=150)

print("Welch PSD parameters:")
print(f"  Window: Hann, {512} samples ({512 / fs * 1000:.0f} ms)")
print("  Overlap: 50%")
print(f"  Frequency resolution: {freqs_welch[1] - freqs_welch[0]:.3f} Hz")
print(f"  Number of frequency bins: {len(freqs_welch)}\n")

# --------------------------------------------
# Band Power: Quantifying Oscillation Strength


def compute_band_power(psd, freqs, band_low, band_high):
    """
    Compute total power within a frequency band using the trapezoidal rule.

    Parameters
    ----------
    psd : np.ndarray
        Power spectral density array (from Welch or similar)
    freqs : np.ndarray
        Frequency axis corresponding to psd
    band_low, band_high : float
        Lower and upper frequency limits of the band in Hz

    Returns
    -------
    float
        Total power in the band (µV²)
    """
    idx = np.logical_and(freqs >= band_low, freqs <= band_high)
    band_power = np.trapezoid(psd[idx], freqs[idx])
    return band_power


# Define standard neural frequency bands
bands = {
    "Delta": (1, 4),
    "Theta": (4, 8),
    "Alpha": (8, 13),
    "Beta": (13, 30),
    "Gamma": (30, 80),
    "Total": (1, 80),
}

print("Band Power Analysis:")
print(f"{'Band':<10} {'Range':<12} {'Power (µV²)':<15} {'% of Total'}")
print("-" * 50)
total_power = compute_band_power(psd_welch, freqs_welch, 1, 80)
for band_name, (lo, hi) in bands.items():
    bp = compute_band_power(psd_welch, freqs_welch, lo, hi)
    pct = (bp / total_power) * 100 if band_name != "Total" else 100.0
    print(f"{band_name:<10} {f'{lo}–{hi} Hz':<12} {bp:<15.4f} {pct:.1f}%")

# Bar chart of relative band powers
band_names = list(bands.keys())[:-1]
band_powers = [compute_band_power(psd_welch, freqs_welch, *bands[b]) for b in band_names]
band_colors_bar = ["#6699cc", "#66bb66", "#ddaa44", "#dd6644", "#aa44aa"]

plt.figure(figsize=(8, 5))
bars = plt.bar(band_names, band_powers, color=band_colors_bar, edgecolor="white", linewidth=1.2)
plt.ylabel("Power (µV²)")
plt.title("Band Power Distribution in Simulated LFP")
plt.tight_layout()
plt.savefig("figure_10-3-4_band_power_bar.png", dpi=150)
print("\nCompute band power example completed...\n")

# -----------------------------------------
# The 1/f Structure of Neural Power Spectra
# Fitting the 1/f background with a linear regression in log-log space

# Use frequencies from 2 Hz to 40 Hz, avoiding oscillation peaks
# In practice you'd exclude known peak frequencies; here we use the full range
log_freqs = np.log10(freqs_welch[2:80])  # 2–80 Hz
log_power = np.log10(psd_welch[2:80])

slope, intercept, r_value, p_value, std_err = linregress(log_freqs, log_power)

print("1/f fit results:")
print(f"  Spectral exponent (slope): {slope:.3f}")
print(f"  R²: {r_value**2:.3f}")
print(f"  p-value: {p_value:.2e}")
print()
print(f"Interpretation: Power scales as f^{slope:.2f}")
print("(Healthy cortical LFP typically shows slopes between -1 and -3)")

# Plot log-log PSD with fit line
plt.figure(figsize=(8, 5))
plt.loglog(freqs_welch[1:], psd_welch[1:], color="#2c4a8c", linewidth=1.2, label="Welch PSD")

# Overlay fit
fit_freqs = freqs_welch[2:80]
fit_line = 10 ** (intercept + slope * np.log10(fit_freqs))
plt.loglog(
    fit_freqs,
    fit_line,
    "r--",
    linewidth=1.5,
    label=f"1/f fit: slope = {slope:.2f}, R²={r_value**2:.2f}",
)
plt.xlabel("Frequency (Hz)")
plt.ylabel("PSD (µV²/Hz)")
plt.title("1/f Background in Neural Power Spectrum")
plt.legend()
plt.grid(True, alpha=0.3, which="both")
plt.tight_layout()
plt.savefig("figure_10-3-5_one_over_f_fit.png", dpi=150)
print("1/f example completed...\n")
