"""
Lecture 12.4: The SpikeTrainPipeline — Adding a New Modality to the Framework
"""

import sys

from week11.lecture_11_7_NeuralAnalysisFramework import (
    NeuralAnalysisFramework,
    NeuralPipeline,
)

from .lecture_12_SpikeTrainPipeline import SpikeTrainPipeline

for p in sys.path:
    print(p)

"""
Launch from the project root as: python -m week12.lecture_12_4_adding_new_modality
"""

# Standalone test
spike_train_pipeline = SpikeTrainPipeline(recording_duration=10.0, sigma_ms=50.0, bin_width=0.1)
# The method chaining works because each method returns self
spike_train_pipeline.load_data("week12/week12_simulated_spikes.npy").preprocess().analyze().report()


# Assumes LFPPipeline and EEGPipeline are already registered (Week 11)
# and their data files are available

framework = NeuralAnalysisFramework(name="week12_demo")

# Add all three modalities
framework.add_pipeline(
    "lfp", NeuralPipeline.create("LFP", sampling_rate=1000, lowcut=1.0, highcut=100.0)
)
framework.add_pipeline("eeg", NeuralPipeline.create("EEG", sampling_rate=256, notch_freq=60.0))
framework.add_pipeline(
    "spike_train",
    SpikeTrainPipeline(recording_duration=10.0, sigma_ms=50.0, bin_width=0.1, sampling_rate=1000),
)

# Load and run everything
framework.load_all(
    {
        "lfp": "week11/week11_lect07_simulated_lfp.npy",
        "eeg": "week11/week11_lect07_simulated_eeg.npy",
        "spike_train": "week12/week12_simulated_spikes.npy",
    }
)
# Run all pipelines
framework.run_all()

# Generate all reports
framework.print_summary()

print(framework._pipelines["spike_train"].get_log())
print(framework._run_times)
