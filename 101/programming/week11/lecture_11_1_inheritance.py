"""
Lecture 11.1: Inheritance and Subclasses — Extending the NeuralPipeline
"""

# The NeuralPipeline base class from Week 10 (simplified for clarity)
import numpy as np


class NeuralPipeline:
    """Base class for neural signal processing pipelines."""

    def __init__(self, sampling_rate=1000, name="NeuralPipeline"):
        self.sampling_rate = sampling_rate
        self.name = name
        self.data = None
        self.processed_data = None
        self._processing_log = []

    def load_data(self, filepath):
        """Load neural data from a .npy file."""
        self.data = np.load(filepath)
        self._log(f"Loaded data: shape {self.data.shape}")
        return self

    def _log(self, message):
        """Internal logging method."""
        self._processing_log.append(message)

    def get_log(self):
        """Get logs."""
        return self._processing_log.copy()

    def run(self):
        """Run the full pipeline. Subclasses override this."""
        raise NotImplementedError("Subclasses must implement run()")


# -------------------
# Defining a Subclass


class LFPPipeline(NeuralPipeline):
    """Pipeline specialized for local field potential recordings."""

    def __init__(self, sampling_rate=1000, lowcut=1.0, highcut=100.0, name="LFPPipeline"):
        # Call the parent __init__ first
        super().__init__(sampling_rate=sampling_rate, name=name)
        # Then add subclass-specific attributes
        self.lowcut = lowcut
        self.highcut = highcut

    def bandpass_filter(self):
        """Apply a bandpass filter appropriate for LFP signals."""
        from scipy.signal import butter, filtfilt

        nyq = self.sampling_rate / 2.0
        low = self.lowcut / nyq
        high = self.highcut / nyq
        b, a = butter(4, [low, high], btype="band")
        self.processed_data = filtfilt(b, a, self.data)
        self._log(f"Bandpass filter applied: {self.lowcut}–{self.highcut} Hz")
        return self

    def run(self):
        """Run the LFP-specific pipeline."""
        self.bandpass_filter()
        self._log("LFP pipeline complete.")
        return self

    def load_data(self, filepath):
        """Load data and validate that it looks like an LFP recording."""
        super().load_data(filepath)  # Run the parent's loading logic first
        # Now add LFP-specific validation
        if self.data.ndim != 1:
            raise ValueError(
                f"LFP data should be 1D, but got shape {self.data.shape}. "
                "If you have multi-channel data, pass a single channel."
            )
        if len(self.data) < self.sampling_rate:
            raise ValueError("Recording is less than 1 second. Too short to analyze.")
        self._log("LFP data validation passed.")
        return self


# Using the subclass
pipeline = LFPPipeline(sampling_rate=1000, lowcut=1.0, highcut=100.0)
pipeline.load_data("../week10/week10_simulated_lfp.npy")  # Inherited from NeuralPipeline
pipeline.run()  # Overridden in LFPPipeline
print(pipeline.get_log())  # Inherited from NeuralPipeline
print()

# --------------------------------------------------
# Method Overriding and Calling the Parent’s Version

# --------------------------
# Building a Second Subclass


class EEGPipeline(NeuralPipeline):
    """Pipeline specialized for scalp EEG recordings."""

    # EEG typically sampled at 256–512 Hz; much lower frequency range of interest
    def __init__(
        self, sampling_rate=256, lowcut=0.5, highcut=50.0, notch_freq=60.0, name="EEGPipeline"
    ):
        super().__init__(sampling_rate=sampling_rate, name=name)
        self.lowcut = lowcut
        self.highcut = highcut
        self.notch_freq = notch_freq  # Remove power line noise

    def apply_notch_filter(self):
        """Remove 60 Hz power line interference from EEG signal."""
        from scipy.signal import filtfilt, iirnotch

        b, a = iirnotch(self.notch_freq, Q=30, fs=self.sampling_rate)
        self.processed_data = filtfilt(b, a, self.data)
        self._log(f"Notch filter applied at {self.notch_freq} Hz")
        return self

    def run(self):
        """Run EEG-specific preprocessing."""
        self.apply_notch_filter()
        self._log("EEG pipeline complete.")
        return self


def process_recording(pipeline, filepath):
    """Process any NeuralPipeline without knowing the specific type."""
    pipeline.load_data(filepath)
    pipeline.run()
    return pipeline.get_log()


# Both pipelines work through the same interface
lfp = LFPPipeline(sampling_rate=1000)
eeg = EEGPipeline(sampling_rate=256)

# This function doesn't need to know or care which type it receives
log_lfp = process_recording(lfp, "../week10/week10_simulated_lfp.npy")
print()

# -----------------------------
# isinstance() and issubclass()

# isinstance checks if an object is an instance of a class OR its subclasses
print(isinstance(lfp, LFPPipeline))  # True
print(isinstance(lfp, NeuralPipeline))  # True — LFPPipeline IS a NeuralPipeline
print(isinstance(lfp, EEGPipeline))  # False

# issubclass checks the class hierarchy itself (not an instance)
print(issubclass(LFPPipeline, NeuralPipeline))  # True
print(issubclass(EEGPipeline, LFPPipeline))  # False — they are siblings


def summarize_pipeline(pipeline):
    """Practical use: graceful handling in a shared function."""
    if not isinstance(pipeline, NeuralPipeline):
        raise TypeError("Expected a NeuralPipeline instance.")
    print(f"Pipeline: {pipeline.name}")
    print(f"Sampling rate: {pipeline.sampling_rate} Hz")
    if isinstance(pipeline, LFPPipeline):
        print(f"LFP band: {pipeline.lowcut}–{pipeline.highcut} Hz")
    elif isinstance(pipeline, EEGPipeline):
        print(f"EEG band: {pipeline.lowcut}–{pipeline.highcut} Hz")
        print(f"Notch frequency: {pipeline.notch_freq} Hz")
