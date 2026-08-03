"""
Lecture 4.4: Instance Variables vs. Class Variables
"""


class Neuron_1:
    """
    Instance variables are created with self inside __init__ (or any method).
    Each object gets its own independent copy:
    """

    def __init__(self, neuron_id, neuron_type):
        self.id = neuron_id  # Instance variable
        self.type = neuron_type  # Instance variable
        self.voltage = -70.0  # Instance variable
        self.spike_times = []  # Instance variable — fresh list per neuron


n1 = Neuron_1(1, "pyramidal")
n2 = Neuron_1(2, "interneuron")

# Modifying n1 has zero effect on n2
n1.voltage = -48.0
print(n1.voltage)  # -48.0
print(n2.voltage)  # -70.0 — untouched


class Neuron_2:
    """
    Class variables
    """

    species = "Mus musculus"  # The model organism
    resting_potential = -70.0  # Standard value for this cell type

    def __init__(self, neuron_id, neuron_type):
        self.id = neuron_id
        self.type = neuron_type
        self.voltage = self.resting_potential  # Read the class variable
        self.spike_times = []


n3 = Neuron_2(3, "pyramidal")
n4 = Neuron_2(4, "interneuron")

# Both access the same class variable
print()
print(n3.species)  # Mus musculus
print(n4.species)  # Mus musculus
print(Neuron_2.species)  # Mus musculus — accessible from the class too

# Changing the class variable updates the view for all instances
Neuron_2.resting_potential = -68.0
print(n3.resting_potential)  # -68.0
print(n4.resting_potential)  # -68.0


class Neuron_3:
    """
    Class variable: default threshold
    """

    threshold = -55.0  # Class variable: default threshold

    def __init__(self, neuron_id):
        self.id = neuron_id
        self.voltage = -70.0


n5 = Neuron_3(5)
n6 = Neuron_3(6)
print()
print(n5.threshold)  # -55.0 (reads class variable)

# Give n1 a custom threshold — creates an instance variable
n5.threshold = -50.0
print(n5.threshold)  # -50.0 (reads instance variable — shadows class variable)
print(n6.threshold)  # -55.0 (still reads class variable — unaffected)
print(Neuron_3.threshold)  # -55.0 (class variable unchanged)


class Neuron_4:
    """
    Class variable for counting
    """

    count = 0  # Tracks total neurons ever created

    def __init__(self, neuron_id, neuron_type):
        self.id = neuron_id
        self.type = neuron_type
        self.voltage = -70.0
        self.spike_times = []
        Neuron_4.count += 1  # Increment the class variable


n7 = Neuron_4(7, "pyramidal")
print()
print(Neuron_4.count)  # 1

n8 = Neuron_4(8, "interneuron")
n9 = Neuron_4(9, "pyramidal")
print(Neuron_4.count)  # 3

print(f"Network contains {Neuron_4.count} neurons")


# ############################################################
# DANGEROUS — do not do this. Should use a instance attribute, with self
class Neuron_5:
    """
    Do not do this: Mutable class variable.
    """

    spike_times: list[float] = []  # Mutable class variable: shared list.

    def __init__(self, neuron_id):
        self.id = neuron_id


n10 = Neuron_5(10)
n11 = Neuron_5(11)
print()
n10.spike_times.append(10.5)  # Appending to the shared list
print(n10.spike_times)  # [10.5]
print(n11.spike_times)  # [10.5] ← n2 was never modified!


# Application: Population Constants and Cell-Specific Data
class Neuron:
    """
    Models a cortical neuron.

    Class variables hold population-level constants.
    Instance variables hold cell-specific state.
    """

    # Population constants (class variables)
    species = "Mus musculus"
    cell_class = "cortical"
    standard_threshold = -55.0  # mV
    count = 0

    def __init__(self, neuron_id, neuron_type, threshold=None):
        # Cell-specific identity (instance variables)
        self.id = neuron_id
        self.type = neuron_type

        # Use per-cell threshold if provided, otherwise use population standard
        self.threshold = threshold if threshold is not None else Neuron.standard_threshold

        # Cell-specific state
        self.voltage = -70.0
        self.spike_times = []
        self.is_refractory = False

        # Update population count
        Neuron.count += 1


# Build a small mixed network
cells = [
    Neuron(0, "pyramidal"),
    Neuron(1, "pyramidal"),
    Neuron(2, "interneuron", threshold=-50.0),  # Custom threshold
]
print()
print(f"Network: {Neuron.count} cells, species: {Neuron.species}")
for c in cells:
    print(f"  Cell {c.id} ({c.type}): threshold={c.threshold} mV")
