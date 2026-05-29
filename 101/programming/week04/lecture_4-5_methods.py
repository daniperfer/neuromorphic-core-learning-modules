"""
Lecture 4.5: Instance Methods — Giving Objects Behavior
"""


class Neuron:
    """
    A method is a function defined inside a class.
    The only requirement that distinguishes it from a regular function is that
    its first parameter must be self.
    """

    def __init__(self, neuron_id, neuron_type):
        self.id = neuron_id
        self.type = neuron_type
        self.voltage = -70.0
        self.threshold = -55.0
        self.spike_times = []
        self.is_refractory = False

    def summary(self):
        """
        Print Neuron summary.
        """
        print(f"Neuron {self.id} ({self.type})")
        print(f"  Voltage: {self.voltage} mV")
        print(f"  Spikes:  {len(self.spike_times)}")
        print(f"  Times:   {self.spike_times}")

    def receive_input(self, current_nA, current_time_ms):
        """
        Apply input current. If threshold is crossed, fire.
        Returns True if the neuron fired, False otherwise.
        """
        if self.is_refractory:
            return False  # Can't fire during refractory period

        self.voltage += current_nA * 10

        if self.has_fired():  # Call another method
            self.fire(current_time_ms)  # Call another method
            return True

        return False

    def has_fired(self):
        """Return True if voltage is at or above threshold."""
        return self.voltage >= self.threshold

    def headroom(self):
        """Return the mV remaining before threshold is reached."""
        return self.threshold - self.voltage

    def firing_rate(self, duration_ms):
        """Return mean firing rate in Hz over a given duration."""
        if duration_ms <= 0:
            return 0.0
        return len(self.spike_times) / (duration_ms / 1000)

    def fire(self, current_time_ms):
        """Record a spike and reset voltage to resting potential."""
        self.spike_times.append(current_time_ms)
        self.voltage = -70.0
        self.is_refractory = True

    def end_refractory(self):
        """Mark the end of the refractory period."""
        self.is_refractory = False

    def reset(self):
        """Return neuron to its initial resting state."""
        self.voltage = -70.0
        self.spike_times = []
        self.is_refractory = False

    def excite(self, target_neuron, strength_nA, current_time_ms):
        """Send excitatory input to another neuron."""
        print(f"Neuron {self.id} → Neuron {target_neuron.id} ({strength_nA} nA)")
        target_neuron.receive_input(strength_nA, current_time_ms)


n1 = Neuron(1, "pyramidal")
print(n1.voltage)  # -70.0

n1.receive_input(1.0, 0.1)
print(n1.voltage)  # -60.0

print()
n1.voltage = -70
print(n1.has_fired())  # False
print(n1.headroom())  # 15.0 mV until threshold

n1.voltage = -48.0
print(n1.has_fired())  # True
print(n1.headroom())  # -7.0 (already past threshold)

print()
n1.fire(current_time_ms=15.5)
print(n1.voltage)  # -70.0 — reset after spike
print(n1.spike_times)  # [15.5]
print(n1.is_refractory)  # True

n1.end_refractory()
print(n1.is_refractory)  # False

print()
fired = n1.receive_input(current_nA=2.0, current_time_ms=20.0)
print(fired)  # True (voltage hit -50.0, above -55.0 threshold)
print(n1.spike_times)  # [15.5 20.0]
print(n1.voltage)  # -70.0 (reset)
print(n1.is_refractory)  # True

pre = n1
post = Neuron(2, "interneuron")
print()
pre.excite(post, strength_nA=2.5, current_time_ms=20.0)
# Neuron 1 → Neuron 2 (2.5 nA)
print(post.voltage)  # -70.0 — post-synaptic neuron fired
print(post.spike_times)  # [20.0]

print()
# Run a short simulation
n = Neuron(2, "pyramidal")

for t in range(0, 100, 10):
    n.receive_input(current_nA=1.5, current_time_ms=t)
    if n.is_refractory:
        n.end_refractory()

n.summary()
"""
Neuron 2 (pyramidal)
  Voltage: -70.0 mV
  Spikes:  10
  Times:   [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
"""
