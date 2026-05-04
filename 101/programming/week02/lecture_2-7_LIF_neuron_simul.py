print("=== LIF Neuron Simulator ===\n")

# Biological parameters
V_rest      = -70.0   # Resting potential (mV) — where voltage returns when idle
V_threshold = -55.0   # Spike threshold (mV) — voltage at which neuron fires
V_reset     = -70.0   # Reset voltage after spike (mV) — same as resting here

# Simulation parameters
tau      = 20.0   # Time constant (ms) — controls how fast the leak pulls voltage back
dt       = 1.0    # Time step (ms) — how much time passes each iteration
duration = 100.0  # Total simulation duration (ms)

# Initial state
V = V_rest        # Neuron starts at resting potential
spike_times = []  # Empty list — will collect spike times as they occur
time = 0.0        # Simulation clock starts at zero

while time < duration:
    # --- Step 1: Determine input current at this moment in time ---
    # The stimulus turns on at 20 ms and off at 80 ms
    if 20 <= time < 80:
        I_input = 2.5   # Sustained input current (nanoamps)
    else:
        I_input = 0.0   # No input before stimulus or after it ends

    # --- Step 2: Calculate how voltage changes this time step ---
    dV_leak  = -(V - V_rest) / tau * dt   # Leak: pulls voltage toward rest
    dV_input = I_input * dt               # Input: pushes voltage up

    # --- Step 3: Update the voltage ---
    V = V + dV_leak + dV_input

    # --- Step 4: Check for a spike ---
    if V >= V_threshold:
        spike_times.append(time)   # Record when the spike occurred
        V = V_reset                # Reset voltage immediately
        print(f"⚡ SPIKE at {time:.1f} ms")

    # --- Step 5: Advance the clock ---
    time += dt

print(f"\nSimulation complete!")
print(f"Total spikes: {len(spike_times)}")
print(f"Spike times: {spike_times}")

if len(spike_times) > 0:
    firing_rate = len(spike_times) / (duration / 1000)
    print(f"Firing rate: {firing_rate:.1f} Hz")
