"""
Lecture 3.6: Docstrings — Writing Code That Explains Itself
"""


def calculate_firing_rate(spikes, duration):
    """
    Calculate the firing rate of a neuron.

    Params:
        spikes (int): number of action potentials recorded
        duration (float): recording duration in seconds

    Returns:
        float: firing rate in Hz

    Example:
        >>> calculate_firing_rate(10, 5)
        2.0
    """
    return spikes / duration


# A Complete Example: Docstring with Error Handling
def update_voltage(V, current, R, dt):
    """
    Update membrane voltage over one time step using Ohm's law.

    Computes the voltage change driven by input current through membrane
    resistance, and returns the new absolute voltage.

    Params:
        V (float): current membrane voltage in millivolts
        current (float): input current in nanoamps
        R (float): membrane resistance in megaohms
        dt (float): time step in milliseconds; must be positive

    Returns:
        float: updated membrane voltage in millivolts

    Raises:
        ValueError: if dt is zero or negative

    Example:
        >>> update_voltage(-70.0, 2.0, 10.0, 1.0)
        -50.0
    """
    if dt <= 0:
        raise ValueError(f"Time step must be positive, got {dt}")
    dV = current * R * dt
    return V + dV


print(update_voltage.__doc__)

# Normal use
print("Run: update_voltage(-70.0, 2.0, 10.0, 1.0)")
V_new = update_voltage(-70.0, 2.0, 10.0, 1.0)
print(f"Updated voltage: {V_new} mV")

# What happens with invalid input
print("Run: update_voltage(-70.0, 2.0, 10.0, dt=0)")
try:
    update_voltage(-70.0, 2.0, 10.0, dt=0)
except ValueError as e:
    print(f"\nERROR: Caught error: {e}")


# Without docstring — caller has to read the math to understand what's expected
def isi(s):
    """No docstring"""
    if len(s) < 2:
        return []
    return [s[i + 1] - s[i] for i in range(len(s) - 1)]


# With docstring — caller knows everything they need at a glance
def compute_interspike_intervals(spike_times):
    """
    Compute inter-spike intervals (ISIs) from a list of spike times.

    Params:
        spike_times (list of float): spike timestamps in milliseconds,
                                      assumed to be in ascending order

    Returns:
        list of float: time differences between consecutive spikes in ms.
        Returns an empty list if fewer than 2 spikes provided.

    Example:
        >>> compute_interspike_intervals([10.0, 25.0, 45.0, 80.0])
        [15.0, 20.0, 35.0]
    """
    if len(spike_times) < 2:
        return []
    return [spike_times[i + 1] - spike_times[i] for i in range(len(spike_times) - 1)]


print()
print(compute_interspike_intervals([10.0, 25.0, 45.0, 80.0]))
