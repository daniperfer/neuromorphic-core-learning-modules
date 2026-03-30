"""
Neural State Classifier
Determines the functional state of a neuron based on membrane voltage, firing
history, and neuron type.
"""

# Collect neuron data
print("=" * 55)
print(f"{'NEURAL STATE CLASSIFIER':^55}")
print("=" * 55)
print()
neuron_id = int(input("Neuron ID: "))
neuron_type = input("Neuron type (Pyramidal/Interneuron/Purkinje): ").strip().title()
voltage = float(input("Current membrane voltage (mV): "))
spike_count = int(input("Spikes in last 100 ms: "))
refractory = input("In refractory period? (yes/no): ").strip().lower() == "yes"
print()

# ── Classify voltage state ──────────────────────────────────
if voltage >= -55:
  voltage_state = "firing threshold reached"
elif voltage >= -60:
  voltage_state = "near- threshold (highly excitable)"
elif voltage >= -70:
  voltage_state = "mildly depolarized"
elif voltage >= -80:
  voltage_state = "resting / slightly hyperpolarized"
else:
  voltage_state = "strongly hyperpolarized"

# ── Classify activity level ─────────────────────────────────
if spike_count == 0:
  activity = "silent"
elif spike_count <= 3:
  activity = "low activity"
elif spike_count <= 10:
  activity = "moderate activity"
elif spike_count <= 25:
  activity = "high activity"
else:
  activity = "bursting"

# ── Determine output type ────────────────────────────────────
if neuron_type == "Interneuron":
  output_type = "inhibitory"
elif neuron_type in ("Pyramidal", "Purkinje"):
  output_type = "excitatory"
else:
  output_type = "unknown"

# ── Can the neuron fire right now? ──────────────────────────
can_fire = (voltage >= -55) and (not refractory)

# ── Build the report ────────────────────────────────────────
print("=" * 55)
print(f" Neuron {neuron_id} — {neuron_type}")
print("=" * 55)
print()
print(f" Voltage state: {voltage_state}")
print(f" Activity level: {activity} ({spike_count} spikes / 100 ms)")
print(f" Output type: {output_type}")
print(f" Refractory: {'Yes — cannot fire' if refractory else 'No'}")
print()

if can_fire:
  print(" ⚡ STATUS: FIRING")
  print(" Action potential conditions met.")
elif voltage >= -55 and refractory: 
  print(" ⏳ STATUS: THRESHOLD REACHED BUT REFRACTORY")
  print(" Neuron will fire again once refractory period ends.")
elif voltage >= -60:
  print(" ⚠️ STATUS: NEAR THRESHOLD")
  print(" Small additional input could trigger a spike.")
else:
  needed = -55 - voltage
  print(f" 💤 STATUS: SUBTHRESHOLD")
  print(f" Needs {needed:.1f} mV more depolarization to fire.")

print()
print("=" * 55)
