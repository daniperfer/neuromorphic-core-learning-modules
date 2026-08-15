"""
Lecture 11.7: Designing a Reusable Neuroscience Analysis Framework
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import numpy as np

# ─────────────────────────────────────────────
# COMPONENT LAYER
# ─────────────────────────────────────────────


class BandpassFilter:
    """Butterworth bandpass filter component."""

    def __init__(self, lowcut: float, highcut: float, order: int = 4):
        self.lowcut = lowcut
        self.highcut = highcut
        self.order = order

    def apply(self, data: np.ndarray, sampling_rate: float) -> np.ndarray:
        """Run."""
        from scipy.signal import butter, filtfilt

        nyq = sampling_rate / 2.0
        b, a = butter(self.order, [self.lowcut / nyq, self.highcut / nyq], btype="band")
        return filtfilt(b, a, data)

    def describe(self) -> dict:
        """Describe."""
        return {
            "type": "BandpassFilter",
            "lowcut": self.lowcut,
            "highcut": self.highcut,
            "order": self.order,
        }

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"BandpassFilter({self.lowcut}–{self.highcut} Hz, order={self.order})"


class NotchFilter:
    """IIR notch filter for removing power line interference."""

    def __init__(self, notch_freq: float = 60.0, Q: float = 30.0):
        self.notch_freq = notch_freq
        self.Q = Q

    def apply(self, data: np.ndarray, sampling_rate: float) -> np.ndarray:
        """Run."""
        from scipy.signal import filtfilt, iirnotch

        b, a = iirnotch(self.notch_freq, self.Q, fs=sampling_rate)
        return filtfilt(b, a, data)

    def describe(self) -> dict:
        """Describe."""
        return {"type": "NotchFilter", "notch_freq": self.notch_freq, "Q": self.Q}

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"NotchFilter({self.notch_freq} Hz, Q={self.Q})"


class BaselineCorrection:
    """Subtracts mean of an initial baseline window."""

    def __init__(self, baseline_window_sec: float = 0.2):
        self.baseline_window_sec = baseline_window_sec

    def apply(self, data: np.ndarray, sampling_rate: float) -> np.ndarray:
        """Run."""
        n_baseline = int(self.baseline_window_sec * sampling_rate)
        return data - data[:n_baseline].mean()

    def describe(self) -> dict:
        """Describe."""
        return {"type": "BaselineCorrection", "window_sec": self.baseline_window_sec}

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"BaselineCorrection(window={self.baseline_window_sec}s)"


# ─────────────────────────────────────────────
# BASE LAYER
# ─────────────────────────────────────────────


class NeuralPipeline(ABC):
    """
    Abstract base class for all neural signal processing pipelines.

    Required in subclasses:
        modality    (abstract property)
        validate_data()  (abstract method; call super() for base checks)
        run()            (abstract method)
    """

    _registry: Dict[str, type] = {}

    def __init__(self, sampling_rate: float = 1000, name: str = "NeuralPipeline"):
        self.sampling_rate = sampling_rate
        self.name = name
        self.data: Optional[np.ndarray] = None
        self.processed_data: Optional[np.ndarray] = None
        self._processing_log: List[str] = []
        self.summary_stats: dict[str, float | int] | None = None

    # ── Class methods ──────────────────────────────────

    @classmethod
    def register(cls, modality_name: str):
        """Register."""

        def decorator(subclass):
            cls._registry[modality_name] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, modality_name: str, **kwargs) -> "NeuralPipeline":
        """Creates Pipeline."""
        if modality_name not in cls._registry:
            raise ValueError(
                f"Unknown modality {modality_name!r}. " f"Registered: {list(cls._registry)}"
            )
        return cls._registry[modality_name](**kwargs)

    # ── Static methods ─────────────────────────────────

    @staticmethod
    def seconds_to_samples(seconds: float, sampling_rate: float) -> int:
        """Seconds converter."""
        return int(round(seconds * sampling_rate))

    @staticmethod
    def validate_frequency_band(lowcut: float, highcut: float, fs: float) -> bool:
        """Frequency validator."""
        nyq = fs / 2.0
        if not (0 < lowcut < highcut < nyq):
            raise ValueError(f"Invalid band {lowcut}–{highcut} Hz for fs={fs} Hz (Nyquist={nyq})")
        return True

    # ── Properties ─────────────────────────────────────

    @property
    def nyquist(self) -> float:
        """Nyquist frequency."""
        return self.sampling_rate / 2.0

    @property
    def duration(self) -> Optional[float]:
        """Data duration."""
        return len(self.data) / self.sampling_rate if self.data is not None else None

    @property
    def n_samples(self) -> int:
        """Data length."""
        return len(self.data) if self.data is not None else 0

    # ── Dunder methods ─────────────────────────────────

    def __len__(self):
        """Data length."""
        return self.n_samples

    def __bool__(self):
        """Check if data loaded."""
        return self.data is not None

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"modality={self.modality!r}, "
            f"fs={self.sampling_rate}, "
            f"samples={self.n_samples})"
        )

    def __eq__(self, other):
        """Comparator."""
        if not isinstance(other, NeuralPipeline):
            return NotImplemented
        return (
            self.modality == other.modality
            and self.sampling_rate == other.sampling_rate
            and self.n_samples == other.n_samples
        )

    def __hash__(self):
        return hash((self.modality, self.sampling_rate, self.n_samples))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log("Context exit." if exc_type is None else f"Context exit on {exc_type.__name__}.")
        return False

    # ── Concrete methods ───────────────────────────────

    def load_data(self, filepath: str) -> "NeuralPipeline":
        """Loads data."""
        self.data = np.load(filepath)
        self._log(f"Loaded: {filepath} — {self.n_samples} samples, {self.duration:.2f}s")
        self.validate_data()
        return self

    def _log(self, message: str):
        """Log message."""
        self._processing_log.append(message)

    def get_log(self) -> List[str]:
        """Get registered logs"""
        return self._processing_log.copy()

    def to_dict(self) -> dict:
        """Dictionary converter."""
        return {
            "name": self.name,
            "modality": self.modality,
            "sampling_rate": self.sampling_rate,
            "n_samples": self.n_samples,
            "duration_sec": self.duration,
            "processed": self.processed_data is not None,
            "summary_stats": self.summary_stats,
            "log": self._processing_log,
        }

    # ── Abstract interface ─────────────────────────────

    @property
    @abstractmethod
    def modality(self) -> str:
        """Returns modality."""
        ...

    @abstractmethod
    def validate_data(self):
        """Data validator."""
        if self.data is None:
            raise ValueError("No data loaded.")
        if not isinstance(self.data, np.ndarray):
            raise TypeError("Data must be a numpy array.")
        self._log("Base validation passed.")

    @abstractmethod
    def run(self) -> "NeuralPipeline":
        """Run pipeline."""
        ...


# ─────────────────────────────────────────────
# MIXIN LAYER
# ─────────────────────────────────────────────


class LoggingMixin:
    """
    Adds file-based and print logging to any NeuralPipeline subclass.
    Assumes the host class has: self._processing_log (list), self.name (str).
    """

    name: str
    _processing_log: list[str]

    def print_log(self):
        """Prints logs"""
        print(f"\n--- Log: {self.name} ---")
        for i, entry in enumerate(self._processing_log, 1):
            print(f"  {i:3}. {entry}")
        print(f"--- {len(self._processing_log)} entries ---\n")

    def save_log(self, filepath: Optional[str] = None) -> str:
        """Saves logs."""
        if filepath is None:
            filepath = f"{self.name}_log.txt"
        with open(filepath, "w") as f:
            f.write(f"Log: {self.name}\n" + "=" * 50 + "\n")
            for i, entry in enumerate(self._processing_log, 1):
                f.write(f"{i:3}. {entry}\n")
        return filepath


class SummaryStatsMixin:
    """Adds summary statistics computation to any NeuralPipeline subclass."""

    processed_data: Optional[np.ndarray]
    sampling_rate: float
    summary_stats: dict[str, float | int] | None = None

    def _log(self, message: str) -> None:
        ...

    def compute_summary(self) -> dict:
        """Summarizes."""
        if self.processed_data is None:
            raise RuntimeError("Run pipeline first.")
        d = self.processed_data
        stats: dict[str, float | int] = {
            "mean": float(np.mean(d)),
            "std": float(np.std(d)),
            "min": float(np.min(d)),
            "max": float(np.max(d)),
            "rms": float(np.sqrt(np.mean(d**2))),
            "duration_sec": len(d) / self.sampling_rate,
            "n_samples": len(d),
        }
        self._log(
            f"Summary — mean={stats['mean']:.4f}, "
            f"std={stats['std']:.4f}, "
            f"rms={stats['rms']:.4f}"
        )
        self.summary_stats = stats
        return stats


# ─────────────────────────────────────────────
# PIPELINE LAYER
# ─────────────────────────────────────────────


@NeuralPipeline.register("LFP")
class LFPPipeline(LoggingMixin, SummaryStatsMixin, NeuralPipeline):
    """Local field potential pipeline."""

    def __init__(
        self,
        sampling_rate: float = 1000,
        lowcut: float = 1.0,
        highcut: float = 100.0,
        baseline_correction: Optional[BaselineCorrection] = None,
    ):
        super().__init__(sampling_rate=sampling_rate, name="LFPPipeline")
        NeuralPipeline.validate_frequency_band(lowcut, highcut, sampling_rate)
        self._filter = BandpassFilter(lowcut, highcut)
        self._baseline = baseline_correction

    @property
    def modality(self) -> str:
        """Returns modality."""
        return "LFP"

    @classmethod
    def for_band(cls, band: str, sampling_rate: float = 1000) -> "LFPPipeline":
        """Creator."""
        bands = {
            "delta": (0.5, 4.0),
            "theta": (4.0, 8.0),
            "alpha": (8.0, 13.0),
            "beta": (13.0, 30.0),
            "gamma": (30.0, 80.0),
            "high_gamma": (80.0, 150.0),
        }
        if band not in bands:
            raise ValueError(f"Unknown band {band!r}. Available: {list(bands)}")
        low, high = bands[band]
        instance = cls(sampling_rate=sampling_rate, lowcut=low, highcut=high)
        instance._log(f"Created via for_band('{band}'): {low}–{high} Hz")
        return instance

    def validate_data(self):
        """Data validator."""
        super().validate_data()
        if self.data.ndim != 1:
            raise ValueError(f"LFP data must be 1D, got shape {self.data.shape}.")
        self._log("LFP validation passed.")

    def run(self) -> "LFPPipeline":
        """Run pipeline."""
        self.processed_data = self._filter.apply(self.data, self.sampling_rate)
        self._log(f"Filtered: {self._filter}")
        if self._baseline is not None:
            self.processed_data = self._baseline.apply(self.processed_data, self.sampling_rate)
            self._log(f"Baseline corrected: {self._baseline}")
        self.compute_summary()
        self._log("LFP run complete.")
        return self


@NeuralPipeline.register("EEG")
class EEGPipeline(LoggingMixin, SummaryStatsMixin, NeuralPipeline):
    """Scalp EEG pipeline with notch + bandpass filtering."""

    def __init__(
        self,
        sampling_rate: float = 256,
        lowcut: float = 0.5,
        highcut: float = 50.0,
        notch_freq: float = 60.0,
    ):
        super().__init__(sampling_rate=sampling_rate, name="EEGPipeline")
        self._notch = NotchFilter(notch_freq)
        self._filter = BandpassFilter(lowcut, highcut)

    @property
    def modality(self) -> str:
        """Returns modality."""
        return "EEG"

    def validate_data(self):
        """Data validator."""
        super().validate_data()
        if self.data.ndim != 1:
            raise ValueError("Single-channel EEG expected. Pass one channel at a time.")
        self._log("EEG validation passed.")

    def run(self) -> "EEGPipeline":
        """Runs pipeline."""
        self.processed_data = self._notch.apply(self.data, self.sampling_rate)
        self._log(f"Notch filtered: {self._notch}")
        self.processed_data = self._filter.apply(self.processed_data, self.sampling_rate)
        self._log(f"Bandpass filtered: {self._filter}")
        self.compute_summary()
        self._log("EEG run complete.")
        return self


# ─────────────────────────────────────────────
# FRAMEWORK LAYER
# ─────────────────────────────────────────────


class NeuralAnalysisFramework:
    """
    High-level orchestrator for running and comparing multiple pipelines.
    Supports batch processing, result comparison, and JSON serialization.
    """

    def __init__(self, name: str = "NeuralAnalysisFramework"):
        self.name = name
        self._pipelines: Dict[str, NeuralPipeline] = {}
        self._run_times: Dict[str, float] = {}

    def add_pipeline(self, pipeline_id: str, pipeline: NeuralPipeline) -> "NeuralAnalysisFramework":
        """Register a pipeline under a string ID."""
        if not isinstance(pipeline, NeuralPipeline):
            raise TypeError(f"Expected NeuralPipeline, got {type(pipeline).__name__}")
        self._pipelines[pipeline_id] = pipeline
        return self

    def __len__(self):
        """Returns number of pipelines."""
        return len(self._pipelines)

    def __iter__(self):
        return iter(self._pipelines.values())

    def __getitem__(self, pipeline_id: str) -> NeuralPipeline:
        return self._pipelines[pipeline_id]

    def __repr__(self):
        ids = list(self._pipelines.keys())
        return f"NeuralAnalysisFramework(name={self.name!r}, pipelines={ids})"

    def load_all(self, filepath_map: Dict[str, str]) -> "NeuralAnalysisFramework":
        """Load data for each pipeline. filepath_map: {pipeline_id: filepath}"""
        for pid, fpath in filepath_map.items():
            if pid not in self._pipelines:
                raise KeyError(f"Pipeline ID {pid!r} not registered.")
            self._pipelines[pid].load_data(fpath)
        return self

    def run_all(self) -> "NeuralAnalysisFramework":
        """Run every registered pipeline, recording wall-clock time."""
        for pid, pipeline in self._pipelines.items():
            start = time.perf_counter()
            pipeline.run()
            elapsed = time.perf_counter() - start
            self._run_times[pid] = elapsed
        return self

    def compare(self) -> dict:
        """
        Compare summary statistics across all processed pipelines.
        Returns a dict mapping pipeline_id → stats dict.
        """
        results: Dict[str, Dict] = {}
        for pid, pipeline in self._pipelines.items():
            if pipeline.processed_data is None:
                results[pid] = {"status": "not processed"}
            else:
                entry = {
                    "modality": pipeline.modality,
                    "duration_sec": pipeline.duration,
                    "n_samples": pipeline.n_samples,
                    "run_time_sec": self._run_times.get(pid),
                }
                if pipeline.summary_stats:
                    entry.update(pipeline.summary_stats)
                results[pid] = entry
        return results

    def save_results(self, filepath: str = "framework_results.json") -> str:
        """Serialize all pipeline results and comparison to JSON."""
        output = {
            "framework": self.name,
            "n_pipelines": len(self),
            "comparison": self.compare(),
            "pipelines": {pid: p.to_dict() for pid, p in self._pipelines.items()},
        }
        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)
        return filepath

    def print_summary(self):
        """Print a formatted comparison table to stdout."""
        comparison = self.compare()
        print(f"\n{'=' * 60}")
        print(f"  {self.name} — {len(self)} pipeline(s)")
        print(f"{'=' * 60}")
        for pid, stats in comparison.items():
            print(f"\n  [{pid}]")
            for k, v in stats.items():
                if isinstance(v, float):
                    print(f"    {k:<20} {v:.4f}")
                else:
                    print(f"    {k:<20} {v}")
        print(f"{'=' * 60}\n")


# ----------------------------
# Using the Complete Framework

if __name__ == "__main__":
    # Generate synthetic data for testing
    np.random.seed(42)
    fs_lfp = 1000
    t_lfp = np.linspace(0, 2, 2 * fs_lfp)
    lfp_signal = (
        np.sin(2 * np.pi * 10 * t_lfp)  # 10 Hz oscillation
        + 0.3 * np.sin(2 * np.pi * 40 * t_lfp)  # 40 Hz gamma
        + 0.5 * np.random.randn(len(t_lfp))
    )
    np.save("week11_lect07_simulated_lfp.npy", lfp_signal)

    fs_eeg = 256
    t_eeg = np.linspace(0, 4, 4 * fs_eeg)
    eeg_signal = (
        np.sin(2 * np.pi * 10 * t_eeg)
        + 0.2 * np.sin(2 * np.pi * 60 * t_eeg)  # 60 Hz artifact
        + 0.4 * np.random.randn(len(t_eeg))
    )
    np.save("week11_lect07_simulated_eeg.npy", eeg_signal)

    # Build pipelines using the registry
    lfp = NeuralPipeline.create("LFP", sampling_rate=1000, lowcut=1.0, highcut=100.0)
    gamma_lfp = LFPPipeline.for_band("gamma", sampling_rate=1000)
    eeg = NeuralPipeline.create("EEG", sampling_rate=256, notch_freq=60.0)

    # Assemble into a framework
    framework = NeuralAnalysisFramework(name="Week11_Demo")
    (
        framework.add_pipeline("lfp_broadband", lfp)
        .add_pipeline("lfp_gamma", gamma_lfp)
        .add_pipeline("eeg_ch1", eeg)
    )

    # Load and run everything
    framework.load_all(
        {
            "lfp_broadband": "week11_lect07_simulated_lfp.npy",
            "lfp_gamma": "week11_lect07_simulated_lfp.npy",
            "eeg_ch1": "week11_lect07_simulated_eeg.npy",
        }
    )
    framework.run_all()

    # Print and save results
    framework.print_summary()
    framework.save_results("week11_framework_results.json")

    # Demonstrate dunder methods on the framework
    print(f"Number of pipelines: {len(framework)}")
    for p in framework:
        print(f"  {repr(p)}")

    # Demonstrate context manager
    with LFPPipeline.for_band("theta") as theta:
        theta.load_data("week11_lect07_simulated_lfp.npy")
        theta.run()
        theta.print_log()
print()
