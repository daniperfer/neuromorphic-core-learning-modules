"""
Lecture 10.4: Spectrograms and Time-Frequency Analysis
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sp_signal
from scipy.signal import chirp

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

# -----------------------------------------
# Computing a Spectrogram with scipy.signal

# Compute spectrogram
freqs_spec, times_spec, Sxx = sp_signal.spectrogram(
    lfp,
    fs=fs,
    window="hann",
    nperseg=256,  # window length: 256 samples = 256 ms at 1000 Hz
    noverlap=224,  # 87.5% overlap → ~32 ms time step between columns
    scaling="density",  # power spectral density: µV²/Hz
)

print(f"Spectrogram shape: {Sxx.shape}")
print(f"  Frequency bins: {len(freqs_spec)} ({freqs_spec[0]:.1f}–{freqs_spec[-1]:.1f} Hz)")
print(f"  Time bins: {len(times_spec)} ({times_spec[0]:.3f}–{times_spec[-1]:.3f} s)")
print(f"  Frequency resolution: {freqs_spec[1] - freqs_spec[0]:.2f} Hz")
print(f"  Time resolution: {times_spec[1] - times_spec[0]:.3f} s")

# Plot spectrogram
fig, axes = plt.subplots(2, 1, figsize=(12, 7), gridspec_kw={"height_ratios": [1, 2]})

# Top: raw signal for reference
axes[0].plot(t, lfp, color="#333333", linewidth=0.7)
axes[0].set_ylabel("Voltage (µV)")
axes[0].set_title("Raw LFP Signal")
axes[0].set_xlim(t[0], t[-1])

# Bottom: spectrogram
# Use log scale for power — standard in neuroscience
im = axes[1].pcolormesh(
    times_spec, freqs_spec, 10 * np.log10(Sxx + 1e-12), shading="gouraud", cmap="inferno"
)
axes[1].set_ylim(0, 100)
axes[1].set_ylabel("Frequency (Hz)")
axes[1].set_xlabel("Time (s)")
axes[1].set_title("Spectrogram (Power in dB re µV²/Hz)")
axes[1].axhline(2, color="white", linestyle=":", alpha=0.7, label="2 Hz")
axes[1].axhline(8, color="white", linestyle=":", alpha=0.7, label="8 Hz")
axes[1].axhline(12, color="white", linestyle=":", alpha=0.7, label="12 Hz")
axes[1].axhline(25, color="white", linestyle=":", alpha=0.7, label="25 Hz")
axes[1].axhline(60, color="white", linestyle=":", alpha=0.7, label="60 Hz")

plt.colorbar(im, ax=axes[1], label="Power (dB)")

plt.tight_layout()
plt.savefig("figure_10-4-1_spectrogram_basic.png", dpi=150)
print("Spectrogram example completed...\n")

# ---------------------------------------
# The Window Length Trade-off in Practice

window_configs = [
    (64, 56, "Short window: 64 ms — fine time, coarse frequency"),
    (256, 224, "Medium window: 256 ms — balanced"),
    (512, 448, "Long window: 512 ms — coarse time, fine frequency"),
]

fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig.suptitle("Time-Frequency Resolution Trade-off", fontsize=13)

for ax, (nperseg, noverlap, title) in zip(axes, window_configs):
    f, t_s, Sxx_w = sp_signal.spectrogram(
        lfp, fs=fs, window="hann", nperseg=nperseg, noverlap=noverlap, scaling="density"
    )
    freq_res = f[1] - f[0]
    time_res = t_s[1] - t_s[0] if len(t_s) > 1 else nperseg / fs

    im = ax.pcolormesh(
        t_s,
        f,
        10 * np.log10(Sxx_w + 1e-12),
        shading="gouraud",
        cmap="inferno",
        vmin=-20,
        vmax=30,  # fixed color scale for fair comparison
    )
    ax.set_ylim(0, 80)
    ax.set_ylabel("Freq (Hz)")
    ax.set_title(f"{title}\n(Freq res: {freq_res:.1f} Hz | Time res: {time_res * 1000:.0f} ms)")
    plt.colorbar(im, ax=ax, label="dB")

axes[-1].set_xlabel("Time (s)")
plt.tight_layout()
plt.savefig("figure_10-4-2_spectrogram_window_tradeoff.png", dpi=150)
print("Window tradeoff example completed...\n")

# ------------------------------------------------------------
# Building a Non-Stationary Signal to Reveal Spectrogram Power

np.random.seed(7)
fs = 1000
duration = 10  # 10 seconds
t_long = np.arange(0, duration, 1 / fs)

# Delta: present throughout (sleep-like background)
delta_bg = 2.0 * np.sin(2 * np.pi * 2 * t_long)

# Theta: bursts during seconds 2–4 and 7–9 (navigation epochs)
theta_burst = np.zeros_like(t_long)
theta_burst[(t_long >= 2) & (t_long < 4)] = 3.0
theta_burst[(t_long >= 7) & (t_long < 9)] = 3.0
theta_sig = theta_burst * np.sin(2 * np.pi * 8 * t_long)

# Gamma: brief burst during second 5 (stimulus response)
gamma_burst = np.zeros_like(t_long)
gamma_burst[(t_long >= 4.8) & (t_long < 5.5)] = 2.0
gamma_sig = gamma_burst * np.sin(2 * np.pi * 60 * t_long)

# Chirp: frequency sweeping from 10 to 30 Hz during seconds 6–7 (arbitrary)
chirp_sig = np.zeros_like(t_long)
chirp_mask = (t_long >= 6) & (t_long < 7)
t_chirp = t_long[chirp_mask] - 6
chirp_sig[chirp_mask] = 1.5 * chirp(t_chirp, f0=10, f1=30, t1=1, method="linear")

# Pink noise background
freqs_n = np.fft.rfftfreq(len(t_long), d=1 / fs)
freqs_n[0] = 1
ns = np.random.randn(len(freqs_n)) + 1j * np.random.randn(len(freqs_n))
ns /= np.sqrt(freqs_n)
pink_noise = np.fft.irfft(ns, n=len(t_long))
pink_noise = 0.5 * (pink_noise / np.std(pink_noise))

lfp_dynamic = delta_bg + theta_sig + gamma_sig + chirp_sig + pink_noise

# Save for use in later lectures
np.save("week10_simulated_lfp_dynamic.npy", lfp_dynamic)
np.save("week10_time_axis_dynamic.npy", t_long)

# Plot signal and spectrogram together
freqs_d, times_d, Sxx_d = sp_signal.spectrogram(
    lfp_dynamic, fs=fs, window="hann", nperseg=256, noverlap=224, scaling="density"
)

fig, axes = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={"height_ratios": [1, 2.5]})

axes[0].plot(t_long, lfp_dynamic, color="#333333", linewidth=0.6)
axes[0].set_ylabel("Voltage (µV)")
axes[0].set_title("Dynamic LFP: Theta Bursts, Gamma Event, and Frequency Sweep")
axes[0].set_xlim(0, duration)
axes[0].axvspan(2, 4, alpha=0.08, color="green", label="Theta burst")
axes[0].axvspan(7, 9, alpha=0.08, color="green")
axes[0].axvspan(4.8, 5.5, alpha=0.08, color="orange", label="Gamma burst")
axes[0].axvspan(6, 7, alpha=0.08, color="purple", label="Freq sweep")
axes[0].legend(fontsize=8, loc="upper right")

im = axes[1].pcolormesh(
    times_d, freqs_d, 10 * np.log10(Sxx_d + 1e-12), shading="gouraud", cmap="inferno"
)
axes[1].set_ylim(0, 80)
axes[1].set_ylabel("Frequency (Hz)")
axes[1].set_xlabel("Time (s)")
axes[1].set_title("Spectrogram — Dynamic Oscillations Clearly Visible")
axes[1].axvline(2, color="lime", linewidth=0.8, alpha=0.6)
axes[1].axvline(4, color="lime", linewidth=0.8, alpha=0.6)
axes[1].axvline(7, color="lime", linewidth=0.8, alpha=0.6)
axes[1].axvline(9, color="lime", linewidth=0.8, alpha=0.6)
axes[1].axvline(4.8, color="orange", linewidth=0.8, alpha=0.6)
axes[1].axvline(5.5, color="orange", linewidth=0.8, alpha=0.6)
plt.colorbar(im, ax=axes[1], label="Power (dB re µV²/Hz)")

plt.tight_layout()
plt.savefig("figure_10-4-3_spectrogram_dynamic.png", dpi=150)
print("Dynamic signal spectrogram example completed...\n")

# --------------------------------------------------------
# Extracting Time-Resolved Band Power from the Spectrogram


def extract_band_power_timeseries(freqs, times, Sxx, band_low, band_high):
    """
    Extract a time-resolved power trace for a specific frequency band
    from a precomputed spectrogram.

    Parameters
    ----------
    freqs : np.ndarray
        Frequency axis from spectrogram()
    times : np.ndarray
        Time axis from spectrogram()
    Sxx : np.ndarray
        2D power array from spectrogram(), shape (n_freqs, n_times)
    band_low, band_high : float
        Frequency band limits in Hz

    Returns
    -------
    np.ndarray
        1D array of band power at each time point (µV²)
    """
    band_mask = (freqs >= band_low) & (freqs <= band_high)
    # Integrate power across the band using the trapezoidal rule
    band_power = np.trapezoid(Sxx[band_mask, :], freqs[band_mask], axis=0)
    return band_power


# Extract theta and gamma power over time from the dynamic signal
theta_power_t = extract_band_power_timeseries(freqs_d, times_d, Sxx_d, 6, 10)
gamma_power_t = extract_band_power_timeseries(freqs_d, times_d, Sxx_d, 30, 80)
delta_power_t = extract_band_power_timeseries(freqs_d, times_d, Sxx_d, 1, 4)

fig, axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)
fig.suptitle("Time-Resolved Band Power Extracted from Spectrogram", fontsize=12)

for ax, (power_ts, label, color, lo, hi) in zip(
    axes,
    [
        (theta_power_t, "Theta (6–10 Hz)", "#66bb66", 2, 4),
        (gamma_power_t, "Gamma (30–80 Hz)", "#aa44aa", 4.8, 5.5),
        (delta_power_t, "Delta (1–4 Hz)", "#6699cc", None, None),
    ],
):
    ax.plot(times_d, power_ts, color=color, linewidth=1.2)
    ax.set_ylabel("Power (µV²)")
    ax.set_title(label)
    if lo is not None:
        ax.axvspan(lo, hi, alpha=0.12, color=color, label="Expected burst")
        assert lo is not None
        assert hi is not None
        ax.axvspan(lo + 5, hi + 5, alpha=0.12, color=color)
        ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

axes[-1].set_xlabel("Time (s)")
plt.tight_layout()
plt.savefig("figure_10-4-4_band_power_timeseries.png", dpi=150)

# Confirm the gamma power increase quantitatively
g_burst_power = np.mean(gamma_power_t[(times_d >= 2) & (times_d < 4)])
g_baseline_power = np.mean(gamma_power_t[(times_d >= 0) & (times_d < 2)])
print(f"Theta power during burst:   {g_burst_power:.4f} µV²")
print(f"Theta power at baseline:    {g_baseline_power:.4f} µV²")
print(f"Burst / baseline ratio:     {g_burst_power / (g_baseline_power + 1e-9):.1f}x")
print()

# -------------------------------------
# Choosing the Right Colormap and Scale

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Spectrogram: Color Scale and Colormap Comparison", fontsize=12)

configs = [
    (Sxx_d, "viridis", "Linear power, viridis"),
    (Sxx_d, "hot", "Linear power, hot"),
    (10 * np.log10(Sxx_d + 1e-12), "inferno", "dB scale, inferno (standard)"),
    (10 * np.log10(Sxx_d + 1e-12), "RdBu_r", "dB scale, RdBu_r (diverging)"),
]

for ax, (data, cmap, title) in zip(axes.flat, configs):
    im = ax.pcolormesh(times_d, freqs_d, data, shading="gouraud", cmap=cmap)
    ax.set_ylim(0, 80)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Freq (Hz)")
    plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.savefig("figure_10-4-5_spectrogram_colormap_comparison.png", dpi=150)
print("Colormap example completed...")
