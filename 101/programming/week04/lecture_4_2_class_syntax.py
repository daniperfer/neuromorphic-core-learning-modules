"""
Lecture 4.2: Class Syntax and Creating Objects
"""


class Neuron:
    """A simple neuron class."""

    pass


n1 = Neuron()
print(type(n1))  # <class '__main__.Neuron'>
print()
n1 = Neuron()
n2 = Neuron()
print(n1 is n2)  # False — two separate objects in memory


class Neuron_2:
    """A neuron with a SHARED resting potential."""

    resting_potential = -70.0  # Class attribute
    threshold = -55.0  # Class attribute


# Every Neuron you create will automatically have access to these values:

n3 = Neuron_2()
n4 = Neuron_2()
print()
print(n3.resting_potential)  # -70.0
print(n4.resting_potential)  # -70.0
print(Neuron_2.resting_potential)  # -70.0 — you can also access it via the class itself

# Watch what happens when you assign to an attribute on an individual instance:
n5 = Neuron_2()
n6 = Neuron_2()

n5.resting_potential = -65.0  # Assign to n5 specifically
print()
print(n5.resting_potential)  # -65.0
print(n6.resting_potential)  # -70.0 — unchanged
print(Neuron_2.resting_potential)  # -70.0 — unchanged

# If you intend to change the value for every neuron, modify the class attribute:
# Neuron.resting_potential = -68.0   # Changes the default for ALL neurons
# If you intend to customize one specific neuron, assigning to the instance is
# correct. Just know which one you’re doing

# You can attach attributes to an individual object after it’s been created,
# without defining them in the class at all:
n8 = Neuron()
n8.id = 1  # type: ignore[attr-defined]
n8.cell_type = "pyramidal"  # type: ignore[attr-defined]
n8.spike_history = []  # type: ignore[attr-defined]
n7 = Neuron()
n7.id = 2  # type: ignore[attr-defined]
# Forgot to add cell_type and spike_history!
# Python won’t stop you. But now n8 and n7 have different shapes —
# trying to access n7.cell_type will raise an AttributeError.
print()
try:
    print(n7.cell_type)  # type: ignore[attr-defined]
except AttributeError as e:
    print(f"ERROR message: {e}")
