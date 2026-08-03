"""
Lecture 10.7: Building a Signal Processing Pipeline for Neural Data
"""

import time

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sp_signal

# from scipy.ndimage import gaussian_filter1d
from scipy.signal import butter, hilbert, sosfiltfilt
from scipy.stats import linregress

# from collections import defaultdict


# ── Utility functions (assembled from previous lectures) ──────────────────────


def butter_filter(data, cutoff, fs, filter_type, order=4):
    """Zero-phase Butterworth filter. Handles low/high/bandpass."""
    nyquist = fs / 2
    if filter_type in ("bandpass", "bandstop"):
        normalized = [c / nyquist for c in cutoff]
    else:
        normalized = cutoff / nyquist
    sos = butter(order, normalized, btype=filter_type, output="sos")
    return sosfiltfilt(sos, data)


def notch_filter(data, notch_freq, fs, quality_factor=30):
    """Remove a narrow frequency band (e.g., 60 Hz power line noise)."""
    from scipy.signal import iirnotch

    b, a = iirnotch(notch_freq, quality_factor, fs)
    from scipy.signal import filtfilt

    return filtfilt(b, a, data)


def estimate_noise_std(signal):
    """Robust noise std via median absolute deviation (Quiroga et al. 2004)."""
    return np.median(np.abs(signal)) / 0.6745


def detect_spikes(signal, fs, threshold_multiplier=4.0, refractory_ms=2.0):
    """Negative threshold-crossing spike detector with refractory period."""
    noise_std = estimate_noise_std(signal)
    threshold = -threshold_multiplier * noise_std
    refractory_samples = int(refractory_ms * fs / 1000)
    spike_samples = []
    i = 0
    while i < len(signal) - 1:
        if signal[i] <= threshold:
            search_end = min(i + int(2 * fs / 1000), len(signal))
            local_min = i + np.argmin(signal[i:search_end])
            spike_samples.append(local_min)
            i = local_min + refractory_samples
        else:
            i += 1
    return np.array(spike_samples), threshold, noise_std


def extract_waveforms(signal, spike_samples, fs, pre_ms=0.5, post_ms=2.0):
    """Extract aligned waveform snippets around each detected spike."""
    pre = int(pre_ms * fs / 1000)
    post = int(post_ms * fs / 1000)
    waveforms, valid = [], []
    for idx in spike_samples:
        if idx - pre >= 0 and idx + post < len(signal):
            waveforms.append(signal[idx - pre : idx + post])
            valid.append(idx)
    wf_time = np.linspace(-pre_ms, post_ms, pre + post)
    return np.array(waveforms), wf_time, np.array(valid)


def compute_band_power(psd, freqs, lo, hi):
    """Integrate PSD across a frequency band using the trapezoidal rule."""
    idx = (freqs >= lo) & (freqs <= hi)
    return float(np.trapezoid(psd[idx], freqs[idx]))


def bandpass_envelope(signal, lo, hi, fs):
    """Instantaneous amplitude envelope via Hilbert transform."""
    hi = min(hi, fs / 2 - 1)
    filtered = butter_filter(signal, [lo, hi], fs, "bandpass")
    envelope = np.abs(hilbert(filtered))
    return filtered, envelope


# ------------------------
# The NeuralPipeline Class


