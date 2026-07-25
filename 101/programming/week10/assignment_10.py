"""
Assignment 10: Neural Signal Processing Pipeline
NEUR 101 — Introduction to Programming with Python for Neuroscience

Student name: _______________
Date: _______________

import matplotlib.pyplot as plt
from scipy import signal as sp_signal
from scipy.ndimage import gaussian_filter1d
from scipy.signal import butter, filtfilt, hilbert, iirnotch, sosfiltfilt
from scipy.stats import linregress
"""
import numpy as np

np.random.seed(101)  # DO NOT CHANGE — ensures reproducible grading

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Generate the Simulated Recording (15 points)
# ─────────────────────────────────────────────────────────────────────────────
# Build a two-channel broadband recording (shape: 2 x n_samples) using the
# parameters below. Do NOT change fs or duration.

fs = 20000  # Hz — sampling rate
duration = 10  # seconds
t = np.arange(0, duration, 1 / fs)

# TODO 1A: Create a theta oscillation that is present during ODD seconds only
#   (seconds 1, 3, 5, 7, 9). The theta amplitude should be 45 µV during
#   running and ~5 µV during rest. Use gaussian_filter1d (sigma=200 samples
#   at 1000 Hz) to smooth the amplitude envelope so there are no abrupt edges.
#   Theta frequency: 8 Hz.
#   Hint: build the envelope at 1000 Hz, then upsample to fs.

# TODO 1B: Create a delta background oscillation present throughout the
#   recording at 2 Hz, amplitude 20 µV.

# TODO 1C: Create a gamma oscillation (55 Hz, amplitude 8 µV) present only
#   during the EVEN seconds (0–1, 2–3, 4–5, 6–7, 8–9 — the rest periods).
#   Use the same smoothed envelope approach as theta.

# TODO 1D: Generate pink (1/f) noise with std = 1.0 µV.
#   Method: generate white noise in frequency domain, divide by sqrt(freq),
#   then inverse FFT. Normalize to std = 1.0 µV.
#   Note: generate at 1000 Hz (for the LFP-rate components) then upsample.

# TODO 1E: Build the two-channel recording.
#   Channel 1: theta + delta + gamma + pink noise + thermal noise (std=20 µV)
#   Channel 2: same LFP components at 60% amplitude + different thermal noise
#   Both channels should be shaped as 1D arrays of length len(t).

# TODO 1F: Add spike waveforms to each channel.
#   Use this waveform generator (do not modify):


def make_spike_waveform(fs, amplitude):
    """
    Build spike waveform
    """
    n = int(2.5 * fs / 1000)
    tw = np.linspace(0, 2.5, n)
    trough = -amplitude * np.exp(-((tw - 0.4) ** 2) / (2 * 0.12**2))
    rebound = amplitude * 0.35 * np.exp(-((tw - 1.1) ** 2) / (2 * 0.25**2))
    return trough + rebound


#   Channel 1: 20 Hz mean firing rate, spike amplitude 200 µV
#   Channel 2: 7 Hz mean firing rate,  spike amplitude 65 µV
#   Use a refractory Poisson process (refractory period = 2 ms).
#   Spikes should fire at a HIGHER rate (40 Hz) during running (odd seconds)
#   and LOWER rate (5 Hz) during rest (even seconds).

#   Stack into: recording = np.vstack([ch1, ch2])   shape: (2, len(t))


# ─────────────────────────────────────────────────────────────────────────────
# PART 2: Build the Signal Processing Pipeline (25 points)
# ─────────────────────────────────────────────────────────────────────────────
# Implement the five pipeline stages as standalone functions.
# Each function must have a docstring explaining its parameters and return values.

# TODO 2A: preprocess(data, fs, notch_freq=60)
#   - Remove DC offset with a 0.5 Hz high-pass filter (order 2)
#   - Apply a notch filter at notch_freq Hz
#   - Return: cleaned array, same shape as data

