from abc import ABC, abstractmethod

import numpy as np


class NeuralPipeline(ABC):
    """
    Abstract base class for all neural signal processing pipelines.

    Subclasses must implement:
        - validate_data(): modality-specific data validation
        - run(): the full processing pipeline
        - modality (property): string identifier for the recording type

    Subclasses are encouraged to call super() in validate_data() to
    inherit shared base validation.
    """

    def __init__(self, sampling_rate=1000, name="NeuralPipeline"):
        self.sampling_rate = sampling_rate
        self.name = name
        self.data = None
        self.processed_data = None
        self._processing_log = []

    def load_data(self, filepath):
        """Load a .npy file and immediately validate it."""
        self.data = np.load(filepath)
        self._log(f"Loaded: {filepath} — shape {self.data.shape}")
        self.validate_data()
        return self

    def _log(self, message):
        """Adds a new message to the log"""
        self._processing_log.append(message)

    def get_log(self):
        """Get logs"""
        return self._processing_log.copy()

    @property
    @abstractmethod
    def modality(self):
        """Recording modality string. Must be defined by subclass."""

    @abstractmethod
    def validate_data(self):
        """
        Validate loaded data against modality-specific requirements.
        Subclasses should call super().validate_data() first.
        """
        if self.data is None:
            raise ValueError("No data loaded.")
        if not isinstance(self.data, np.ndarray):
            raise TypeError("Data must be a numpy array.")
        self._log("Base validation passed.")

    @abstractmethod
    def run(self):
        """Execute the full processing pipeline."""

    def __repr__(self):
        status = "loaded" if self.data is not None else "no data"
        return (
            f"{self.__class__.__name__}("
            f"modality={self.modality!r}, "
            f"fs={self.sampling_rate}, "
            f"status={status!r})"
        )
