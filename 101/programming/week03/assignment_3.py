# Assignment 3: Neuron Simulation Library
# Student Name: [YOUR NAME]
# Date: [DATE]


def initialize_neuron(neuron_id, V_rest=-70.0):
    """
    Create a new neuron with default parameters.

    Params:
        neuron_id (int): unique neuron identifier
        V_rest (float): resting membrane potential in mV (default: -70.0)

    Returns:
        dict: neuron properties including id, current voltage,
              resting potential, and time constant
    """
    # TODO: Return a dictionary with the following keys:
    # 'id', 'V', 'V_rest', 'tau'
    # Starting voltage should equal V_rest
    # Default tau is 20.0 ms
    pass


def update_voltage(V, I_input, tau=20.0, V_rest=-70.0, dt=1.0):
    """
    Update membrane voltage by one time step using the LIF model.

    The leak term pulls voltage back toward resting potential.
    The input term drives voltage up in response to current.

    Params:
        V (float): current membrane voltage in mV
        I_input (float): input current in nanoamps
        tau (float): membrane time constant in ms (default: 20.0)
        V_rest (float): resting membrane potential in mV (default: -70.0)
        dt (float): simulation time step in ms (default: 1.0)

    Returns:
        float: updated membrane voltage in mV
    """
    # TODO: Implement LIF voltage update
    # dV_leak  = -(V - V_rest) / tau * dt
    # dV_input = I_input * dt
    # V_new    = V + dV_leak + dV_input
    pass


def check_spike(V, threshold=-55.0):
    """
    Determine whether a membrane voltage has crossed the firing threshold.

    Params:
        V (float): current membrane voltage in mV
        threshold (float): action potential threshold in mV (default: -55.0)

    Returns:
        bool: True if V >= threshold, False otherwise
    """
    # TODO: Return True if V has reached or exceeded threshold
    pass


def reset_voltage(V_reset=-70.0):
    """
    Return the post-spike reset voltage.

    Params:
        V_reset (float): voltage to reset to after a spike in mV (default: -70.0)

    Returns:
        float: reset voltage in mV
    """
    # TODO: Return the reset voltage
    pass


def calculate_firing_rate(spike_times, duration):
    """
    Calculate mean firing rate from a list of spike times.

    Params:
        spike_times (list): spike timestamps in milliseconds
        duration (float): total recording duration in SECONDS

    Returns:
        float: firing rate in Hz, or 0.0 if no spikes occurred
    """
    # TODO: Return len(spike_times) / duration
    # Handle the case where spike_times is empty
    pass


def simulate_neuron(duration, I_input, neuron_params):
    """
    Run a complete LIF neuron simulation.

    Steps through time from 0 to duration (ms), updating voltage each step.
    Records and prints each spike. Returns list of all spike times.

    Params:
        duration (float): simulation duration in milliseconds
        I_input (float): constant input current in nanoamps
        neuron_params (dict): neuron properties from initialize_neuron()

    Returns:
        list of float: spike times in milliseconds
    """
    # TODO: Implement the simulation loop
    # Hints:
    # - Extract V, V_rest, tau from neuron_params
    # - Loop through time steps from dt to duration using a while or for loop
    # - At each step: update voltage, check for spike, reset if needed
    # - Collect spike times in a list
    # - Print each spike as: f"⚡ Spike at {time:.1f} ms"
    pass


# ── Run your tests when the script is executed directly ──────────────────────
if __name__ == "__main__":
    print("=== Testing Neuron Library ===\n")

    # Test 1: Initialize a neuron
    neuron = initialize_neuron(1)
    print(f"Created neuron: {neuron}")

    # Test 2: Run the simulation
    spike_times = simulate_neuron(duration=100, I_input=2.5, neuron_params=neuron)

    # Test 3: Calculate and report firing rate
    print(f"\nSpike times: {spike_times}")
    if len(spike_times) > 0:
        rate = calculate_firing_rate(spike_times, duration=100 / 1000)
        print(f"Firing rate: {rate:.2f} Hz")
    else:
        print("No spikes recorded.")

    print("\n=== All Tests Passed! ===")
