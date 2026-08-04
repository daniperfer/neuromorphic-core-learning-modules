import numpy as np
from scipy.ndimage import gaussian_filter1d
from week11.lecture_11_7_NeuralAnalysisFramework import NeuralPipeline


@NeuralPipeline.register("SpikeTrain")
class SpikeTrainPipeline(NeuralPipeline):
    """
    Pipeline for spike train analysis.

    Registered as 'spike_train' in the NeuralAnalysisFramework registry.
    Implements load → preprocess → analyze → report for a single spike train
    stored as a 1D array of timestamps in seconds.

    Params
    ------

    recording_duration : float
        Total recording duration in seconds. Must be provided at instantiation
        because this metadata is not stored in the .npy file itself.
    sigma_ms : float
        Gaussian kernel bandwidth for firing rate smoothing (default: 50 ms).
    bin_width : float
        Histogram bin width in seconds for bin-count rate estimate (default: 0.1 s).
    sampling_rate: float
        Required by NeuralPipeline parent class
    """

    def __init__(self, recording_duration=10.0, sigma_ms=50.0, bin_width=0.1, sampling_rate=1000):
        super().__init__(sampling_rate=sampling_rate, name="SpikeTrainPipeline")
        if recording_duration <= 0:
            raise ValueError(
                f"recording_duration must be positive, got {recording_duration}"
            )  # noqa: E702
        if sigma_ms <= 0:
            raise ValueError(f"sigma_ms must be positive, got {sigma_ms}")  # noqa: E702
        if bin_width <= 0 or bin_width > recording_duration:
            raise ValueError(
                f"bin_width must be in (0, recording_duration], got {bin_width}"
            )  # noqa: E702
        self.recording_duration = recording_duration
        self.sigma_ms = sigma_ms
        self.bin_width = bin_width
        self.data = None
        self.results = {}

    def load_data(self, filepath):
        """Load spike times from a .npy file."""
        self.data = np.load(filepath)
        self.filepath = filepath
        print(f"[SpikeTrainPipeline] Loaded {len(self.data)} spikes from '{filepath}'")
        return self

    def preprocess(self):
        """Validation spike train invariants."""
        if self.data is None:
            raise RuntimeError("Call load() before preprocess().")
        if self.data.ndim != 1:
            raise ValueError(f"Spike train must be 1D, got shape {self.data.shape}.")
        if not np.all(self.data >= 0):
            raise ValueError("All spike times must be non-negative.")
        if len(self.data) > 1 and not np.all(np.diff(self.data) > 0):
            raise ValueError("Spike times must be strictly increasing.")
        if self.data[-1] >= self.recording_duration:
            raise ValueError(
                f"Last spike ({self.data[-1]:.4f} s) is outside the "
                f"recording window ({self.recording_duration} s)."
            )
        print(
            f"[SpikeTrainPipeline] Preprocessing complete — " f"{len(self.data)} spikes validated."
        )
        return self

    def analyze(self):
        """Compute ISI statistics and firing rate estimates."""
        spike_times = self.data
        duration = self.recording_duration
        n_spikes = len(spike_times)
        isis = np.diff(spike_times)

        # --- ISI statistics ---
        cv = isis.std() / isis.mean() if len(isis) > 1 else np.nan

        edges = np.arange(0, duration + 0.5, 0.5)
        counts = np.histogram(spike_times, bins=edges)[0]
        n_full = int(duration / 0.5)
        counts = counts[:n_full]
        fano = counts.var() / counts.mean() if counts.mean() > 0 else np.nan

        # --- Bin-count firing rate ---
        bin_edges = np.arange(0, duration + self.bin_width, self.bin_width)
        bin_counts, _ = np.histogram(spike_times, bins=bin_edges)
        bin_rate = bin_counts / self.bin_width
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        n_full_bins = int(duration / self.bin_width)

        # --- Gaussian kernel firing rate ---
        dt_s = 0.001  # 1 ms resolution
        n_samp = int(duration / dt_s)
        binary = np.zeros(n_samp)
        idx = (spike_times / dt_s).astype(int)
        idx = idx[idx < n_samp]
        binary[idx] = 1.0
        sigma_samp = self.sigma_ms / (dt_s * 1000)
        smoothed = gaussian_filter1d(binary, sigma=sigma_samp)
        kernel_rate = smoothed / dt_s
        kernel_time = np.arange(n_samp) * dt_s

        self.results = {
            # Summary statistics
            "n_spikes": n_spikes,
            "mean_firing_rate": n_spikes / duration,
            "mean_isi_ms": isis.mean() * 1000,
            "median_isi_ms": np.median(isis) * 1000,
            "std_isi_ms": isis.std() * 1000,
            "min_isi_ms": isis.min() * 1000,
            "max_isi_ms": isis.max() * 1000,
            "cv": cv,
            "fano_factor": fano,
            # Time-series estimates (for plotting)
            "isis": isis,
            "bin_centers": bin_centers[:n_full_bins],
            "bin_rate": bin_rate[:n_full_bins],
            "kernel_time": kernel_time,
            "kernel_rate": kernel_rate,
        }

        print(
            f"[SpikeTrainPipeline] Analysis complete — "
            f"rate={n_spikes / duration:.1f} Hz, CV={cv:.3f}, FF={fano:.3f}"
        )
        return self

    def report(self):
        """Print a formatted summary and save the analysis figure."""
        if not self.results:
            raise RuntimeError("Call analyze() before report().")

        r = self.results
        print("\n" + "=" * 45)
        print("  Spike Train Analysis Report")
        print("=" * 45)
        print(f"  File:              {self.filepath}")
        print(f"  Recording:         {self.recording_duration:.1f} s")
        print(f"  Spikes:            {r['n_spikes']}")
        print(f"  Mean firing rate:  {r['mean_firing_rate']:.2f} Hz")
        print(f"  Mean ISI:          {r['mean_isi_ms']:.2f} ms")
        print(f"  ISI std:           {r['std_isi_ms']:.2f} ms")
        print(f"  CV:                {r['cv']:.4f}")
        print(f"  Fano factor:       {r['fano_factor']:.4f}")
        print("=" * 45)

        # Save figure
        self._save_figure()
        return self

    def _save_figure(self):
        """Save a three-panel summary figure."""
        import matplotlib.pyplot as plt

        r = self.results
        fig, axes = plt.subplots(3, 1, figsize=(13, 9))

        # Panel 1: raster
        axes[0].eventplot(self.data, lineoffsets=0, linelengths=0.8, color="black", linewidths=0.7)
        axes[0].set_xlim(0, self.recording_duration)
        axes[0].set_yticks([])
        axes[0].set_title("Spike Raster")
        axes[0].set_ylabel("Neuron")

        # Panel 2: ISI histogram
        axes[1].hist(r["isis"] * 1000, bins=40, color="steelblue", edgecolor="white", linewidth=0.5)
        axes[1].set_xlabel("ISI (ms)")
        axes[1].set_ylabel("Count")
        axes[1].set_title(
            f'ISI Distribution | CV = {r["cv"]:.3f} | ' f'Fano = {r["fano_factor"]:.3f}'
        )

        # Panel 3: firing rate
        axes[2].bar(
            r["bin_centers"],
            r["bin_rate"],
            width=self.bin_width * 0.9,
            color="steelblue",
            alpha=0.5,
            label=f"Histogram ({self.bin_width * 1000:.0f} ms bins)",
        )
        axes[2].plot(
            r["kernel_time"],
            r["kernel_rate"],
            color="coral",
            linewidth=1.8,
            label=f"Kernel (σ={self.sigma_ms:.0f} ms)",
        )
        axes[2].axhline(
            r["mean_firing_rate"], color="black", linestyle="--", linewidth=1.0, label="Mean rate"
        )
        axes[2].set_xlabel("Time (s)")
        axes[2].set_ylabel("Firing Rate (Hz)")
        axes[2].set_title("Firing Rate Estimate")
        axes[2].legend()

        plt.suptitle("SpikeTrainPipeline — Analysis Summary", fontsize=13, y=1.01)
        plt.tight_layout()
        plt.savefig("figure_12-4_spike_train_report.png", dpi=150, bbox_inches="tight")
        print("[SpikeTrainPipeline] Figure saved: figure_12-4_spike_train_report.png")

    @property
    def modality(self) -> str:
        """Returns modality."""
        return "SpikeTrain"

    def validate_data(self):
        """Data validator."""
        super().validate_data()
        self.preprocess()
        self._log("SpikeTrain validation passed.")

    def run(self) -> "SpikeTrainPipeline":
        """Runs pipeline."""
        self.analyze()
        self.processed_data = self.data
        self._log("SpikeTrain run complete.")
        return self
