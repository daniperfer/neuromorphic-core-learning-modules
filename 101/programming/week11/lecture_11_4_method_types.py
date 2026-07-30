"""
Lecture 11.4: Class Methods, Static Methods, and Properties
"""
from abc import ABC

import numpy as np

# ------------------------------
# @property: Computed Attributes


class NeuralPipeline(ABC):
    """NeuralPipeline"""

    def __init__(self, sampling_rate=1000, name="NeuralPipeline"):
        self.sampling_rate = sampling_rate
        self.name = name
        self.data = None
        self.processed_data = None
        self._processing_log = []

    def _log(self, message):
        """Adds a new message to the log"""
        self._processing_log.append(message)

    def load_data(self, filepath):
        """Load a .npy file and immediately validate it."""
        self.data = np.load(filepath)
        self._log(f"Loaded: {filepath} — shape {self.data.shape}")
        return self

    @property
    def nyquist(self):
        """The Nyquist frequency in Hz. Computed from sampling_rate."""
        return self.sampling_rate / 2.0

    @property
    def duration(self):
        """Duration of the loaded recording in seconds. Returns None if no data."""
        if self.data is None:
            return None
        return len(self.data) / self.sampling_rate

    @property
    def n_samples(self):
        """Number of samples in the loaded recording."""
        return len(self.data) if self.data is not None else 0

    _registry: dict[str, str] = {}

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
            raise ValueError(
                f"Unknown modality: {modality_name!r}. " f"Available: {list(cls._registry.keys())}"
            )
        return cls._registry[modality_name](**kwargs)

    @staticmethod
    def hz_to_radians(frequency_hz, sampling_rate):
        """Convert a frequency in Hz to radians per sample."""
        return 2 * np.pi * frequency_hz / sampling_rate

    @staticmethod
    def seconds_to_samples(seconds, sampling_rate):
        """Convert a duration in seconds to an integer number of samples."""
        return int(round(seconds * sampling_rate))

    @staticmethod
    def samples_to_seconds(n_samples, sampling_rate):
        """Convert a sample count to duration in seconds."""
        return n_samples / sampling_rate

    @staticmethod
    def validate_frequency_band(lowcut, highcut, sampling_rate):
        """
        Check that a frequency band is valid for the given sampling rate.
        Returns True or raises ValueError with a descriptive message.
        """
        nyq = sampling_rate / 2.0
        if lowcut <= 0:
            raise ValueError(f"lowcut must be positive, got {lowcut} Hz")
        if highcut >= nyq:
            raise ValueError(f"highcut ({highcut} Hz) must be below Nyquist ({nyq} Hz)")
        if lowcut >= highcut:
            raise ValueError(f"lowcut ({lowcut} Hz) must be less than highcut ({highcut} Hz)")
        return True


@NeuralPipeline.register("LFP")
class LFPPipeline(NeuralPipeline):
    """LFPPipeline"""

    def __init__(self, sampling_rate=1000, lowcut=1.0, highcut=100.0):
        super().__init__(sampling_rate=sampling_rate, name="LFPPipeline")
        self._lowcut = lowcut
        self._highcut = highcut

    @classmethod
    def from_dict(cls, config):
        """
        Create an LFPPipeline from a configuration dictionary.

        Example config:
        {
            "sampling_rate": 1000,
            "lowcut": 1.0,
            "highcut": 100.0
        }
        """
        return cls(
            sampling_rate=config.get("sampling_rate", 1000),
            lowcut=config.get("lowcut", 1.0),
            highcut=config.get("highcut", 100.0),
        )

    @classmethod
    def for_gamma_band(cls, sampling_rate=1000):
        """Create an LFPPipeline pre-configured for gamma-band analysis (30–80 Hz)."""
        instance = cls(sampling_rate=sampling_rate, lowcut=30.0, highcut=80.0)
        instance._log("Created from for_gamma_band() factory.")
        return instance

    @classmethod
    def for_theta_band(cls, sampling_rate=1000):
        """Create an LFPPipeline pre-configured for theta-band analysis (4–8 Hz)."""
        instance = cls(sampling_rate=sampling_rate, lowcut=4.0, highcut=8.0)
        instance._log("Created from for_theta_band() factory.")
        return instance

    @property
    def lowcut(self):
        """Returns lowcut."""
        return self._lowcut

    @lowcut.setter
    def lowcut(self, value):
        if value <= 0:
            raise ValueError(f"lowcut must be positive, got {value}")
        if value >= self.nyquist:
            raise ValueError(f"lowcut ({value} Hz) must be below Nyquist ({self.nyquist} Hz)")
        self._lowcut = value
        self._log(f"lowcut updated to {value} Hz")

    @property
    def highcut(self):
        """Returns highcut."""
        return self._highcut

    @highcut.setter
    def highcut(self, value):
        if value <= 0:
            raise ValueError(f"highcut must be positive, got {value}")
        if value >= self.nyquist:
            raise ValueError(f"highcut ({value} Hz) must be below Nyquist ({self.nyquist} Hz)")
        if value <= self._lowcut:
            raise ValueError(
                f"highcut ({value} Hz) must be greater than lowcut ({self._lowcut} Hz)"
            )
        self._highcut = value
        self._log(f"highcut updated to {value} Hz")


pipeline = LFPPipeline(sampling_rate=1000)
print(pipeline.nyquist)  # 500.0  — no () needed
pipeline.load_data("week11_simulated_lfp.npy")
print(pipeline.duration)  # e.g. 2.0  — automatically reflects loaded data
print(pipeline.n_samples)  # e.g. 2000
pipeline.lowcut = 4.0  # Calls the setter, which validates
pipeline.highcut = 80.0  # Validated against Nyquist and lowcut

try:
    pipeline.lowcut = -1.0  # Raises ValueError immediately
except ValueError:
    print("ValueError: lowcut must be positive!")

try:
    pipeline.highcut = 600.0  # Raises ValueError: above Nyquist
except ValueError:
    print("ValueError: highcut must be below Nyquist!")
print()

# -------------------------------------------------------------
# @classmethod: Factory Constructors and Class-Level Operations

# Standard construction
pipeline2 = LFPPipeline(sampling_rate=1000, lowcut=1.0, highcut=100.0)

# Factory from config dict (useful when loading from JSON/YAML)
config = {"sampling_rate": 2000, "lowcut": 0.5, "highcut": 200.0}
pipeline2 = LFPPipeline.from_dict(config)

# Domain-specific factory — the intent is immediately clear
gamma_pipeline = LFPPipeline.for_gamma_band()
theta_pipeline = LFPPipeline.for_theta_band()
print()

# Now you can create pipelines by name — useful in automated batch processing
pipeline = NeuralPipeline.create("LFP", sampling_rate=1000)
print()

# -------------------------------------
# @staticmethod: Pure Utility Functions

# Call on the class directly — no instance needed
n = NeuralPipeline.seconds_to_samples(0.5, 1000)  # 500
print(n)
freq_rad = NeuralPipeline.hz_to_radians(10.0, 1000)  # ~0.0628
print(freq_rad)

# Can also call on an instance
n = pipeline.seconds_to_samples(0.5, 1000)  # Same result
print(n)

# Validate a frequency band before creating a pipeline
val = NeuralPipeline.validate_frequency_band(1.0, 100.0, 1000)  # OK
print(val)
try:
    val = NeuralPipeline.validate_frequency_band(1.0, 600.0, 1000)  # Raises ValueError
    print(val)
except ValueError:
    print("ValueError: highcut must be below Nyquist")
print()
