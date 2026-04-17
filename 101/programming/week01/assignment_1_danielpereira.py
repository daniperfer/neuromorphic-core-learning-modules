"""
Assignment 1: Neuron Voltage Simulator
Student Name: Daniel Pereira
Date: April 17, 2026
Course: NEUR 101 - Introduction to Programming with Python

This program simulates basic neuron voltage dynamics using Ohm's law.
It calculates how a neuron's membrane potential changes when current
is injected, and determines whether the neuron fires an action potential.
"""

import math

# ============================================================
# SECTION 1: WELCOME SCREEN
# ============================================================
print("=" * 60)
print(" " * 15 + "NEUROSCIENCE CALCULATOR v1.0")
print(" " * 10 + "Neuron Voltage Simulator")
print("=" * 60)
print()
print("This program models how a neuron's voltage changes")
print("when it receives an input current.")
print("Formula: ΔV = I × R  (Ohm's Law)")
print()

# ============================================================
# SECTION 2: GET USER INPUTS
# ============================================================
print("-" * 60)
print("Enter Neuron Parameters")
print("-" * 60)

# Get a neuron ID number from the user (whole number — use int)
# Example: neuron_id = int(input("Enter Neuron ID: "))
neuron_id = int(input("Enter Neuron ID: "))

# Get the neuron type as text — no conversion needed, stays a string
neuron_type = input("Enter Neuron type (e.g., Pyramidal, Interneuron): ").strip().title()

# Get the starting membrane voltage in mV (decimal — use float)
v_initial = float(input("Enter initial voltage (mV): "))

# Get the injected current in nanoamps (decimal — use float)
i_current = float(input("Enter input current (nA): "))

# Get the membrane resistance in megaohms (decimal — use float)
r_membrane = float(input("Enter membrane resistance (MΩ): "))

# Get the duration of one time step in milliseconds (decimal — use float)
time_step = float(input("Enter time step duration (ms): "))

print()

# ============================================================
# SECTION 3: CALCULATIONS
# ============================================================

# Calculate voltage change: ΔV = I × R
delta_v = i_current * r_membrane

# Calculate new membrane potential: V_new = V_initial + ΔV
v_new = v_initial + delta_v

# Define the spike threshold (this one is done for you)
threshold = -55.0  # mV — the voltage at which an action potential fires

# Did the neuron spike? Create a boolean: True if v_new >= threshold
did_spike = True if v_new >= threshold else False

# How much more voltage is needed to reach threshold (only if no spike)?
voltage_needed = 0
if not did_spike:
    voltage_needed = threshold - v_new    

# ============================================================
# SECTION 4: DISPLAY RESULTS
# ============================================================
print("=" * 60)
print(" " * 18 + "SIMULATION RESULTS")
print("=" * 60)
print()

print("NEURON INFORMATION:")
print(f"  Neuron ID:   {neuron_id}")
print(f"  Type:        {neuron_type}")
print()

print("INPUT PARAMETERS:")
print(f"  Initial voltage:     {v_initial:+.2f} mV")
print(f"  Input current:       {i_current:+.2f} nA")
print(f"  Membrane resistance: {r_membrane:+.2f} MΩ")
print(f"  Time step:           {time_step:+.2f} ms")
print()

print("CALCULATED RESULTS:")
# Display voltage change formatted to 2 decimal places
print(f"  Voltage change (ΔV):     {delta_v:+.2f} mV")
# Display new voltage formatted to 2 decimal places
print(f"  New membrane potential:  {v_new:+.2f} mV")
print(f"  Spike threshold:         {threshold:+.2f} mV")
print()

print("SPIKE STATUS:")
if did_spike:
    print("  ⚡ SPIKE DETECTED!")
    print("  The neuron fired an action potential.")
    print(f"  Voltage exceeded threshold by {v_new - threshold:.2f} mV")
else:
    print("  ✗ No spike.")
    print(f"  Voltage is {voltage_needed:.2f} mV below threshold.")
    # If resistance is valid, calculate how much more current would be needed
    if r_membrane > 0:
        current_needed = voltage_needed / r_membrane
        print(f"  Would need {current_needed:.2f} more nA to reach threshold.")

print()

# ============================================================
# SECTION 5: BIOLOGICAL INTERPRETATION
# ============================================================
print("-" * 60)
print("BIOLOGICAL INTERPRETATION:")
print("-" * 60)

if v_new <= -80:
    print("The neuron is hyperpolarized — more negative than resting.")
    print("Inhibitory inputs (or open K⁺ channels) are suppressing activity.")
elif v_new <= -65:
    print("The neuron is near its resting potential.")
    print("This is a normal, quiet state — no significant input received.")
elif v_new < -55:
    print("The neuron is depolarized but has not yet reached threshold.")
    print("It's receiving excitatory input but not enough to fire.")
else:
    print("The neuron reached threshold and fired an action potential.")
    print("The spike will propagate down the axon to downstream neurons.")

print()

# ============================================================
# SECTION 6: FOOTER
# ============================================================
print("=" * 60)
print("Simulation complete.")
print("Keep exploring — one neuron at a time.")
print("=" * 60)
print()

# ============================================================
# BONUS: Additional Calculations
# ============================================================
print("=" * 60)
print("BONUS: Additional Calculations.")
print("=" * 60)
# BONUS 1: If the neuron fired, calculate the approximate firing rate.
# Firing rate (Hz) = 1000 / time_step (converts ms to spikes per second)
firing_rate = 1000 / time_step
print(f"  Firing rate {firing_rate:.2f} Hz")

# BONUS 2: Handle division by zero if r_membrane = 0
# Add a check before the delta_v calculation that prints a warning
# and sets delta_v = 0 if r_membrane is zero.
if r_membrane == 0:
    print("r_membrane is zero! Setting delta_v to zero.")
    delta_v = 0
