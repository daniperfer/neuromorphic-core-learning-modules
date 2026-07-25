"""
Lecture 10.1: What Is a Signal? Sampling, Nyquist, and Neural Recordings
"""

import matplotlib.pyplot as plt
import numpy as np

# Simulate a continuous neural oscillation (10 Hz alpha wave)
# In reality this would come from your recording system
fs = 1000  # sampling rate in Hz (samples per second)
duration = 2.0  # seconds
t = np.arange(0, duration, 1 / fs)  # time array: [0, 0.001, 0.002, ..., 1.999]

# A simple sinusoidal signal at 10 Hz (alpha band)
frequency = 10  # Hz
amplitude = 50  # microvolts
signal = amplitude * np.sin(2 * np.pi * frequency * t)

print(f"Sampling rate: {fs} Hz")
print(f"Number of samples: {len(t)}")
print(f"Time resolution: {1 / fs * 1000:.2f} ms per sample")
print(f"Signal shape: {signal.shape}")

plt.figure(figsize=(10, 4))
plt.plot(t[:200], signal[:200])  # first 200 ms
plt.xlabel("Time (s)")
plt.ylabel("Voltage (µV)")
plt.title("Simulated 10 Hz Alpha Oscillation (first 200 ms)")
plt.tight_layout()
plt.savefig("figure_10-1-1_alpha_oscillation.png", dpi=150)
print()

# Comparing time resolution at different sampling rates
sampling_rates = {
    "LFP recording": 1000,
    "EEG recording": 512,
    "Spike sorting": 30000,
    "High-dens. silicon probe": 40000,
}

print("Sampling Rate Comparison:")
print(f"{'System':<25} {'Rate (Hz)':<15} {'Time resolution':<20} {'Max detectable freq'}")
print("-" * 75)
for system, fs in sampling_rates.items():
    dt_ms = (1 / fs) * 1000
    max_freq = fs / 2
    print(f"{system:<25} {fs:<15} {dt_ms:.3f} ms{'':<14} {max_freq:.0f} Hz")
print()

# ------------------------------------
# The Nyquist-Shannon Sampling Theorem

# Demonstrating the Nyquist theorem visually
true_freq = 10  # Hz — the actual signal frequency
t_continuous = np.linspace(0, 0.5, 10000)  # "continuous" time
true_signal = np.sin(2 * np.pi * true_freq * t_continuous)

fig, axes = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle("Effect of Sampling Rate on Signal Reconstruction", fontsize=13)

sampling_scenarios = [
    (15, "Under-sampled (15 Hz — below Nyquist)", "red"),
    (25, "Just above Nyquist (25 Hz)", "orange"),
    (200, "Well-sampled (200 Hz)", "green"),
]

for ax, (fs_demo, label, color) in zip(axes, sampling_scenarios):
    t_sampled = np.arange(0, 0.5, 1 / fs_demo)
    sampled = np.sin(2 * np.pi * true_freq * t_sampled)

    ax.plot(t_continuous, true_signal, "gray", alpha=0.4, label="True signal")
    ax.stem(
        t_sampled,
        sampled,
        linefmt=color,
        markerfmt="C0o",
        basefmt=" ",
        label=f"Samples ({fs_demo} Hz)",
    )
    ax.set_title(label)
    ax.set_ylabel("Amplitude")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_xlim(0, 0.5)

axes[-1].set_xlabel("Time (s)")
plt.tight_layout()
plt.savefig("figure_10-1-2_nyquist_demo.png", dpi=150)
print()

# ----------------------------------------
# Aliasing: The Enemy of Neural Recordings

# Demonstrating aliasing mathematically
fs_low = 30  # Hz — dangerously low sampling rate for illustration
true_freq = 25  # Hz — actual signal frequency
alias_freq = abs(true_freq - fs_low)  # = 5 Hz — what we'd measure
fs_nyq = fs_low * 2

t_demo = np.linspace(0, 1.0, 10000)
t_sampled = np.arange(0, 1.0, 1 / fs_low)
t_nyq = np.arange(0, 1.0, 1 / fs_nyq)

true_wave = np.sin(2 * np.pi * true_freq * t_demo)
alias_wave = np.sin(2 * np.pi * alias_freq * t_demo - np.pi)
sampled_points = np.sin(2 * np.pi * true_freq * t_sampled)
nyq_points = np.sin(2 * np.pi * true_freq * t_nyq)

