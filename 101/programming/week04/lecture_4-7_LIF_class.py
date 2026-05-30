"""
Lecture 4.7: Putting It All Together — The LIF Neuron Class
"""


class LIFNeuron:
    """
    Leaky Integrate-and-Fire neuron model.

    Simulates membrane voltage dynamics with leak, input integration,
    spike generation, and refractory period.
    """

    # Class variables: shared biological constants
    V_rest = -70.0  # Resting membrane potential (mV)
    V_reset = -70.0  # Post-spike reset voltage (mV)
    threshold = -55.0  # Firing threshold (mV)
    t_refractory = 5.0  # Absolute refractory period (ms)

    def __init__(self, neuron_id, tau=20.0):
        """
        Params
        ----------
        neuron_id : int
            Unique identifier for this cell.
        tau : float
            Membrane time constant in ms. Controls leak rate.
            Default 20.0 ms (typical for cortical pyramidal cells).
        """
        if tau <= 0:
            raise ValueError(f"tau must be positive. Got {tau}")

        # Identity
        self.id = neuron_id
        self.tau = tau  # Per-cell: tau varies by cell type

        # State
        self.voltage = self.V_rest  # Start at rest
        self.refractory_until = 0.0  # No refractory period at t=0

        # History
        self.spike_times = []  # Fresh list for every neuron

    def update(self, I_input, t, dt=1.0):
        """
        Advance the neuron one timestep.

        Params
        ----------
        I_input : float
            Input current (nA). Positive = excitatory.
        t : float
            Current simulation time (ms).
        dt : float
            Timestep size (ms). Default 1.0 ms.

        Returns
        -------
        bool
            True if the neuron fired this timestep, False otherwise.
        """
        # During refractory period: frozen, cannot fire
        if t < self.refractory_until:
            return False

        # Euler integration: leak + input
        dV_leak = -(self.voltage - self.V_rest) / self.tau * dt
        dV_input = I_input * dt
        self.voltage += dV_leak + dV_input

        # Check threshold
        if self.voltage >= self.threshold:
            self._fire(t)
            return True

        return False

    def _fire(self, t):
        """Record spike, reset voltage, begin refractory period."""
        self.spike_times.append(t)
        self.voltage = self.V_reset
        self.refractory_until = t + self.t_refractory

    def firing_rate(self, duration_ms):
        """
        Mean firing rate over a given duration.

        Params
        ----------
        duration_ms : float
            Duration of the recording window in ms.

        Returns
        -------
        float
            Firing rate in Hz (spikes per second).
        """
        if duration_ms <= 0:
            return 0.0
        return len(self.spike_times) / (duration_ms / 1000)

    def spike_count(self):
        """Return total number of spikes recorded."""
        return len(self.spike_times)

    def reset(self):
        """Return neuron to its initial state. Clears spike history."""
        self.voltage = self.V_rest
        self.spike_times = []
        self.refractory_until = 0.0

    def __str__(self):
        return (
            f"LIF neuron #{self.id} | "
            f"V={self.voltage:.1f} mV | "
            f"{self.spike_count()} spikes | "
            f"tau={self.tau} ms"
        )

    def __repr__(self):
        return (
            f"LIFNeuron(id={self.id}, tau={self.tau}, "
            f"voltage={self.voltage:.1f}, "
            f"spikes={self.spike_count()}, "
            f"refractory_until={self.refractory_until})"
        )


neuron = LIFNeuron(neuron_id=1, tau=25.0)
duration = 100  # ms
dt = 1.0

print(f"Starting simulation: {neuron}\n")

for t in range(duration):
    # Apply input only during the middle of the simulation
    I_current = 2.5 if 20 <= t < 80 else 0.0
    fired = neuron.update(I_current, t, dt)
    if fired:
        print(f"  Spike at t={t} ms")

print(f"\nFinal state: {neuron}")
print(f"Firing rate: {neuron.firing_rate(duration):.1f} Hz")
print(f"Spike times: {neuron.spike_times}")
print()

# Compare three neurons with different time constants
taus = [10.0, 20.0, 35.0]
duration = 100
I_input = 2.5

print("Effect of tau on firing rate (I=2.5 nA, 100 ms):\n")

for tau in taus:
    n = LIFNeuron(neuron_id=tau, tau=tau)
    for t in range(duration):
        I_current = I_input if 20 <= t < 80 else 0.0
        n.update(I_current, t)
    print(f"  tau={tau:5.1f} ms → {n.spike_count()} spikes, " f"{n.firing_rate(duration):.1f} Hz")
