"""
Interactive Neuron Voltage Simulator
Collects user input and computes membrane potential dynamics
"""

import math

# ============================================================
# WELCOME
# ============================================================
print("=" * 55)
print(f"{'INTERACTIVE NEURON SIMULATOR':^55}")
print("=" * 55)
print()
print("This tool calculates how a neuron's membrane voltage")
print("changes when it receives an input current (Ohm's Law).")
print()

# ============================================================
# COLLECT INPUTS
# ============================================================
print("-" * 55)
print("NEURON PARAMETERS")
print("-" * 55)

# Identity
neuron_id   = int(input("  Neuron ID: "))
neuron_type = input("  Neuron type (e.g. Pyramidal): ").strip().title()
region      = input("  Brain region (e.g. hippocampus): ").strip().title()

print()

# Electrical properties
print("  Electrical properties:")
v_initial  = float(input("    Resting voltage (mV): "))
threshold  = float(input("    Spike threshold (mV): "))
resistance = float(input("    Membrane resistance (MΩ): "))

print()

# Stimulation
print("  Stimulation:")
current   = float(input("    Input current (nA): "))
time_step = float(input("    Time step duration (ms): "))

print()

# ============================================================
# CALCULATIONS
# ============================================================
delta_v   = current * resistance        # Ohm's law: ΔV = I × R
v_new     = v_initial + delta_v         # New membrane potential
did_spike = v_new >= threshold          # Did we reach threshold?

if not did_spike:
    voltage_needed  = threshold - v_new
    current_needed  = voltage_needed / resistance if resistance > 0 else 0
else:
    voltage_needed = 0
    current_needed = 0

if time_step > 0:
    firing_rate_estimate = 1000 / time_step   # Hz
else:
    firing_rate_estimate = 0

# ============================================================
# REPORT
# ============================================================
print("=" * 55)
print(f"{'SIMULATION RESULTS':^55}")
print("=" * 55)
print()

print("NEURON:")
print(f"  ID:           {neuron_id}")
print(f"  Type:         {neuron_type}")
print(f"  Region:       {region}")
print()

print("INPUTS:")
print(f"  Resting voltage:    {v_initial:.1f} mV")
print(f"  Threshold:          {threshold:.1f} mV")
print(f"  Resistance:         {resistance:.1f} MΩ")
print(f"  Current:            {current:.2f} nA")
print(f"  Time step:          {time_step:.1f} ms")
print()

print("RESULTS:")
print(f"  Voltage change:     {delta_v:+.2f} mV")   # + forces sign to show
print(f"  New voltage:        {v_new:.2f} mV")
print(f"  Threshold:          {threshold:.1f} mV")
print()

print("STATUS:")
if did_spike:
    print(f"  ⚡ SPIKE DETECTED")
    print(f"  Exceeded threshold by {v_new - threshold:.2f} mV")
    print(f"  Estimated firing rate: {firing_rate_estimate:.1f} Hz")
else:
    print(f"  ✗ No spike")
    print(f"  {voltage_needed:.2f} mV below threshold")
    print(f"  Need {current_needed:.3f} more nA to fire")
print()

print("INTERPRETATION:")
if v_new <= -80:
    print("  Hyperpolarized — inhibitory input dominating")
elif v_new <= -65:
    print("  Near resting potential — minimal net input")
elif v_new <= -55:
    print("  Subthreshold depolarization — excitatory input present")
else:
    print("  Threshold reached — action potential fired")

print()
print("=" * 55)
print("  Simulation complete.")
print("=" * 55)
