"""
Lecture 11.5: Dunder (double underscore) Methods and Operator Overloading
"""
import numpy as np
from lecture_11_4_pipeline_complete import NeuralPipeline
from scipy.signal import butter, filtfilt

# -----------------------------------
# repr and str: Human-Readable Output


@NeuralPipeline.register("LFP")
class LFPPipeline(NeuralPipeline):
    """LFPPipeline class."""

    def __init__(self, sampling_rate=1000, lowcut=1.0, highcut=100.0):
        super().__init__(sampling_rate=sampling_rate, name="LFPPipeline")
        self._lowcut = lowcut
        self._highcut = highcut

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
        b, a = butter(4, [self._lowcut / nyq, self._highcut / nyq], btype="band")
        self.processed_data = filtfilt(b, a, self.data)
        self._log(f"Bandpass filtered: {self._lowcut}–{self._highcut} Hz")
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

    def __add__(self, other):
        """
        Concatenate two LFP recordings along the time axis.
        Both pipelines must have the same sampling rate.
        Returns a new LFPPipeline with the concatenated data.
        """
        if not isinstance(other, LFPPipeline):
            return NotImplemented
        if self.sampling_rate != other.sampling_rate:
            raise ValueError(
                f"Cannot concatenate: sampling rates differ "
                f"({self.sampling_rate} vs {other.sampling_rate} Hz)"
            )
        if self.data is None or other.data is None:
            raise ValueError("Both pipelines must have data loaded before concatenating.")

        new_pipeline = LFPPipeline(
            sampling_rate=self.sampling_rate,
            lowcut=self._lowcut,
            highcut=self._highcut,
        )
        new_pipeline.data = np.concatenate([self.data, other.data])
        new_pipeline._log(
            f"Concatenated: {len(self.data)} + {len(other.data)} = "
            f"{len(new_pipeline.data)} samples"
        )
        return new_pipeline

    def __contains__(self, frequency_hz):
        """Check if a frequency is within this pipeline's passband."""
        return self._lowcut <= frequency_hz <= self._highcut


print("\nrepr and str:")
pipeline = LFPPipeline(sampling_rate=1000)
pipeline.load_data("week11_simulated_lfp.npy")
pipeline.run()

print("repr(pipeline)")
print(repr(pipeline))
# "LFPPipeline(modality='LFP', fs=1000, duration=2.0s)"
print("print(pipeline)")
print(pipeline)
# [LFPPipeline] modality=LFP, fs=1000 Hz, 2000 samples (2.00s), status=processed
print("str(pipeline)")
print(str(pipeline))
# "[LFPPipeline] modality=LFP, ..."

# --------------------------------------
# len and bool: Sizing and Truth Testing
print("\nlen and bool:")
pipeline2 = LFPPipeline()
bool(pipeline2)  # False — no data yet
print(len(pipeline2))  # 0
# Natural use in conditionals
if pipeline2:
    pipeline2.run()
else:
    print("Load data before running.")

bool(pipeline)  # True — data loaded
print(len(pipeline))  # 2000
# Natural use in conditionals
if pipeline:
    pipeline.run()
else:
    print("Load data before running.")
print()

# Natural use with lists
pipelines = [pipeline, pipeline2]
for p in pipelines:
    if p:  # Uses __bool__
        p.run()
print(pipeline.get_log())  # 3 times run
print()

# ----------------------------------
# eq and hash: Equality and Identity
print("\neq and hash:")

p1 = LFPPipeline(sampling_rate=1000)
p2 = LFPPipeline(sampling_rate=1000)
p1.load_data("week11_simulated_lfp.npy")
p2.load_data("week11_simulated_lfp.npy")

print(p1 == p2)  # True — same modality, fs, and sample count
print(p1 is p2)  # False — different objects in memory

# Can use as dict keys
results = {p1: "processed", p2: "cached"}
print(len(results))  # 1 — they hash equally, so same key
print(results)
print()

# -------------------------------------------
# iter and getitem: Making Pipelines Iterable
print("\niter and getitem:")


class MultiChannelPipeline:
    """A container that runs one LFPPipeline per channel."""

    def __init__(self, n_channels, sampling_rate=1000, **pipeline_kwargs):
        self.pipelines = [
            LFPPipeline(sampling_rate=sampling_rate, **pipeline_kwargs) for _ in range(n_channels)
        ]
        self.n_channels = n_channels

    def __len__(self):
        return self.n_channels

    def __iter__(self):
        """Iterate over the per-channel pipelines."""
        return iter(self.pipelines)

    def __getitem__(self, index):
        """Access a specific channel's pipeline by index."""
        return self.pipelines[index]

    def __repr__(self):
        return f"MultiChannelPipeline(n_channels={self.n_channels})"

    def load_and_run(self, filepaths):
        """Load data and run each channel pipeline."""
        for pipeline, filepath in zip(self.pipelines, filepaths):
            pipeline.load_data(filepath)
            pipeline.run()
        return self


mc = MultiChannelPipeline(n_channels=4, sampling_rate=1000)

# Iteration
for channel_pipeline in mc:
    print(channel_pipeline)

# Indexing
first_channel = mc[0]
last_channel = mc[-1]

# List comprehension
all_durations = [p.duration for p in mc if p]
print(all_durations)

# Built-in functions
print(len(mc))  # 4
print(list(mc))  # [LFPPipeline(...), LFPPipeline(...), ...]
print()

# --------------------------------------
# add and contains: Operator Overloading
print("\nadd and contains:")
p10 = LFPPipeline(sampling_rate=1000, lowcut=1.0, highcut=100.0)
p20 = LFPPipeline(sampling_rate=1000, lowcut=1.0, highcut=100.0)

p10.load_data("week11_simulated_lfp.npy")
p20.load_data("week11_simulated_lfp.npy")

# Concatenation using +
combined = p10 + p20
print(len(combined))  # 4000 samples (2 + 2 seconds)

# Membership using in
print(10.0 in p10)  # True  — 10 Hz is within 1–100 Hz
print(200.0 in p10)  # False — 200 Hz exceeds highcut
print(0.5 in p10)  # False — 0.5 Hz below lowcut

# Use in analysis: filter out events outside the passband
event_frequencies = [4.0, 10.0, 80.0, 120.0, 200.0]
in_band = [f for f in event_frequencies if f in p10]
print(in_band)  # [4.0, 10.0, 80.0]
print()

# ----------------------------------------
# enter and exit: Context Manager Protocol
print("\nenter and exit (Context Manager Protocol):")

with LFPPipeline(sampling_rate=1000) as pipeline_ctx:
    pipeline_ctx.load_data("week11_simulated_lfp.npy")
    pipeline_ctx.run()
    print(pipeline_ctx.get_log())
# __exit__ is guaranteed to run here, even if an exception occurred inside the block
print()
