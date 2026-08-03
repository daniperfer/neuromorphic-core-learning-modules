"""
Lecture 11.6: Encapsulation, Composition vs. Inheritance
"""
from lecture_11_4_pipeline_complete import NeuralPipeline
from lecture_11_5_overloading import LFPPipeline
from scipy.signal import butter, sosfiltfilt

# ---------------------------------------------
# Encapsulation: Public, Protected, and Private

# Accessing from outside
pipeline = LFPPipeline(sampling_rate=2000)
print(pipeline.sampling_rate)  # Works — public
print(pipeline._processing_log)  # Works but discouraged — protected
try:
    print(pipeline.__version)  # AttributeError — mangled
except AttributeError:
    print("AttributeError: 'LFPPipeline' object has no attribute '__version'.")

# pipeline._NeuralPipeline__version --> Works but very bad practice. mypy marks an error
print(pipeline._NeuralPipeline__version)  # type: ignore[attr-defined]
print()

# ----------------------------------
# Composition: Objects as Components


class BandpassFilter:
    """A reusable bandpass filter component."""

    def __init__(self, lowcut, highcut, order=4):
        self.lowcut = lowcut
        self.highcut = highcut
        self.order = order

    def apply(self, data, sampling_rate):
        """Applies filter."""
        from scipy.signal import butter, filtfilt

        nyq = sampling_rate / 2.0
        b, a = butter(self.order, [self.lowcut / nyq, self.highcut / nyq], btype="band")
        return filtfilt(b, a, data)

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"BandpassFilter(lowcut={self.lowcut}, highcut={self.highcut}, order={self.order})"


class BaselineCorrection:
    """A reusable baseline correction component."""

    def __init__(self, baseline_window_sec=0.2):
        self.baseline_window_sec = baseline_window_sec

    def apply(self, data, sampling_rate):
        """Baseline correction."""
        n_baseline = int(self.baseline_window_sec * sampling_rate)
        baseline_mean = data[:n_baseline].mean()
        return data - baseline_mean

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"BaselineCorrection(window={self.baseline_window_sec}s)"


class JSONExporter:
    """A reusable JSON export component."""

    def export(self, pipeline, filepath):
        """Exporting."""
        import json

        result = {
            "name": pipeline.name,
            "modality": pipeline.modality,
            "sampling_rate": pipeline.sampling_rate,
            "log": pipeline.get_log(),
        }
        with open(filepath, "w") as f:
            json.dump(result, f, indent=2)
        return filepath


class LFPPipelineComposed(NeuralPipeline):
    """
    LFP pipeline built using composition.
    Behavior is provided by injected components, not inheritance.
    """

    def __init__(
        self,
        sampling_rate=1000,
        lowcut=1.0,
        highcut=100.0,
        filter_order=4,
        baseline_correction=None,
        exporter=None,
    ):
        super().__init__(sampling_rate=sampling_rate, name="LFPPipelineComposed")
        # Components injected via __init__ — can be replaced without subclassing
        self._filter = BandpassFilter(lowcut, highcut, order=filter_order)
        self._baseline = baseline_correction  # Optional — may be None
        self._exporter = exporter  # Optional — may be None

    @property
    def modality(self):
        """Returns modality."""
        return "LFP"

    def validate_data(self):
        """Validate data."""
        super().validate_data()
        if self.data.ndim != 1:
            raise ValueError("LFP data must be 1D.")

    def run(self):
        """Runs pipeline."""
        self.processed_data = self._filter.apply(self.data, self.sampling_rate)
        self._log(f"Filtered with {self._filter}")
        if self._baseline is not None:
            self.processed_data = self._baseline.apply(self.processed_data, self.sampling_rate)
            self._log(f"Baseline corrected with {self._baseline}")
        self._log("LFP pipeline complete.")
        return self

    def export(self, filepath=None):
        """Export results."""
        if self._exporter is None:
            raise RuntimeError("No exporter configured. Pass exporter= to __init__.")
        if filepath is None:
            filepath = f"{self.name}_results.json"
        return self._exporter.export(self, filepath)


# The power of this design becomes apparent when you change behavior.
# To swap the filter algorithm, you pass a different filter object — no subclassing required.
# To add baseline correction to an existing pipeline, you pass the component in:

# Standard LFP pipeline
pipeline_s = LFPPipeline(sampling_rate=1000, lowcut=1.0, highcut=100.0)

# Evoked LFP pipeline with baseline correction and export
evoked = LFPPipelineComposed(
    sampling_rate=1000,
    lowcut=1.0,
    highcut=100.0,
    baseline_correction=BaselineCorrection(baseline_window_sec=0.2),
    exporter=JSONExporter(),
)


# Swap filters without touching the pipeline class
class SosFilter:
    """Filter example."""

    def __init__(self, lowcut, highcut):
        self.lowcut = lowcut
        self.highcut = highcut

    def apply(self, data, sampling_rate):
        """Apply filtering."""
        sos = butter(
            4,
            [self.lowcut / (sampling_rate / 2), self.highcut / (sampling_rate / 2)],
            btype="band",
            output="sos",
        )
        return sosfiltfilt(sos, data)

    def __repr__(self):
        """Unambiguous representation for debugging."""
        return f"SosFilter(lowcut={self.lowcut}, highcut={self.highcut})"


evoked.load_data("week11_simulated_lfp.npy")
# Inject the new filter — no changes to LFPPipeline class
evoked._filter = SosFilter(1.0, 100.0)
evoked.run()
print(evoked.get_log())
