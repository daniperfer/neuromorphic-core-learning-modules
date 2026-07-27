"""
Lecture 11.2: Abstract Base Classes and Interfaces
"""

# ---------------------------------------
# Introducing abc.ABC and @abstractmethod

from abc import ABC, abstractmethod

import numpy as np
from scipy.signal import butter, filtfilt


class NeuralPipeline(ABC):
    """
    Abstract base class for neural signal processing pipelines.
    Cannot be instantiated directly — must be subclassed.
    Subclasses MUST implement: run(), validate_data()
    """

    def __init__(self, sampling_rate=1000, name="NeuralPipeline"):
        self.sampling_rate = sampling_rate
        self.name = name
        self.data = None
        self.processed_data = None
        self._processing_log = []

    def load_data(self, filepath):
        """Load data from disk, then call validate_data()."""
        self.data = np.load(filepath)
        self._log(f"Loaded data from {filepath}: shape {self.data.shape}")
        self.validate_data()  # Calls the subclass's implementation
        return self

    def _log(self, message):
        """Adds a new message to the log"""
        self._processing_log.append(message)

    def get_log(self):
        """Get logs"""
        return self._processing_log.copy()

    @abstractmethod
    def validate_data(self):
        """
        Validate that loaded data meets the requirements of this pipeline type.
        Subclasses must implement this method.
        Base validation all pipelines share: check that data is not None
        and is a numpy array.
        Subclasses MUST call super().validate_data() and then add their own checks.
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        if not isinstance(self.data, np.ndarray):
            raise TypeError(f"Expected numpy array, got {type(self.data).__name__}")
        self._log("Base validation passed: data is a non-None numpy array.")

    @abstractmethod
    def run(self):
        """
        Execute the full processing pipeline.
        Subclasses must implement this method.
        """

    @property
    @abstractmethod
    def modality(self):
        """
        Return a string describing the recording modality.
        E.g., 'LFP', 'EEG', 'spike_train', 'calcium_imaging'.
        """


# This will raise a TypeError immediately — no runtime surprise
# pipeline = NeuralPipeline(sampling_rate=1000)
# TypeError: Can't instantiate abstract class NeuralPipeline
# with abstract methods run, validate_data

# -----------------------------------
# Implementing the Abstract Interface


class LFPPipeline(NeuralPipeline):
    """Pipeline for local field potential recordings."""

    def __init__(self, sampling_rate=1000, lowcut=1.0, highcut=100.0):
        super().__init__(sampling_rate=sampling_rate, name="LFPPipeline")
        self.lowcut = lowcut
        self.highcut = highcut

    def validate_data(self):
        """Implement the abstract method: validate LFP-specific requirements."""
        super().validate_data()  # Runs the shared checks from the base class (Universal checks)
        # Then add LFP-specific checks for this subclass
        if self.data.ndim != 1:
            raise ValueError(
                f"LFP data must be 1D. Got shape {self.data.shape}. " "Pass a single channel."
            )
        duration_sec = len(self.data) / self.sampling_rate
        if duration_sec < 1.0:
            raise ValueError(f"Recording too short: {duration_sec:.2f}s. Minimum 1s required.")
        self._log(f"LFP validation passed: {duration_sec:.1f}s at {self.sampling_rate} Hz")

    def bandpass_filter(self):
        """Appy bandpass filter"""
        nyq = self.sampling_rate / 2.0
        b, a = butter(4, [self.lowcut / nyq, self.highcut / nyq], btype="band")
        self.processed_data = filtfilt(b, a, self.data)
        self._log(f"Bandpass filtered: {self.lowcut}–{self.highcut} Hz")
        return self

    def run(self):
        """Implement the abstract method: full LFP processing pipeline."""
        self.bandpass_filter()
        self._log("LFP pipeline complete.")
        return self

    @property
    def modality(self):
        """Return modality of subclass"""
        return "LFP"


class IncompletePipeline(NeuralPipeline):
    """A pipeline that only implements run() but forgets validate_data()."""

    def run(self):
        """Implement the abstract method."""
        self._log("Running.")


# This raises TypeError at instantiation, not at runtime
# p = IncompletePipeline()
# TypeError: Can't instantiate abstract class IncompletePipeline
# with abstract method validate_data


class EEGPipeline(NeuralPipeline):
    """Example"""

    def __init__(self, sampling_rate=1000):
        super().__init__(sampling_rate=sampling_rate, name="EEGPipeline")

    def validate_data(self):
        """Implement the abstract method: validate LFP-specific requirements."""
        super().validate_data()

    def run(self):
        """Implement the abstract method: full EEG processing pipeline."""
        self._log("EEG pipeline complete.")
        return self

    @property
    def modality(self):
        """Return modality of subclass"""
        return "EEG"


pipelines = [LFPPipeline(), EEGPipeline()]
for p in pipelines:
    print(f"{p.name}: modality = {p.modality}")
print()
