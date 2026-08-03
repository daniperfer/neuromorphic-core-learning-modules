from abc import ABC, abstractmethod

import numpy as np


class NeuralPipeline(ABC):
    """NeuralPipeline"""

    _registry: dict[str, str] = {}

    def __init__(self, sampling_rate=1000, name="NeuralPipeline"):
        self.sampling_rate = sampling_rate
        self.name = name
        self.data = None
        self.processed_data = None
        self._processing_log = []
        self.__version = "1.0"  # Private: mangled to _NeuralPipeline__version

    def get_version(self):
        """Returns version."""
        return self.__version  # Access via public method

    @property
    def nyquist(self):
        """Returns Nyquist freq."""
        return self.sampling_rate / 2.0

    @property
    def duration(self):
        """Reeturns duration"""
        return len(self.data) / self.sampling_rate if self.data is not None else None

    @property
    def n_samples(self):
        """Return len samples"""
        return len(self.data) if self.data is not None else 0

    @staticmethod
    def seconds_to_samples(seconds, sampling_rate):
        """Seconds convert."""
        return int(round(seconds * sampling_rate))

    @staticmethod
    def validate_frequency_band(lowcut, highcut, sampling_rate):
        """Validate freqs."""
        nyq = sampling_rate / 2.0
        if not (0 < lowcut < highcut < nyq):
            raise ValueError(
                f"Invalid band: {lowcut}–{highcut} Hz for fs={sampling_rate} Hz "
                f"(Nyquist={nyq} Hz)"
            )
        return True

    @classmethod
    def register(cls, modality_name):
        """Decorator to register a subclass under a modality name."""

        def decorator(subclass):
            cls._registry[modality_name] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, modality_name, **kwargs):
        """Factory: create the right pipeline type from a modality string."""
        if modality_name not in cls._registry:
            raise ValueError(f"Unknown modality: {modality_name!r}")
        return cls._registry[modality_name](**kwargs)

    def load_data(self, filepath):
        """Loads data."""
        self.data = np.load(filepath)
        self._log(f"Loaded: {filepath} — {self.n_samples} samples, {self.duration:.2f}s")
        self.validate_data()
        return self

    def _log(self, message):
        """Register log"""
        self._processing_log.append(message)

    def get_log(self):
        """Returns logs."""
        return self._processing_log.copy()

    @property
    @abstractmethod
    def modality(self):
        """Returns modality."""
        ...

    @abstractmethod
    def validate_data(self):
        """Data validation"""
        if self.data is None:
            raise ValueError("No data loaded.")
        self._log("Base validation passed.")

    @abstractmethod
    def run(self):
        """Runs pipeline."""
        ...

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return (
            f"{self.__class__.__name__}("
            f"modality={self.modality!r}, "
            f"fs={self.sampling_rate}, "
            f"duration={self.duration}s)"
        )

    def __str__(self):
        """Readable summary for print() and str()."""
        status = "processed" if self.processed_data is not None else "raw"
        data_info = (
            f"{self.n_samples} samples ({self.duration:.2f}s)"
            if self.data is not None
            else "no data loaded"
        )
        return (
            f"[{self.__class__.__name__}] "
            f"modality={self.modality}, "
            f"fs={self.sampling_rate} Hz, "
            f"{data_info}, "
            f"status={status}"
        )

    def __len__(self):
        """Return the number of samples in the loaded recording."""
        return self.n_samples  # Already defined as a @property

    def __bool__(self):
        """A pipeline is truthy if it has data loaded."""
        return self.data is not None

    def __eq__(self, other):
        """Two pipelines are equal if they have the same configuration and data shape."""
        if not isinstance(other, NeuralPipeline):
            return NotImplemented
        return (
            self.modality == other.modality
            and self.sampling_rate == other.sampling_rate
            and self.n_samples == other.n_samples
        )

    def __hash__(self):
        """Required when __eq__ is defined, to keep objects usable as dict keys."""
        return hash((self.modality, self.sampling_rate, self.n_samples))

    def __enter__(self):
        """Enable use as a context manager."""
        self._log("Pipeline context entered.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up on context exit; log any exception."""
        if exc_type is not None:
            self._log(f"Pipeline exited with exception: {exc_type.__name__}: {exc_val}")
        else:
            self._log("Pipeline context exited cleanly.")
        # Return False to propagate exceptions (don't suppress them)
        return False