plt.figure(figsize=(10, 4))
plt.plot(t_demo, true_wave, "blue", alpha=0.5, label=f"True signal: {true_freq} Hz")
plt.plot(t_demo, alias_wave, "red", alpha=0.7, label=f"Alias: {alias_freq} Hz (what we measure)")
plt.plot(t_nyq, nyq_points, "go", markersize=6, label=f"{fs_nyq:.1f} Hz sampled points")
plt.plot(t_sampled, sampled_points, "ko", markersize=6, label="30 Hz sample points")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Aliasing: A 25 Hz Signal Sampled at 30 Hz Appears as 5 Hz")
plt.legend()
plt.tight_layout()
plt.savefig("figure_10-1-3_aliasing_demo.png", dpi=150)

print(f"True signal frequency: {true_freq} Hz")
print(f"Sampling rate: {fs_low} Hz")
print(f"Nyquist frequency: {fs_low / 2} Hz")
print(f"Alias frequency: {alias_freq} Hz  ← this is the false signal we'd record")
print()

# ---------------------------------------------
# Working with Real Neural Recording Parameters


def describe_recording(fs, duration, n_channels=1):
    """
    Print key properties of a neural recording given its parameters.

    Parameters
    ----------
    fs : float
        Sampling rate in Hz
    duration : float
        Recording duration in seconds
    n_channels : int
        Number of simultaneously recorded channels
    """
    n_samples = int(fs * duration)
    nyquist = fs / 2
    dt_ms = (1 / fs) * 1000
    memory_mb = (n_samples * n_channels * 2) / (1024**2)  # int16 = 2 bytes

    print("Recording Parameters:")
    print(f"  Sampling rate:       {fs:,.0f} Hz")
    print(f"  Duration:            {duration:.1f} s")
    print(f"  Channels:            {n_channels}")
    print(f"  Samples per channel: {n_samples:,}")
    print(f"  Total samples:       {n_samples * n_channels:,}")
    print(f"  Time resolution:     {dt_ms:.4f} ms")
    print(f"  Nyquist frequency:   {nyquist:,.0f} Hz")
    print(f"  Est. memory (int16): {memory_mb:.1f} MB")
    print()


# Typical LFP recording setup
describe_recording(fs=1000, duration=600, n_channels=32)

# High-density silicon probe for spike sorting
describe_recording(fs=30000, duration=3600, n_channels=64)
print()

# --------------------------------------------------
# Creating a Simulated Multi-Frequency Neural Signal

np.random.seed(42)  # reproducibility

fs = 1000  # Hz — standard LFP sampling rate
duration = 5  # seconds
t = np.arange(0, duration, 1 / fs)

# Layered oscillations matching real neural frequency bands
delta = 3.0 * np.sin(2 * np.pi * 2 * t)  # 2 Hz delta
theta = 2.0 * np.sin(2 * np.pi * 8 * t)  # 8 Hz theta
alpha = 1.5 * np.sin(2 * np.pi * 12 * t)  # 12 Hz alpha
beta = 0.8 * np.sin(2 * np.pi * 25 * t)  # 25 Hz beta
gamma = 0.4 * np.sin(2 * np.pi * 60 * t)  # 60 Hz gamma

# Add 1/f ("pink") noise — characteristic of real brain recordings
freqs = np.fft.rfftfreq(len(t), d=1 / fs)
freqs[0] = 1  # avoid division by zero
noise_spectrum = np.random.randn(len(freqs)) + 1j * np.random.randn(len(freqs))
noise_spectrum /= np.sqrt(freqs)  # 1/f shaping
pink_noise = np.fft.irfft(noise_spectrum, n=len(t))
pink_noise = 1.0 * (pink_noise / np.std(pink_noise))  # normalize to 1 µV std

# Composite LFP signal
lfp = delta + theta + alpha + beta + gamma + pink_noise

print("Simulated LFP signal:")
print(f"  Length: {len(lfp)} samples ({duration} s at {fs} Hz)")
print(f"  Mean: {np.mean(lfp):.3f} µV")
print(f"  Std:  {np.std(lfp):.3f} µV")
print(f"  Min:  {np.min(lfp):.3f} µV")
print(f"  Max:  {np.max(lfp):.3f} µV")

# Save for use in later lectures
filename_signal = "week10_simulated_lfp.npy"
filename_time = "week10_time_axis.npy"
np.save(f"{filename_signal}", lfp)
np.save(f"{filename_time}", t)
print(f"\nSaved {filename_signal} and {filename_time} for use in later lectures.")

# Plot first 2 seconds
plt.figure(figsize=(12, 4))
mask = t < 2
plt.plot(t[mask], lfp[mask], color="#2c4a8c", linewidth=0.8)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (µV)")
plt.title("Simulated LFP Signal (first 2 s) — Delta + Theta + Alpha + Beta + Gamma + Pink Noise")
plt.tight_layout()
plt.savefig("figure_10-1-4_simulated_lfp_raw.png", dpi=150)
print()
