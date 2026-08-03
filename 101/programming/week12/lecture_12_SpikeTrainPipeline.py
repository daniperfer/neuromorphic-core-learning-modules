import numpy as np
from week11.lecture_11_7_NeuralAnalysisFramework import NeuralPipeline


@NeuralPipeline.register("spike_train")
class SpikeTrainPipeline(NeuralPipeline):
    """Pipeline for spike train analysis."""

    def load(self, filepath):
        """Load data."""
        self.data = np.load(filepath)
        self.recording_duration = 10.0  # will be made configurable in 12.4
        return self

    def preprocess(self):
        """Validation checks."""
        # Validate invariants
        assert np.all(np.diff(self.data) > 0), "Spike times must be strictly increasing"
        return self

    def analyze(self):
        """Run analysis."""
        n_spikes = len(self.data)
        self.results = {
            "n_spikes": n_spikes,
            "mean_firing_rate": n_spikes / self.recording_duration,
        }
        return self

    def report(self):
        """Report statistics."""
        print("Spike Train Analysis")
        print(f"  Spikes:       {self.results['n_spikes']}")
        print(f"  Firing rate:  {self.results['mean_firing_rate']:.2f} Hz")
        return self
