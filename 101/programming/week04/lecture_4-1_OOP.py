"""
Lecture 4.1: Introduction to Object-Oriented Programming
"""

# Tracking neuron data without classes
neuron1_id = 1
neuron1_voltage = -70.0
neuron1_type = "pyramidal"
neuron1_threshold = -55.0
neuron1_spikes: list[int] = []

neuron2_id = 2
neuron2_voltage = -65.0
neuron2_type = "interneuron"
neuron2_threshold = -50.0
neuron2_spikes: list[int] = []


# Now imagine doing this for 200 neurons
# And writing a function that operates on one of them:
def check_spike(voltage, threshold, spikes):
    """Public function, floating free..."""
    if voltage >= threshold:
        spikes.append(voltage)
        return True
    return False


# You have to manually pass the right variables every time
# As your simulation grows, this becomes unmaintainable.
fired = check_spike(neuron1_voltage, neuron1_threshold, neuron1_spikes)


# The Solution: A Simple Class
class Neuron:
    """Represents a single biological neuron."""

    def __init__(self, neuron_id, neuron_type):
        self.id = neuron_id
        self.voltage = -70.0  # Resting membrane potential (mV)
        self.type = neuron_type
        self.threshold = -55.0  # Firing threshold (mV)
        self.spikes = []  # Timestamps or voltages at each spike

    def has_fired(self):
        """Return True if the neuron's voltage has crossed threshold."""
        return self.voltage >= self.threshold

    def reset(self):
        """Reset voltage to resting potential after a spike."""
        self.voltage = -70.0


neuron1 = Neuron(neuron_id=1, neuron_type="pyramidal")
neuron2 = Neuron(neuron_id=2, neuron_type="interneuron")

print(neuron1.voltage)  # -70.0
print(neuron2.type)  # interneuron
print(neuron1.id)  # 1
neuron1.voltage = -50.0  # Only neuron1 changes
print(neuron1.voltage)  # -50.0
print(neuron2.voltage)  # -70.0  — untouched
print()
neuron1 = Neuron(1, "pyramidal")
print(neuron1.has_fired())  # False — resting at -70.0
neuron1.voltage = -48.0  # Simulate depolarization
print(neuron1.has_fired())  # True — threshold crossed
neuron1.reset()
print(neuron1.voltage)  # -70.0 — back to rest