class NeuralPipeline:
    """
    End-to-end signal processing pipeline for extracellular neural recordings.

    Accepts a multi-channel broadband recording and produces:
      - Cleaned broadband signal (DC removed, notch filtered)
      - LFP stream (band-pass 1–300 Hz, downsampled)
      - MUA / spike stream (high-pass > 300 Hz, original rate)
      - Power spectral density (Welch) per channel
      - Band power values for all canonical bands
      - Time-resolved band power traces (from spectrogram)
      - Detected spike times, waveforms, and ISI statistics
      - Summary report figures

    Parameters
    ----------
    fs_raw : float
        Sampling rate of the input recording in Hz
    fs_lfp : float
        Target sampling rate for the LFP stream (default 1000 Hz)
    notch_freq : float
        Power line noise frequency to remove (60 Hz in US, 50 Hz in Europe)
    spike_threshold : float
        Spike detection threshold in units of noise std (default 4.0)
    lfp_band : tuple
        (low, high) cutoffs for LFP extraction in Hz (default (1, 300))
    spike_hp_cutoff : float
        High-pass cutoff for MUA/spike stream in Hz (default 300)
    """

    CANONICAL_BANDS = {
        "Delta": (0.5, 4, "#4a90d9"),
        "Theta": (4, 8, "#5cb85c"),
        "Alpha": (8, 13, "#f0ad4e"),
        "Beta": (13, 30, "#d9534f"),
        "Low Gamma": (30, 70, "#9b59b6"),
        "High Gamma": (70, 150, "#6c3483"),
    }

    def __init__(
        self,
        fs_raw=30000,
        fs_lfp=1000,
        notch_freq=60,
        spike_threshold=4.0,
        lfp_band=(1, 300),
        spike_hp_cutoff=300,
    ):
        self.fs_raw = fs_raw
        self.fs_lfp = fs_lfp
        self.notch_freq = notch_freq
        self.spike_threshold = spike_threshold
        self.lfp_band = lfp_band
        self.spike_hp_cutoff = spike_hp_cutoff
        self.results = {}
        self._log = []

    # ── Internal helpers ────────────────────────────────────────────────────

    def _log_step(self, message):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self._log.append(entry)
        print(entry)

    def _validate_input(self, data):
        """Check data dimensions and flag obvious problems."""
        if data.ndim == 1:
            data = data[np.newaxis, :]  # treat as single channel
        if data.ndim != 2:
            raise ValueError(f"Expected 2D array (n_channels, n_samples), got shape {data.shape}")
        n_channels, n_samples = data.shape
        duration = n_samples / self.fs_raw
        if duration < 1.0:
            raise ValueError(f"Recording too short ({duration:.2f} s). Need at least 1 s.")
        nyquist = self.fs_raw / 2
        if self.lfp_band[1] >= nyquist:
            raise ValueError(
                f"LFP upper cutoff ({self.lfp_band[1]} Hz) exceeds Nyquist ({nyquist} Hz)."
            )
        self._log_step(
            f"Input validated: {n_channels} channel(s), {n_samples:,} samples, "
            f"{duration:.2f} s at {self.fs_raw} Hz"
        )
        return data

    # ── Stage 1: Preprocessing ────────────────────────────────────────────

    def preprocess(self, data):
        """
        Stage 1: DC removal and notch filtering.

        Returns cleaned broadband signal at the original sampling rate.
        """
        self._log_step("Stage 1: Preprocessing")
        n_channels, _ = data.shape
        cleaned = np.zeros_like(data, dtype=float)

        for ch in range(n_channels):
            # Remove DC offset (high-pass at 0.5 Hz)
            dc_removed = butter_filter(data[ch].astype(float), 0.5, self.fs_raw, "high", order=2)
            # Remove power line noise
            notched = notch_filter(dc_removed, self.notch_freq, self.fs_raw)
            cleaned[ch] = notched

        self.results["broadband_clean"] = cleaned
        self._log_step(
            f"  DC removal (0.5 Hz HP) + {self.notch_freq} Hz notch — done "
            f"({n_channels} channel(s))"
        )
        return cleaned

    # ── Stage 2: Signal Separation ─────────────────────────────────────────

    def separate_signals(self, cleaned):
        """
        Stage 2: Separate LFP and MUA streams from the cleaned broadband signal.

        LFP stream: band-pass filtered, downsampled to fs_lfp.
        MUA stream: high-pass filtered, kept at fs_raw.
        """
        self._log_step("Stage 2: Signal separation (LFP / MUA)")
        n_channels, n_samples = cleaned.shape
        downsample_factor = int(self.fs_raw / self.fs_lfp)
        n_lfp_samples = n_samples // downsample_factor

        lfp_all = np.zeros((n_channels, n_lfp_samples))
        mua_all = np.zeros_like(cleaned)

        for ch in range(n_channels):
            # LFP: band-pass then downsample
            lfp_bp = butter_filter(cleaned[ch], list(self.lfp_band), self.fs_raw, "bandpass")
            lfp_all[ch] = lfp_bp[::downsample_factor][:n_lfp_samples]
            # MUA: high-pass
            mua_all[ch] = butter_filter(cleaned[ch], self.spike_hp_cutoff, self.fs_raw, "high")

        self.results["lfp"] = lfp_all
        self.results["mua"] = mua_all
        self.results["fs_lfp"] = self.fs_lfp
        self.results["fs_mua"] = self.fs_raw
        self.results["downsample_factor"] = downsample_factor

        _ = n_samples / self.fs_raw  # duration
        t_lfp = np.arange(n_lfp_samples) / self.fs_lfp
        t_raw = np.arange(n_samples) / self.fs_raw
        self.results["t_lfp"] = t_lfp
        self.results["t_raw"] = t_raw

        self._log_step(
            f"  LFP: {self.lfp_band[0]}–{self.lfp_band[1]} Hz BP, "
            f"downsampled {downsample_factor}x → {self.fs_lfp} Hz "
            f"({n_lfp_samples:,} samples)"
        )
        self._log_step(
            f"  MUA: >{self.spike_hp_cutoff} Hz HP, kept at {self.fs_raw} Hz "
            f"({n_samples:,} samples)"
        )
        return lfp_all, mua_all

    # ── Stage 3: Spectral Analysis ─────────────────────────────────────────

    def spectral_analysis(self, lfp_all):
        """
        Stage 3: Compute PSD (Welch) and band powers for each LFP channel.
        """
        self._log_step("Stage 3: Spectral analysis")
        n_channels, n_samples = lfp_all.shape
        fs = self.fs_lfp

        nperseg = min(2048, n_samples // 4)

        psds, freqs_list, band_powers_all = [], [], []

        for ch in range(n_channels):
            freqs_w, psd = sp_signal.welch(
                lfp_all[ch],
                fs=fs,
                window="hann",
                nperseg=nperseg,
                noverlap=nperseg // 2,
                scaling="density",
            )
            psds.append(psd)
            freqs_list.append(freqs_w)

            # Band powers
            ch_bands = {}
            total = compute_band_power(psd, freqs_w, 0.5, 150)
            for band, (lo, hi, _) in self.CANONICAL_BANDS.items():
                hi_clip = min(hi, fs / 2 - 1)
                bp = compute_band_power(psd, freqs_w, lo, hi_clip)
                ch_bands[band] = {"power_uv2": bp, "fraction": bp / total if total > 0 else 0}
            band_powers_all.append(ch_bands)

        self.results["psd"] = np.array(psds)
        self.results["psd_freqs"] = freqs_list[0]
        self.results["band_powers"] = band_powers_all

        # Fit 1/f slope for each channel
        slopes = []
        for psd in psds:
            mask = (freqs_list[0] >= 2) & (freqs_list[0] <= 40)
            slope, intercept, r, *_ = linregress(
                np.log10(freqs_list[0][mask]), np.log10(psd[mask] + 1e-30)
            )
            slopes.append(slope)
        self.results["spectral_exponent"] = np.array(slopes)

        self._log_step(
            f"  Welch PSD: nperseg={nperseg}, "
            f"freq resolution={freqs_list[0][1] - freqs_list[0][0]:.3f} Hz"
        )
        self._log_step(f"  1/f exponents: {[f'{s:.2f}' for s in slopes]}")
        return np.array(psds), freqs_list[0], band_powers_all

    # ── Stage 4: Time-Frequency Analysis ───────────────────────────────────

    def time_frequency_analysis(self, lfp_all):
        """
        Stage 4: Compute spectrogram and time-resolved band power for each channel.
        """
        self._log_step("Stage 4: Time-frequency analysis (spectrograms)")
        n_channels, n_samples = lfp_all.shape
        fs = self.fs_lfp

        nperseg = min(256, n_samples // 8)
        noverlap = int(nperseg * 0.875)

        spectrograms, spec_freqs, spec_times = [], None, None
        band_timeseries_all = []

        for ch in range(n_channels):
            f, t_s, Sxx = sp_signal.spectrogram(
                lfp_all[ch],
                fs=fs,
                window="hann",
                nperseg=nperseg,
                noverlap=noverlap,
                scaling="density",
            )
            spectrograms.append(Sxx)
            if spec_freqs is None:
                spec_freqs = f
                spec_times = t_s

            # Time-resolved band power for each canonical band
            ch_band_ts = {}
            for band, (lo, hi, _) in self.CANONICAL_BANDS.items():
                hi_clip = min(hi, fs / 2 - 1)
                band_mask = (f >= lo) & (f <= hi_clip)
                if band_mask.any():
                    ch_band_ts[band] = np.trapezoid(Sxx[band_mask, :], f[band_mask], axis=0)
                else:
                    ch_band_ts[band] = np.zeros(len(t_s))
            band_timeseries_all.append(ch_band_ts)

        self.results["spectrograms"] = np.array(spectrograms)
        self.results["spec_freqs"] = spec_freqs
        self.results["spec_times"] = spec_times
        self.results["band_timeseries"] = band_timeseries_all

        self._log_step(
            f"  Spectrogram: nperseg={nperseg}, "
            f"time resolution={spec_times[1] - spec_times[0]:.3f} s "
            f"({len(spec_times)} time bins)"
        )
        return np.array(spectrograms), spec_freqs, spec_times

    # ── Stage 5: Spike Detection ──────────────────────────────────────────

    def spike_detection(self, mua_all):
        """
        Stage 5: Detect spikes, extract waveforms, and compute ISI statistics.
        """
        self._log_step("Stage 5: Spike detection")
        n_channels = mua_all.shape[0]
        fs = self.fs_raw

        spike_results = []

        for ch in range(n_channels):
            spike_samples, threshold, noise_std = detect_spikes(
                mua_all[ch], fs, threshold_multiplier=self.spike_threshold
            )
            spike_times = spike_samples / fs

            waveforms, wf_time, valid_samples = extract_waveforms(mua_all[ch], spike_samples, fs)

            # ISI statistics
            if len(spike_times) >= 2:
                isis_ms = np.diff(np.sort(spike_times)) * 1000
                mean_rate = 1000 / np.mean(isis_ms)
                cv = np.std(isis_ms) / np.mean(isis_ms)
                refract_violations = int(np.sum(isis_ms < 2.0))
                refract_pct = 100 * refract_violations / len(isis_ms)
            else:
                isis_ms = np.array([])
                mean_rate, cv, refract_violations, refract_pct = 0, 0, 0, 0

            ch_result = {
                "spike_times": spike_times,
                "spike_samples": valid_samples,
                "waveforms": waveforms,
                "wf_time_ms": wf_time,
                "n_spikes": len(spike_times),
                "threshold_uv": threshold,
                "noise_std_uv": noise_std,
                "mean_rate_hz": mean_rate,
                "isi_cv": cv,
                "isis_ms": isis_ms,
                "refract_violations": refract_violations,
                "refract_pct": refract_pct,
            }
            spike_results.append(ch_result)

            self._log_step(
                f"  Channel {ch + 1}: {len(spike_times)} spikes, "
                f"{mean_rate:.1f} Hz, CV={cv:.2f}, "
                f"refract violations={refract_violations} ({refract_pct:.1f}%)"
            )

        self.results["spikes"] = spike_results
        return spike_results

    # ── Main run method ────────────────────────────────────────────────────

    def run(self, raw_data):
        """
        Execute the full pipeline on raw_data.

        Parameters
        ----------
        raw_data : np.ndarray
            Shape (n_channels, n_samples) or (n_samples,) for single channel.
            Values in µV, sampled at self.fs_raw Hz.

        Returns
        -------
        dict
            self.results — all pipeline outputs keyed by name.
        """
        t_start = time.time()
        self._log_step("=" * 55)
        self._log_step("NeuralPipeline: starting full run")
        self._log_step("=" * 55)

        data = self._validate_input(raw_data)
        cleaned = self.preprocess(data)
        lfp_all, mua_all = self.separate_signals(cleaned)
        self.spectral_analysis(lfp_all)
        self.time_frequency_analysis(lfp_all)
        self.spike_detection(mua_all)

        elapsed = time.time() - t_start
        self._log_step(f"Pipeline complete in {elapsed:.2f} s")
        self._log_step("=" * 55)

        self.results["processing_log"] = self._log.copy()
        return self.results

    # ── Reporting ─────────────────────────────────────────────────────────

    def summary_report(self, channel=0):
        """
        Generate a multi-panel summary figure for one channel.

        Parameters
        ----------
        channel : int
            Channel index to visualize (0-based)
        """
        if not self.results:
            raise RuntimeError("Run the pipeline first with .run(data)")

        r = self.results
        ch = channel
        fs_lfp = r["fs_lfp"]

        fig = plt.figure(figsize=(16, 14))
        fig.suptitle(
            f"NeuralPipeline Summary Report — Channel {ch + 1}",
            fontsize=14,
            fontweight="bold",
            y=0.98,
        )

        gs = gridspec.GridSpec(4, 3, figure=fig, hspace=0.55, wspace=0.38)

        # ── Panel 1: LFP time trace ───────────────────────────────────────
        ax1 = fig.add_subplot(gs[0, :2])
        t_lfp = r["t_lfp"]
        lfp_ch = r["lfp"][ch]
        ax1.plot(t_lfp, lfp_ch, color="#2c4a8c", linewidth=0.6)
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("µV")
        ax1.set_title("LFP (1–300 Hz)")
        ax1.set_xlim(t_lfp[0], t_lfp[-1])

        # ── Panel 2: Power spectrum ───────────────────────────────────────
        ax2 = fig.add_subplot(gs[0, 2])
        freqs_w = r["psd_freqs"]
        psd_ch = r["psd"][ch]
        ax2.semilogy(freqs_w[1:], psd_ch[1:], color="#2c4a8c", linewidth=1.2)
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("PSD (µV²/Hz)")
        ax2.set_title("Power Spectrum (Welch)")
        ax2.set_xlim(0, min(200, fs_lfp / 2))
        for band, (lo, hi, col) in self.CANONICAL_BANDS.items():
            ax2.axvspan(lo, min(hi, fs_lfp / 2 - 1), alpha=0.12, color=col)
        ax2.grid(True, alpha=0.25)

        # ── Panel 3: Spectrogram ─────────────────────────────────────────
        ax3 = fig.add_subplot(gs[1, :2])
        Sxx = r["spectrograms"][ch]
        t_s = r["spec_times"]
        f_s = r["spec_freqs"]
        im = ax3.pcolormesh(t_s, f_s, 10 * np.log10(Sxx + 1e-12), shading="gouraud", cmap="inferno")
        ax3.set_ylim(0, min(100, fs_lfp / 2))
        ax3.set_ylabel("Frequency (Hz)")
        ax3.set_xlabel("Time (s)")
        ax3.set_title("Spectrogram")
        plt.colorbar(im, ax=ax3, label="dB")

        # ── Panel 4: Band power bar chart ────────────────────────────────
        ax4 = fig.add_subplot(gs[1, 2])
        band_data = r["band_powers"][ch]
        names = list(band_data.keys())
        fracs = [band_data[n]["fraction"] * 100 for n in names]
        colors = [self.CANONICAL_BANDS[n][2] for n in names]
        bars = ax4.bar(names, fracs, color=colors, edgecolor="white")
        ax4.set_ylabel("% of Total Power")
        ax4.set_title("Band Power Distribution")
        ax4.tick_params(axis="x", rotation=30, labelsize=7)
        for bar, pct in zip(bars, fracs):
            ax4.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"{pct:.1f}%",
                ha="center",
                fontsize=7,
            )

        # ── Panel 5: Time-resolved band power ────────────────────────────
        ax5 = fig.add_subplot(gs[2, :2])
        for band, (lo, hi, col) in self.CANONICAL_BANDS.items():
            ts = r["band_timeseries"][ch][band]
            ax5.plot(t_s, ts / (ts.max() + 1e-12), color=col, linewidth=0.9, alpha=0.85, label=band)
        ax5.set_xlabel("Time (s)")
        ax5.set_ylabel("Normalized power")
        ax5.set_title("Time-Resolved Band Power (normalized)")
        ax5.legend(fontsize=7, ncol=3, loc="upper right")
        ax5.set_xlim(t_s[0], t_s[-1])

        # ── Panel 6: Spike waveforms ──────────────────────────────────────
        ax6 = fig.add_subplot(gs[2, 2])
        sp = r["spikes"][ch]
        if sp["n_spikes"] > 0:
            wfs = sp["waveforms"]
            wft = sp["wf_time_ms"]
            ax6.plot(wft, wfs[: min(100, len(wfs))].T, color="#2c4a8c", alpha=0.08, linewidth=0.5)
            ax6.plot(wft, np.mean(wfs, axis=0), color="red", linewidth=2.0, label="Mean")
            ax6.axvline(0, color="gray", linewidth=0.6, linestyle="--")
            ax6.set_xlabel("Time (ms)")
            ax6.set_ylabel("µV")
            ax6.set_title(f"Spike Waveforms (n={sp['n_spikes']})")
            ax6.legend(fontsize=8)
        else:
            ax6.text(
                0.5, 0.5, "No spikes detected", ha="center", va="center", transform=ax6.transAxes
            )
            ax6.set_title("Spike Waveforms")

        # ── Panel 7: ISI distribution ─────────────────────────────────────
        ax7 = fig.add_subplot(gs[3, :2])
        if sp["n_spikes"] >= 2:
            isis = sp["isis_ms"]
            bins = np.arange(0, min(200, isis.max() + 5), 2)
            ax7.hist(isis, bins=bins, color="#2c4a8c", edgecolor="white", linewidth=0.3)
            ax7.axvline(
                2.0,
                color="red",
                linestyle="--",
                linewidth=1.2,
                label=f"Refractory (2 ms) — {sp['refract_violations']} violations",
            )
            ax7.set_xlabel("ISI (ms)")
            ax7.set_ylabel("Count")
            ax7.set_title(
                f"ISI Distribution | Rate: {sp['mean_rate_hz']:.1f} Hz | " f"CV: {sp['isi_cv']:.2f}"
            )
            ax7.legend(fontsize=8)
        else:
            ax7.text(
                0.5,
                0.5,
                "Insufficient spikes for ISI analysis",
                ha="center",
                va="center",
                transform=ax7.transAxes,
            )

        # ── Panel 8: Text summary ─────────────────────────────────────────
        ax8 = fig.add_subplot(gs[3, 2])
        ax8.axis("off")
        duration = len(r["lfp"][ch]) / r["fs_lfp"]
        summary_lines = [
            f"Recording duration: {duration:.1f} s",
            f"LFP sampling rate:  {r['fs_lfp']} Hz",
            f"MUA sampling rate:  {r['fs_mua']} Hz",
            f"1/f exponent:       {r['spectral_exponent'][ch]:.2f}",
            "",
            "Band Powers:",
        ]
        for band, bdata in r["band_powers"][ch].items():
            summary_lines.append(f"  {band:<12} {bdata['fraction'] * 100:.1f}%")
        summary_lines += [
            "",
            f"Spikes detected:    {sp['n_spikes']}",
            f"Mean firing rate:   {sp['mean_rate_hz']:.1f} Hz",
            f"ISI CV:             {sp['isi_cv']:.3f}",
            f"Refract. viol.:     {sp['refract_pct']:.1f}%",
        ]
        ax8.text(
            0.05,
            0.95,
            "\n".join(summary_lines),
            transform=ax8.transAxes,
            va="top",
            fontsize=8,
            fontfamily="monospace",
            bbox=dict(boxstyle="round", facecolor="#f0f4fa", edgecolor="#c0c8d8"),
        )

        plt.savefig(f"figure_10-7-1_pipeline_report_ch{ch + 1}.png", dpi=150, bbox_inches="tight")
        print(f"\nReport saved: pipeline_report_ch{ch + 1}.png")


# -----------------------------------------------------------
# Running the Pipeline on a Simulated Multi-Channel Recording
def generate_test_recording(fs=30000, duration=5, seed=42):
    """
    Generate a two-channel broadband neural recording for pipeline testing.

    Channel 1: Theta-dominant LFP + near neuron (large spikes, 15 Hz)
    Channel 2: Gamma-dominant LFP + far neuron  (small spikes, 8 Hz)
    """
    np.random.seed(seed)
    t = np.arange(0, duration, 1 / fs)

    def make_lfp_background(dominant_freq, dominant_amp, fs_target, t_arr):
        """Build a realistic LFP background at the target sampling rate."""
        t_lfp = np.arange(0, len(t_arr) / fs * fs_target + 1 / fs_target, 1 / fs_target)
        t_lfp = t_lfp[: int(duration * fs_target)]
        sig = (
            dominant_amp * np.sin(2 * np.pi * dominant_freq * t_lfp)
            + 20 * np.sin(2 * np.pi * 2 * t_lfp)
            + 5 * np.sin(2 * np.pi * 25 * t_lfp)
        )
        return sig, t_lfp

    # Build LFP at 1000 Hz then upsample naively for broadband simulation
    lfp1, t_lfp = make_lfp_background(8, 40, 1000, t)  # theta dominant
    lfp2, _ = make_lfp_background(50, 15, 1000, t)  # gamma dominant

    # Upsample LFP to 30 kHz (simple repeat — fine for simulation)
    upsample = fs // 1000
    lfp1_up = np.repeat(lfp1, upsample)[: len(t)]
    lfp2_up = np.repeat(lfp2, upsample)[: len(t)]

    # Spike waveform templates
    def biphasic(fs, amp):
        n = int(2.5 * fs / 1000)
        tw = np.linspace(0, 2.5, n)
        return -amp * np.exp(-((tw - 0.4) ** 2) / (2 * 0.12**2)) + amp * 0.35 * np.exp(
            -((tw - 1.1) ** 2) / (2 * 0.25**2)
        )

    wf1 = biphasic(fs, 250)
    wf2 = biphasic(fs, 80)

    def poisson_spikes(rate, dur, fs_r, refract_ms=2.0, seed=0):
        rng = np.random.default_rng(seed)
        times, now = [], rng.exponential(1 / rate)
        while now < dur:
            times.append(now)
            now += refract_ms / 1000 + rng.exponential(1 / rate)
        return np.array(times)

    st1 = poisson_spikes(15, duration, fs, seed=1)
    st2 = poisson_spikes(8, duration, fs, seed=2)

    noise_std = 25
    ch1 = lfp1_up + noise_std * np.random.randn(len(t))
    ch2 = lfp2_up + noise_std * np.random.randn(len(t))

    for st in st1:
        idx = int(st * fs)
        if idx + len(wf1) < len(ch1):
            ch1[idx : idx + len(wf1)] += wf1

    for st in st2:
        idx = int(st * fs)
        if idx + len(wf2) < len(ch2):
            ch2[idx : idx + len(wf2)] += wf2

    recording = np.vstack([ch1, ch2])
    print(f"Test recording: shape {recording.shape}, " f"duration {duration} s at {fs} Hz")
    print(f"  Ch1: theta-dominant LFP, {len(st1)} spikes (250 µV)")
    print(f"  Ch2: gamma-dominant LFP, {len(st2)} spikes (80 µV)")
    return recording


# Generate the test recording
recording = generate_test_recording(fs=30000, duration=5)

# Instantiate and run the pipeline
pipeline = NeuralPipeline(
    fs_raw=30000,
    fs_lfp=1000,
    notch_freq=60,
    spike_threshold=4.0,
    lfp_band=(1, 300),
    spike_hp_cutoff=300,
)

results = pipeline.run(recording)

# Generate the summary report for channel 1
pipeline.summary_report(channel=0)

# ----------------------------------------
# Extracting Features for Machine Learning


def extract_ml_features(results, channel=0):
    """
    Flatten pipeline results into a fixed-length feature vector
    suitable for machine learning classifiers.

    Feature vector composition:
    - 6 band power fractions (one per canonical band)
    - 1 spectral exponent (1/f slope)
    - 6 time-resolved band power statistics (mean + std per band)
    - 3 spike features (mean rate, ISI CV, refractory violation %)
    Total: 22 features per channel
    """
    features = {}
    ch = channel

    # Band power fractions
    for band, bdata in results["band_powers"][ch].items():
        features[f'bp_frac_{band.replace(" ", "_").lower()}'] = bdata["fraction"]

    # Spectral exponent
    features["spectral_exponent"] = float(results["spectral_exponent"][ch])

    # Time-resolved band power statistics
    for band, ts in results["band_timeseries"][ch].items():
        key = band.replace(" ", "_").lower()
        features[f"bp_ts_mean_{key}"] = float(np.mean(ts))
        features[f"bp_ts_std_{key}"] = float(np.std(ts))

    # Spike features
    sp = results["spikes"][ch]
    features["spike_rate_hz"] = float(sp["mean_rate_hz"])
    features["spike_isi_cv"] = float(sp["isi_cv"])
    features["spike_refract_pct"] = float(sp["refract_pct"])

    return features


# Extract features from both channels
print("ML feature vectors extracted from pipeline output:")
print()
for ch_idx in range(2):
    feats = extract_ml_features(results, channel=ch_idx)
    print(f"Channel {ch_idx + 1} ({['theta-dominant', 'gamma-dominant'][ch_idx]}):")
    for name, val in feats.items():
        print(f"  {name:<40} {val:.4f}")
    print(f"  {'TOTAL FEATURES':<40} {len(feats)}")
    print()
print()
