def calculate_firing_rate_v1(spikes, duration):
    """Calculate firing rate in Hz given spike count and duration in seconds."""
    rate = spikes / duration
    return rate


# Use it three times — each call is one clean line
rate1 = calculate_firing_rate_v1(10, 5)
rate2 = calculate_firing_rate_v1(20, 10)
rate3 = calculate_firing_rate_v1(15, 7.5)

print(f"Rates: {rate1}, {rate2}, {rate3} Hz\n")


# Include a Safety Check
def calculate_firing_rate_v2(spikes, duration):
    """
    Calculate firing rate in Hz.

    Args:
        spikes   - number of action potentials recorded
        duration - recording duration in seconds

    Returns:
        firing rate in Hz, or None if duration is invalid
    """
    if duration <= 0:
        print(f"Warning: invalid duration ({duration}s). Skipping.")
        return None

    rate = spikes / duration
    return rate


# Test with good data
rate_a = calculate_firing_rate_v2(15, 3.0)
print(f"Neuron A: {rate_a} Hz\n")

# Test with bad data — function handles it gracefully
rate_b = calculate_firing_rate_v2(8, 0)
print(f"Neuron B: {rate_b}\n")

""" Neuroscience Application: Analyzing Multiple Neurons
"""


def calculate_firing_rate(spikes, duration):
    """Calculate firing rate in Hz."""
    if duration <= 0:
        return None
    return spikes / duration


def classify_neuron(firing_rate):
    """
    Classify a neuron's activity based on its firing rate.

    Args:
        firing_rate: spikes per second average rate (float)

    Returns a string label: 'silent', 'low', 'moderate', or 'high'.
    """
    if firing_rate is None:
        return "unknown"
    elif firing_rate == 0:
        return "silent"
    elif firing_rate < 5:
        return "low activity"
    elif firing_rate < 20:
        return "moderate activity"
    else:
        return "high activity"


# Data from 5 neurons
spike_counts = [0, 20, 45, 180, 210]
recording_duration = 10.0  # seconds

print("Neuron Analysis Results")
print("-" * 35)

for i, spikes in enumerate(spike_counts):
    neuron_id = i + 1
    rate = calculate_firing_rate(spikes, recording_duration)
    label = classify_neuron(rate)
    print(f"Neuron {neuron_id}: {spikes} spikes in {recording_duration} s, {rate:.1f} Hz — {label}")
