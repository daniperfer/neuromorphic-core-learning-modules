"""
Lecture 4.3: The __init__ Method and Instance Variables
"""


class Neuron:
    """Models a single biological neuron.
    __init__ can have default values, threshold=-55.0, initial_voltage=-70.0

    Never use a mutable object (like a list or dictionary) as a default parameter value.
    """

    def __init__(self, neuron_id, neuron_type, threshold=-55.0, initial_voltage=-70.0):
        print(f"Setting up object with id={id(self)}")  # id() shows memory address
        if threshold > 0:
            raise ValueError(
                f"Threshold must be negative (membrane potential is in mV). " f"Got: {threshold}"
            )
        if neuron_type not in (
            "pyramidal",
            "interneuron",
            "purkinje",
            "granule",
            "fast-spiking interneuron",
        ):
            raise ValueError(f"Unknown neuron type: {neuron_type}")

        self.id = neuron_id  # Unique identifier
        self.type = neuron_type  # Cell type (pyramidal, interneuron, etc.)
        self.voltage = initial_voltage  # Membrane potential (mV), starts at rest
        self.threshold = threshold  # Firing threshold (mV)
        self.spike_times = []  # Record of when this neuron fired
        self.is_refractory = False  # Whether the cell is in its refractory period
        # Compute something useful from the inputs
        self.headroom = abs(self.voltage - self.threshold)  # mV until threshold


pyramidal = Neuron(1, "pyramidal")
interneuron = Neuron(2, "interneuron")
print(pyramidal.id)  # 1
print(pyramidal.voltage)  # -70.0
print(interneuron.type)  # interneuron
print(interneuron.spike_times)  # []
print()
# Use the defaults
n1 = Neuron(1, "pyramidal")
print(n1.threshold)  # -55.0
print(n1.headroom)  # 15.0 — needs 15 mV of depolarization to fire

# Override for a specific neuron with a different threshold
n2 = Neuron(2, "fast-spiking interneuron", threshold=-50.0)
print(n2.threshold)  # -50.0

# Keyword arguments work too
n3 = Neuron(3, "pyramidal", initial_voltage=-68.0)
print(n3.voltage)  # -68.0
print(n3.threshold)  # -55.0 (default)

# Raises ValueError
try:
    n4 = Neuron(4, "pyramidal", threshold=0.9)
except ValueError as e:
    print(f"ERROR message: {e}")


# WRONG — don't do this
class NeuronWrong:
    """Never use a mutable object (like a list or dictionary) as a default parameter value."""

    def __init__(self, neuron_id, spike_times=[]):  # Shared list!
        self.id = neuron_id
        self.spike_times = spike_times


n5 = NeuronWrong(1)
n6 = NeuronWrong(2)

n5.spike_times.append(10.5)
print(n5.spike_times)  # [10.5]
print(n6.spike_times)  # [10.5] ← WRONG! n2 was never modified


# RIGHT
class NeuronRight:
    """The correct pattern is to use None as the default and create a fresh list inside __init__"""

    def __init__(self, neuron_id, spike_times=None):
        self.id = neuron_id
        self.spike_times = spike_times if spike_times is not None else []


n7 = NeuronRight(1)
n8 = NeuronRight(2)

n7.spike_times.append(10.5)
print(n7.spike_times)  # [10.5]
print(n8.spike_times)  # [] ← Correct — independent list


class WellDesignedNeuron:
    """
    Models a single biological neuron.

    Params
    ----------
    neuron_id : int
        Unique identifier for this cell.
    neuron_type : str
        Cell type: 'pyramidal', 'interneuron', 'purkinje', or 'granule'.
    threshold : float, optional
        Firing threshold in mV. Default -55.0.
    """

    def __init__(self, neuron_id, neuron_type, threshold=-55.0):
        # Validation
        if threshold > 0:
            raise ValueError(f"Threshold must be negative. Got {threshold}")

        # Identity
        self.id = neuron_id
        self.type = neuron_type

        # Electrophysiology
        self.voltage = -70.0  # Resting membrane potential (mV)
        self.threshold = threshold  # Firing threshold (mV)
        self.is_refractory = False

        # History
        self.spike_times = []  # Fresh list for every neuron

        # Computed
        self.headroom = abs(self.voltage - self.threshold)


print()
# Create a small network
cells = [WellDesignedNeuron(i, "pyramidal") for i in range(3)]
cells.append(WellDesignedNeuron(3, "interneuron", threshold=-50.0))

for cell in cells:
    print(
        f"Neuron {cell.id} ({cell.type}): "
        f"threshold={cell.threshold} mV, headroom={cell.headroom} mV"
    )