# TODO 2B: separate_signals(cleaned, fs, fs_lfp=1000)
#   - Extract LFP: band-pass 1–300 Hz, downsample to fs_lfp
#   - Extract MUA: high-pass > 300 Hz, keep at original fs
#   - Return: (lfp array at fs_lfp, mua array at fs, t_lfp, t_raw)

# TODO 2C: compute_psd(lfp, fs_lfp)
#   - Compute Welch PSD for each channel
#     nperseg = min(2048, n_samples // 4)
#     noverlap = nperseg // 2
#     scaling = 'density'
#   - Fit the 1/f slope using log-log linear regression (2–40 Hz)
#   - Return: (psd array shape n_ch x n_freqs, freqs, spectral_exponents)

# TODO 2D: compute_spectrogram(lfp, fs_lfp)
#   - Compute spectrogram for each channel
#     nperseg = 256, noverlap = 224, window = 'hann', scaling = 'density'
#   - Extract time-resolved band power for each canonical band:
#       Delta (0.5–4 Hz), Theta (4–8 Hz), Alpha (8–13 Hz),
#       Beta (13–30 Hz), Gamma (30–80 Hz)
#     using np.trapz across the frequency axis
#   - Return: (spectrograms array, freqs, times, band_timeseries dict)

# TODO 2E: detect_and_analyze_spikes(mua, fs)
#   - High-pass filter already done (mua is the output of separate_signals)
#   - For each channel:
#       * Estimate noise std: median(|x|) / 0.6745
#       * Set threshold = -4.0 * noise_std
#       * Detect negative crossings with 2 ms refractory period
#       * Extract waveforms: 0.5 ms pre-trough, 2.0 ms post-trough
#       * Compute: mean rate (Hz), ISI CV, refractory violation %
#   - Return: list of per-channel dicts with keys:
#       spike_times, waveforms, wf_time_ms, n_spikes,
#       mean_rate_hz, isi_cv, refract_pct, threshold_uv


# ─────────────────────────────────────────────────────────────────────────────
# PART 3: Run the Pipeline and Print a Summary (15 points)
# ─────────────────────────────────────────────────────────────────────────────

# TODO 3A: Run all five pipeline stages in the correct order and store results.
#   Print a one-line status message after each stage completes, e.g.:
#   "[Stage 1] Preprocessing complete — 2 channels, 200000 samples"

# TODO 3B: Print a structured text summary with the following sections:
#
#   ══════════════════════════════════════════
#   PIPELINE SUMMARY — WEEK 10 ASSIGNMENT
#   ══════════════════════════════════════════
#
#   Recording
#     Channels:         2
#     Duration:         10.0 s
#     Sampling rate:    20000 Hz
#     LFP rate:         1000 Hz
#
#   Channel 1 — Spectral
#     1/f exponent:     X.XX
#     Delta power:      X.XX µV²  (XX.X%)
#     Theta power:      X.XX µV²  (XX.X%)
#     Alpha power:      X.XX µV²  (XX.X%)
#     Beta power:       X.XX µV²  (XX.X%)
#     Gamma power:      X.XX µV²  (XX.X%)
#
#   Channel 1 — Spikes
#     Spikes detected:  XXX
#     Mean rate:        XX.X Hz
#     ISI CV:           X.XXX
#     Refract. viol.:   X.X%
#
#   [repeat for Channel 2]
#   ══════════════════════════════════════════


# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Produce Five Analysis Figures (30 points)
# ─────────────────────────────────────────────────────────────────────────────
# Each figure must have:
#   - A descriptive title
#   - Labeled axes (with units)
#   - A legend where multiple traces appear
# Save each figure as a .png file.

# TODO 4A — Figure 1: Raw and LFP-filtered signals (6 points)
#   Two-row figure. Top row: first 2 seconds of raw broadband signal for
#   both channels (overlay or subplots). Bottom row: corresponding LFP
#   (1–300 Hz filtered) for both channels.
#   Show the dramatic amplitude reduction after high-pass filtering removes
#   the LFP from the raw broadband trace.
#   Save as: "fig1_raw_vs_lfp.png"

