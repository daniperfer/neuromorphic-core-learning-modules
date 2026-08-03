"""
Lecture 3.4: Return Values — Getting Results Out of Functions
"""


def spike_detector_v1(voltage, threshold=-55.0):
    """
    Determine whether a membrane voltage has crossed firing threshold.

    Params:
        voltage: current membrane potential in mV
        threshold: action potential threshold in mV (default: -55.0)

    Returns:
        True if spike occurred, False otherwise
    """
    if voltage >= threshold:
        return True  # Exit immediately — no need to continue
    return False  # Only reached if the condition above was false


def spike_detector_v2(voltage, threshold=-55.0):
    """Determine whether a membrane voltage has crossed firing threshold."""
    return voltage >= threshold


print(spike_detector_v2(voltage=-54, threshold=-55.0))


# Returning Multiple Values
def neuron_stats(spike_times):
    """
    Compute basic statistics from a list of spike times.

    Params:
        spike_times: list of spike timestamps in milliseconds

    Returns:
        tuple of (num_spikes, first_spike_ms, active_duration_ms)
        Returns (0, 0.0, 0.0) if no spikes recorded.
    """
    num_spikes = len(spike_times)

    if num_spikes == 0:
        return 0, 0.0, 0.0  # Early return for the empty case

    first_spike = spike_times[0]
    last_spike = spike_times[-1]
    duration = last_spike - first_spike

    return num_spikes, first_spike, duration


# Unpack the three return values directly into three variables
count, first, dur = neuron_stats([10.5, 25.3, 48.7, 89.2])
print(f"Spikes: {count}, First: {first} ms, Active window: {dur} ms")

stats = neuron_stats([10.5, 25.3, 48.7, 89.2])
print(stats)  # (4, 10.5, 78.7)
print(stats[0])  # 4  — access by index if needed


# Putting It Together: A Small Analysis Pipeline
def detect_spikes(voltage_trace, threshold=-55.0):
    """Return list of indices where voltage crossed threshold."""
    spike_indices = []
    for i, v in enumerate(voltage_trace):
        if v >= threshold:
            spike_indices.append(i)
    return spike_indices


def compute_firing_rate(spike_indices, duration_ms):
    """Return firing rate in Hz given spike indices and duration."""
    if duration_ms <= 0:
        return None
    return len(spike_indices) / (duration_ms / 1000.0)


# Simulated voltage trace (mV)
voltage = [-70, -68, -65, -58, -50, -45, -70, -68, -60, -52, -44, -70]

spikes = detect_spikes(voltage)
rate = compute_firing_rate(spikes, duration_ms=120.0)

print(f"Spikes detected at indices: {spikes}")
print(f"Firing rate: {rate:.1f} Hz")
