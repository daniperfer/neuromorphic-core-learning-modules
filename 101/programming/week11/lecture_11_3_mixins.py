"""
Lecture 11.3: Mixins and Multiple Inheritance
"""
import json
import time

import numpy as np
from lecture_11_2_refactored_complete import NeuralPipeline


class LoggingMixin:
    """
    Mixin that adds file-based logging to any NeuralPipeline subclass.
    Assumes the host class has: self._processing_log (list), self.name (str).
    """

    def save_log(self, filepath=None):
        """Write the processing log to a text file."""
        if filepath is None:
            filepath = f"{self.name}_log.txt"
        with open(filepath, "w") as f:
            f.write(f"Processing log for: {self.name}\n")
            f.write("=" * 50 + "\n")
            for i, entry in enumerate(self._processing_log, 1):
                f.write(f"{i:3}. {entry}\n")
        return filepath

    def print_log(self):
        """Print the processing log to stdout in a readable format."""
        print(f"\n--- Processing Log: {self.name} ---")
        for i, entry in enumerate(self._processing_log, 1):
            print(f"  {i:3}. {entry}")
        print(f"--- {len(self._processing_log)} entries total ---\n")


# ------------------------------------------------
# Multiple Inheritance and Class Definition Syntax


class LFPPipeline(LoggingMixin, NeuralPipeline):
    """
    LFP pipeline with file logging capability.
    Inherits core pipeline logic from NeuralPipeline,
    logging utilities from LoggingMixin.
    """

    def __init__(self, sampling_rate=1000, lowcut=1.0, highcut=100.0):
        super().__init__(sampling_rate=sampling_rate, name="LFPPipeline")
        self.lowcut = lowcut
        self.highcut = highcut

    @property
    def modality(self):
        """Returns modality."""
        return "LFP"

    def validate_data(self):
        """Validate data."""
        super().validate_data()
        if self.data.ndim != 1:
            raise ValueError("LFP data must be 1D.")
        self._log("LFP validation passed.")

    def bandpass_filter(self):
        """Applies bandpass."""
        from scipy.signal import butter, filtfilt

        nyq = self.sampling_rate / 2.0
        b, a = butter(4, [self.lowcut / nyq, self.highcut / nyq], btype="band")
        self.processed_data = filtfilt(b, a, self.data)
        self._log(f"Bandpass filtered: {self.lowcut}–{self.highcut} Hz")
        return self

    def run(self):
        """Run pipeline."""
        self.bandpass_filter()
        self._log("LFP pipeline complete.")
        return self


# The pipeline now has both NeuralPipeline methods AND LoggingMixin methods

np.random.seed(42)
t = np.linspace(0, 2, 2000)
np.save("week11_simulated_lfp.npy", np.sin(2 * np.pi * 10 * t) + 0.3 * np.random.randn(2000))

pipeline = LFPPipeline()
pipeline.load_data("week11_simulated_lfp.npy")
pipeline.run()
pipeline.print_log()  # From LoggingMixin
pipeline.save_log()  # From LoggingMixin
print()

# -----------------------------------------------
# Building More Mixins for the Pipeline Framework


class JSONExportMixin:
    """
    Mixin that adds JSON export capability to NeuralPipeline subclasses.
    Assumes the host class has: self.name, self.sampling_rate,
    self._processing_log, self.processed_data (numpy array or None).
    """

    def to_dict(self):
        """Return a dictionary representation of pipeline results."""
        return {
            "name": self.name,
            "modality": getattr(self, "modality", "unknown"),
            "sampling_rate": self.sampling_rate,
            "data_shape": list(self.data.shape) if self.data is not None else None,
            "processed": self.processed_data is not None,
            "log_entries": len(self._processing_log),
            "log": self._processing_log,
        }

    def save_json(self, filepath=None):
        """Export pipeline results and metadata to a JSON file."""
        if filepath is None:
            filepath = f"{self.name}_results.json"
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        self._log(f"Results exported to {filepath}")
        return filepath


class TimingMixin:
    """
    Mixin that adds timing instrumentation to NeuralPipeline subclasses.
    Tracks elapsed time for each run() call.
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def timed_run(self):
        """Run the pipeline and record wall-clock time."""
        start = time.perf_counter()
        self.run()
        elapsed = time.perf_counter() - start
        self._log(f"Pipeline completed in {elapsed:.4f}s")
        self.last_run_time = elapsed
        return self


class SummaryStatsMixin:
    """
    Mixin that adds signal summary statistics to NeuralPipeline subclasses.
    Assumes the host class has: self.processed_data (numpy array),
    self.sampling_rate, self._log.
    """

    def compute_summary(self):
        """Compute and log basic statistics on the processed signal."""
        if self.processed_data is None:
            raise RuntimeError("No processed data. Run the pipeline first.")
        data = self.processed_data
        stats = {
            "mean": float(np.mean(data)),
            "std": float(np.std(data)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "duration_sec": len(data) / self.sampling_rate,
            "n_samples": len(data),
        }
        self._log(
            f"Summary stats — mean: {stats['mean']:.4f}, "
            f"std: {stats['std']:.4f}, "
            f"duration: {stats['duration_sec']:.2f}s"
        )
        self.summary_stats = stats
        return stats


class FullLFPPipeline(
    LoggingMixin, JSONExportMixin, TimingMixin, SummaryStatsMixin, NeuralPipeline
):
    """LFP pipeline with logging, export, timing, and statistics."""

    def __init__(self, sampling_rate=1000, lowcut=1.0, highcut=100.0):
        super().__init__(sampling_rate=sampling_rate, name="FullLFPPipeline")
        self.lowcut = lowcut
        self.highcut = highcut
        self.last_run_time = None
        self.summary_stats = None

    @property
    def modality(self):
        """Returns modality."""
        return "LFP"

    def validate_data(self):
        """Validates data."""
        super().validate_data()
        if self.data.ndim != 1:
            raise ValueError("LFP data must be 1D.")
        self._log("LFP validation passed.")

    def bandpass_filter(self):
        """Applies bandpass filter."""
        from scipy.signal import butter, filtfilt

        nyq = self.sampling_rate / 2.0
        b, a = butter(4, [self.lowcut / nyq, self.highcut / nyq], btype="band")
        self.processed_data = filtfilt(b, a, self.data)
        self._log(f"Bandpass filtered: {self.lowcut}–{self.highcut} Hz")
        return self

    def run(self):
        """Runs pipeline."""
        self.bandpass_filter()
        self.compute_summary()  # From SummaryStatsMixin
        self._log("Full LFP pipeline complete.")
        return self


# Demo
pipeline2 = FullLFPPipeline()
pipeline2.load_data("week11_simulated_lfp.npy")
pipeline2.timed_run()  # From TimingMixin (wraps run())
pipeline2.print_log()  # From LoggingMixin
pipeline2.save_json()  # From JSONExportMixin
print()

# -----------------------------
# Method Resolution Order (MRO)

print(FullLFPPipeline.__mro__)
