"""
Lecture 3.2: Parameters, Arguments, and Return Values — Making Functions Flexible
"""


def calculate_voltage_change(current, resistance, dt):
    """
    Current, resistance, dt are: PARAMETERS

    Calculate the change in membrane voltage over one time step.

    Params:
        current: input current in nanoamps
        resistance: membrane resistance in megaohms
        dt: time step in milliseconds

    Returns:
        voltage change (dV) in millivolts
    """
    dV = current * resistance * dt
    return dV


change = calculate_voltage_change(2.0, 10.0, 1.0)  # 2.0, 10.0, 1.0 are: ARGUMENTS
print(f"Voltage change: {change} mV")


# DEFAULT ARGUMENTS
def is_above_threshold(voltage, threshold=-55.0):
    """
    Check whether a membrane voltage has crossed firing threshold.

    Params:
        voltage: current membrane potential in mV
        threshold: firing threshold in mV (default: -55.0 mV)

    Returns:
        True if voltage >= threshold, False otherwise
    """
    return voltage >= threshold


# Using the default threshold
print(is_above_threshold(-50.0))  # True  (-50 >= -55)
print(is_above_threshold(-60.0))  # False (-60 >= -55 is false)

# Overriding the default for a different neuron type
print(is_above_threshold(-50.0, threshold=-45.0))  # False (-50 >= -45 is false)


# RETURN VALUE/S
def analyze_spike_train(spike_times, duration):
    """
    Analyze basic properties of a spike train.

    Params:
        spike_times (list of float): Spike times in milliseconds.
        duration (float): Total recording duration in milliseconds.

    Returns:
        tuple: A tuple containing:
            - spike_count (int): Number of spikes.
            - firing_rate_hz (float): Average firing rate in Hz.
            - mean_isi_ms (float or None): Mean inter-spike interval in milliseconds,
              or None if fewer than two spikes are present.
    """
    spike_count = len(spike_times)

    # Convert duration to seconds for Hz calculation
    firing_rate_hz = spike_count / (duration / 1000.0)

    # Calculate mean inter-spike interval
    if spike_count < 2:
        mean_isi = None  # Can't compute ISI with fewer than 2 spikes
    else:
        intervals = []
        for i in range(1, spike_count):
            intervals.append(spike_times[i] - spike_times[i - 1])
        mean_isi = sum(intervals) / len(intervals)

    return spike_count, firing_rate_hz, mean_isi


# Analyze a sample spike train
spikes = [12.1, 45.3, 78.9, 110.2, 155.7]
count, rate, isi = analyze_spike_train(spike_times=spikes, duration=200.0)

print(f"Spike count: {count}")
print(f"Firing rate: {rate:.1f} Hz")
print(f"Mean ISI: {isi:.1f} ms")
