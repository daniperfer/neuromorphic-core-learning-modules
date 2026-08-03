"""
Lecture 3.3: Positional, Keyword, and Default Arguments — Calling Functions Clearly
"""


def describe_neuron(neuron_id, neuron_type, voltage):
    """Describe a neuron's current state."""
    print(f"Neuron {neuron_id} ({neuron_type}): {voltage} mV")


# Correct order: id, type, voltage
describe_neuron(1, "pyramidal", -65.0)

# Wrong order — Python won't complain, but the output is nonsense
print("WRONG: ", end=" ")
describe_neuron(-65.0, 1, "pyramidal")

# Any of these orderings work identically
describe_neuron(voltage=-65.0, neuron_id=1, neuron_type="pyramidal")
describe_neuron(neuron_type="pyramidal", voltage=-65.0, neuron_id=1)

# Positional for the obvious ones, keyword for the easy-to-confuse ones
# You can’t put keyword arguments before positional ones though
describe_neuron(1, "pyramidal", voltage=-65.0)


# Default Parameter Values: Building in Sensible Assumptions
def calculate_rate(spikes, duration, unit="Hz"):
    """
    Calculate firing rate with a specified unit label.

    Params:
        spikes   - number of action potentials
        duration - recording duration in seconds
        unit     - label for the output string (default: "Hz")

    Returns:
        formatted string with rate and unit
    """
    rate = spikes / duration
    return f"{rate} {unit}"


# Use the default unit
print(calculate_rate(10, 5))

# Override when needed
print(calculate_rate(10, 5, "spikes/sec"))


"""
Neuroscience Application: The LIF Neuron as a Configurable Function
"""


def update_lif_neuron(V, I_input, V_rest=-70.0, tau=20.0, dt=1.0):
    """
    Compute the updated membrane voltage for one time step of a LIF neuron.

    The leak term pulls voltage back toward resting potential.
    The input term drives voltage in response to current.

    Params:
        V: current membrane voltage (mV)
        I_input: input current (nA)
        V_rest: resting membrane potential (mV), default -70.0
        tau: membrane time constant (ms), default 20.0
        dt: simulation time step (ms), default 1.0

    Returns:
        new membrane voltage (mV)
    """
    dV_leak = -(V - V_rest) / tau * dt  # Leak: pulls voltage toward rest
    dV_input = I_input * dt  # Drive: input current pushes voltage up
    V_new = V + dV_leak + dV_input
    return V_new


# Standard neuron — all defaults are fine
V1 = update_lif_neuron(-65.0, 2.0)
print(f"Standard neuron: {V1:.2f} mV")

# Slower neuron — override just the time constant
V2 = update_lif_neuron(-65.0, 2.0, tau=30.0)
print(f"Slow neuron (tau=30): {V2:.2f} mV")

# Fully specified — different resting potential, time constant, and time step
V3 = update_lif_neuron(-65.0, 2.0, V_rest=-75.0, tau=25.0, dt=0.5)
print(f"Custom neuron: {V3:.2f} mV")
