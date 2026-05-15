# Assignment 3: Neuron Simulation Library
# Student Name: Daniel Pereira
# Date: May 15, 2026


def initialize_neuron(neuron_id, V_rest=-70.0):
    """
    Create a new neuron with default parameters.

    Params:
        neuron_id (int): unique neuron identifier
        V_rest (float): resting membrane potential in mV (default: -70.0)

    Returns:
        dict: neuron properties including id, current voltage in mV,
              resting potential in mV, and time constant in ms
    """
    # Return a dictionary with the following keys:
    # 'id', 'V', 'V_rest', 'tau'
    # Starting voltage should equal V_rest
    # Default tau is 20.0 ms
    return {"id": neuron_id, "V": V_rest, "V_rest": V_rest, "tau": 20}


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
    # Implement LIF voltage update
    dV_leak = -(V - V_rest) / tau * dt
    dV_input = I_input * dt
    V_new = V + dV_leak + dV_input
    return V_new


def check_spike(V, threshold=-55.0):
    """
    Determine whether a membrane voltage has crossed the firing threshold.

    Params:
        V (float): current membrane voltage in mV
        threshold (float): action potential threshold in mV (default: -55.0)

    Returns:
        bool: True if V >= threshold, False otherwise
    """
    # Return True if V has reached or exceeded threshold
    return V >= threshold


def reset_voltage(V_reset=-70.0):
    """
    Return the post-spike reset voltage.

    Params:
        V_reset (float): voltage to reset to after a spike in mV (default: -70.0)

    Returns:
        float: reset voltage in mV
    """
    # Return the reset voltage
    return V_reset


def calculate_firing_rate(spike_times, duration):
    """
    Calculate mean firing rate from a list of spike times.

    Params:
        spike_times (list): spike timestamps in milliseconds
        duration (float): total recording duration in SECONDS

    Returns:
        float: firing rate in Hz, or 0.0 if no spikes occurred
    """
    # Return len(spike_times) / duration
    # Handle the case where spike_times is empty
    if duration <= 0:
        return None
    return len(spike_times) / duration


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
    # Implement the simulation loop
    # Hints:
    # - Extract V, V_rest, tau from neuron_params
    print(f"\nSimulating neuron {neuron_params['id']} for {duration:.1f} ms...")
    V = neuron_params["V"]
    V_rest = neuron_params["V_rest"]
    tau = neuron_params["tau"]
    dt = 1.0
    spike_times = []
    # - Loop through time steps from dt to duration using a while or for loop
    time = 0
    while time < duration:
        # - At each step: update voltage, check for spike, reset if needed
        V = update_voltage(V, I_input, tau=tau, V_rest=V_rest, dt=dt)
        if check_spike(V):
            # - Collect spike times in a list
            spike_times.append(time)
            V = reset_voltage()
            # - Print each spike as: f"⚡ Spike at {time:.1f} ms"
            print(f"⚡ Spike at {time:.1f} ms")
        time += dt
    return spike_times


# ── Run your tests when the script is executed directly ──────────────────────
if __name__ == "__main__":
    print("=== Testing Neuron Library ===\n")
    duration_ms = 100
    input_current = 1.3

    # Test 1: Initialize a neuron
    neuron = initialize_neuron(1)
    print(f"Created neuron: {neuron}")

    # Test 2: Run the simulation
    spike_times = simulate_neuron(duration=duration_ms, I_input=input_current, neuron_params=neuron)

    # Test 3: Calculate and report firing rate
    print(f"\nSpike times: {spike_times}")
    if len(spike_times) > 0:
        rate = calculate_firing_rate(spike_times, duration=duration_ms / 1000)
        print(f"Firing rate: {rate:.2f} Hz")
    else:
        print("No spikes recorded.")

    print("\n=== All Tests Passed! ===")


"""
# Assignment_3 Daniel Pereira

A short document showing outputs of `assignment_3_danielpereira.py`.

Testing with values: I_input=2.5, duration=100
=== Testing Neuron Library ===

Created neuron: {'id': 1, 'V': -70.0, 'V_rest': -70.0, 'tau': 20}

Simulating neuron 1 for 100.0 ms...
⚡ Spike at 6.0 ms
⚡ Spike at 13.0 ms
⚡ Spike at 20.0 ms
⚡ Spike at 27.0 ms
⚡ Spike at 34.0 ms
⚡ Spike at 41.0 ms
⚡ Spike at 48.0 ms
⚡ Spike at 55.0 ms
⚡ Spike at 62.0 ms
⚡ Spike at 69.0 ms
⚡ Spike at 76.0 ms
⚡ Spike at 83.0 ms
⚡ Spike at 90.0 ms
⚡ Spike at 97.0 ms

Spike times: [6.0, 13.0, 20.0, 27.0, 34.0, 41.0, 48.0, 55.0, 62.0, 69.0, 76.0, 83.0, 90.0, 97.0]
Firing rate: 140.00 Hz

============================================================

Testing with values: I_input=2.0, duration=100
=== Testing Neuron Library ===

Created neuron: {'id': 1, 'V': -70.0, 'V_rest': -70.0, 'tau': 20}

Simulating neuron 1 for 100.0 ms...
⚡ Spike at 9.0 ms
⚡ Spike at 19.0 ms
⚡ Spike at 29.0 ms
⚡ Spike at 39.0 ms
⚡ Spike at 49.0 ms
⚡ Spike at 59.0 ms
⚡ Spike at 69.0 ms
⚡ Spike at 79.0 ms
⚡ Spike at 89.0 ms
⚡ Spike at 99.0 ms

Spike times: [9.0, 19.0, 29.0, 39.0, 49.0, 59.0, 69.0, 79.0, 89.0, 99.0]
Firing rate: 100.00 Hz

============================================================

Testing with values: I_input=1.3, duration=100
=== Testing Neuron Library ===

Created neuron: {'id': 1, 'V': -70.0, 'V_rest': -70.0, 'tau': 20}

Simulating neuron 1 for 100.0 ms...
⚡ Spike at 16.0 ms
⚡ Spike at 33.0 ms
⚡ Spike at 50.0 ms
⚡ Spike at 67.0 ms
⚡ Spike at 84.0 ms

Spike times: [16.0, 33.0, 50.0, 67.0, 84.0]
Firing rate: 50.00 Hz

============================================================
"""