# TODO 4B — Figure 2: Power spectral density comparison (6 points)
#   Single figure with two panels (one per channel), log-log scale.
#   On each panel:
#     - Plot the Welch PSD
#     - Shade the five canonical frequency bands with distinct colors
#     - Overlay the fitted 1/f line (dashed red)
#     - Label the spectral exponent and R² in the panel title or as text
#   Save as: "fig2_psd_comparison.png"

# TODO 4C — Figure 3: Spectrograms with behavioral annotation (6 points)
#   Two-row spectrogram figure (one row per channel), inferno colormap,
#   dB scale, frequency axis 0–100 Hz.
#   Add vertical dashed lines at every second (0, 1, 2, ... 10) to mark
#   the running/rest transitions.
#   Add a color bar labeled "Power (dB re µV²/Hz)".
#   Save as: "fig3_spectrograms.png"

# TODO 4D — Figure 4: Theta and gamma power timeseries (6 points)
#   For CHANNEL 1 only:
#   Plot theta power (4–8 Hz) and gamma power (30–80 Hz) as time series
#   on the same axes (use a twin y-axis if the scales differ greatly).
#   Shade running epochs (odd seconds) in light green and rest epochs
#   (even seconds) in light gray.
#   Add a legend distinguishing theta and gamma traces.
#   Save as: "fig4_band_power_timeseries.png"

# TODO 4E — Figure 5: Spike analysis panel (6 points)
#   Three-column figure for CHANNEL 1:
#   Left:   All spike waveforms overlaid (first 150 max), mean in red.
#           x-axis in ms, y-axis in µV.
#   Middle: ISI histogram (2 ms bins, 0–200 ms range).
#           Mark the 2 ms refractory line in red.
#           Title should include mean rate and ISI CV.
#   Right:  Scatter plot of trough depth vs. peak height for all waveforms.
#           Color points by their position in time (use a sequential colormap).
#           Include a colorbar labeled "Time (s)".
#   Save as: "fig5_spike_analysis.png"


# ─────────────────────────────────────────────────────────────────────────────
# PART 5: Neuroscience Interpretation (15 points)
# ─────────────────────────────────────────────────────────────────────────────
# Answer the three questions below as Python comments (# lines).
# Each answer should be 3–5 sentences. Use what you learned in Lectures
# 10.1–10.7 and the Week 10 neuroscience content.

# QUESTION 1 (5 points):
# Look at your Figure 3 spectrograms and Figure 4 theta/gamma timeseries.
# Describe what you observe about the relationship between behavioral state
# (running vs. rest) and the power in the theta and gamma bands. Why would
# you expect this pattern in a real hippocampal recording from a navigating
# rodent? What circuit-level mechanism generates the theta rhythm during
# locomotion?
#
# YOUR ANSWER:
# ...

# QUESTION 2 (5 points):
# Examine the spike statistics printed in your Part 3 summary. Compare the
# mean firing rate and ISI CV between channels 1 and 2. What does the ISI CV
# value tell you about the firing pattern of each neuron? If the refractory
# violation percentage were 8% instead of <2%, what would that indicate about
# the quality of the spike detection, and how would you address it?
#
# YOUR ANSWER:
# ...

# QUESTION 3 (5 points):
# In Figure 2, you fitted a 1/f line to the power spectrum. What does the
# spectral exponent (the slope of that line) represent biologically? If you
# were comparing recordings from a healthy control animal and an animal model
# of a neurological disorder and found that the disorder animal had a steeper
# (more negative) 1/f slope, what might that indicate about the underlying
# neural circuit? Name one neuroscience study area where 1/f slope changes
# have been reported as a biomarker.
#
# YOUR ANSWER:
# ...
