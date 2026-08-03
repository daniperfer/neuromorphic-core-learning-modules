"""
Here is the complete refactoring of the Week 10 NeuralPipeline into
a base class with an LFPPipeline subclass.
This is the pattern all subsequent Week 11 lectures will extend.
"""

import numpy as np
from scipy.signal import butter, filtfilt


class NeuralPipeline:
    """
    Base class for neural signal processing pipelines.
    Not meant to be used directly — subclass it for specific modalities.
    """

    def __init__(self, sampling_rate=1000, name="NeuralPipeline"):
        self.sampling_rate = sampling_rate
        self.name = name
        self.data = None
        self.processed_data = None
        self._processing_log = []

    def load_data(self, filepath):
        """Load neural data from a .npy file."""
        self.data = np.load(filepath)
        self._log(f"Loaded data from {filepath}: shape {self.data.shape}")
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

    def __repr__(self):
        """Print internal info."""
        return f"{self.__class__.__name__}(name={self.name!r}, fs={self.sampling_rate})"


class LFPPipeline(NeuralPipeline):
    """Pipeline for local field potential recordings."""

    def __init__(self, sampling_rate=1000, lowcut=1.0, highcut=100.0):
        super().__init__(sampling_rate=sampling_rate, name="LFPPipeline")
        self.lowcut = lowcut
        self.highcut = highcut

    def load_data(self, filepath):
        """Load neural data from a .npy file."""
        super().load_data(filepath)
        if self.data.ndim != 1:
            raise ValueError("LFP data must be 1D.")
        self._log("LFP validation passed.")
        return self

    def bandpass_filter(self):
        """Band pass filtering"""
        nyq = self.sampling_rate / 2.0
        b, a = butter(4, [self.lowcut / nyq, self.highcut / nyq], btype="band")
        self.processed_data = filtfilt(b, a, self.data)
        self._log(f"Bandpass filtered: {self.lowcut}–{self.highcut} Hz")
        return self

    def run(self):
        """Run the full pipeline."""
        self.bandpass_filter()
        self._log("LFP pipeline run complete.")
        return self


# Quick test
if __name__ == "__main__":
    np.random.seed(42)
    # Simulate a short LFP signal and save it
    t = np.linspace(0, 2, 2000)
    signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.random.randn(len(t))
    np.save("week11_simulated_lfp.npy", signal)

    pipeline = LFPPipeline(sampling_rate=1000, lowcut=1.0, highcut=100.0)
    pipeline.load_data("week11_simulated_lfp.npy")
    pipeline.run()
    for entry in pipeline.get_log():
        print(entry)
    print(repr(pipeline))
