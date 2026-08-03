"""
Lecture 4.6: Special Methods — __str__ and __repr__
"""


class UnhelpfulNeuron:
    """
    Without either method defined, Python falls back to a generic representation.
    """

    def __init__(self, neuron_id, neuron_type):
        self.id = neuron_id
        self.type = neuron_type
        self.voltage = -70.0


nu = UnhelpfulNeuron(1, "pyramidal")
print(nu)  # <__main__.Neuron object at 0x7f8b8c1d4a90>
print()


class Neuron:
    """
    __str__: The Human-Readable Summary.
    __repr__: The Complete Technical Picture.
    """

    def __init__(self, neuron_id, neuron_type):
        self.id = neuron_id
        self.type = neuron_type
        self.voltage = -70.0
        self.threshold = -55.0
        self.spike_times = []
        self.is_refractory = False

    def __str__(self):
        status = "firing" if self.voltage >= self.threshold else "at rest"
        return (
            f"STR {self.type.title()} neuron #{self.id} | "
            f"V={self.voltage} mV | "
            f"{len(self.spike_times)} spikes | {status}"
        )

    def __repr__(self):
        return (
            f"REPR Neuron(id={self.id}, type='{self.type}', "
            f"voltage={self.voltage}, threshold={self.threshold}, "
            f"spikes={len(self.spike_times)}, refractory={self.is_refractory})"
        )


n = Neuron(1, "pyramidal")
print(n)
# Pyramidal neuron #1 | V=-70.0 mV | 0 spikes | at rest

n.voltage = -48.0
print(n)
# Pyramidal neuron #1 | V=-48.0 mV | 0 spikes | firing
n.voltage = -70.0

# Works naturally in f-strings too
print(f"Inspecting: {n}")
# Inspecting: Pyramidal neuron #1 | V=-70.0 mV | 0 spikes | firing

print(repr(n))
# Neuron(id=1, type='pyramidal', voltage=-48.0, threshold=-55.0, spikes=0, refractory=False)

print()
# __repr__ is especially valuable when inspecting a list of objects —
# Python uses __repr__ automatically when displaying list contents:
network = [Neuron(i, "pyramidal") for i in range(3)]
print(network)
# [Neuron(id=0, type='pyramidal', voltage=-70.0, threshold=-55.0, spikes=0, refractory=False),
#  Neuron(id=1, type='pyramidal', voltage=-70.0, threshold=-55.0, spikes=0, refractory=False),
#  Neuron(id=2, type='pyramidal', voltage=-70.0, threshold=-55.0, spikes=0, refractory=False)]

print()
print(n)  # __str__: Pyramidal neuron #1 | V=-70.0 mV | 0 spikes
print(repr(n))  # __repr__: Neuron(id=1, type='pyramidal', voltage=-70.0, ...)
print(str(n))  # __str__: Pyramidal neuron #1 | V=-70.0 mV | 0 spikes


class Neuron_2:
    """
    Always define __repr__.
    Define __str__ when you want a different, cleaner summary.
    """

    def __init__(self, neuron_id, neuron_type, threshold=-55.0):
        self.id = neuron_id
        self.type = neuron_type
        self.voltage = -70.0
        self.threshold = threshold
        self.spike_times = []
        self.is_refractory = False

    def receive_input(self, current_nA, t):
        """Receives input."""
        if self.is_refractory:
            return False
        self.voltage += current_nA * 10
        if self.voltage >= self.threshold:
            self.spike_times.append(t)
            self.voltage = -70.0
            self.is_refractory = True
            return True
        return False

    def end_refractory(self):
        """Ends refreeactory."""
        self.is_refractory = False

    def __str__(self):
        return (
            f"STR: {self.type.title()} #{self.id} | "
            f"V={self.voltage:.1f} mV | "
            f"{len(self.spike_times)} spikes"
        )

    def __repr__(self):
        return (
            f"REPR: Neuron(id={self.id}, type='{self.type}', "
            f"voltage={self.voltage}, threshold={self.threshold}, "
            f"spikes={self.spike_times}, refractory={self.is_refractory})"
        )


# Simulate 5 time steps
ns = Neuron_2(1, "pyramidal")
print()
for t in range(5):
    fired = ns.receive_input(current_nA=1.4, t=t * 10)
    print(f"t = {t * 10}ms: {ns}")  # __str__ gives a clean per-step readout
    if ns.is_refractory:
        ns.end_refractory()
