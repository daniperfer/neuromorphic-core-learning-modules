"""
Week 1 Capstone: Multi-Neuron Analysis Report
Demonstrates: variables, data types, math, strings,
              f-strings, input, booleans, conditionals

Analyzes five neurons from a 60-second recording session
and produces a formatted lab report.
"""

import math

# ── Constants ────────────────────────────────────────────────
# These values don't change during the program.
# Defining them at the top as named constants means:
# (a) they're easy to find and change later
# (b) the rest of the code is self-documenting
RECORDING_TIME_DEF  = 60       # seconds

THRESHOLD       = -55.0    # mV — action potential threshold
RESTING         = -70.0    # mV — typical resting potential
RECORDING_TIME  = RECORDING_TIME_DEF       # seconds
SEPARATOR       = "=" * 60
SUBSEPARATOR    = "-" * 60

"""
Exercise 2: The current program always uses 60 seconds as the recording duration. 
Modify it to ask the user for the recording duration at the start using input(), 
and use that value in all calculations.
"""
while True:
    try:
        recording_time_raw = input(f"RECORDING_TIME [default {RECORDING_TIME_DEF})]: ")
        RECORDING_TIME = float(recording_time_raw) if recording_time_raw else RECORDING_TIME_DEF
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue
    if RECORDING_TIME <= 0:
        print("Invalid range. The input number must be greater than 0")
        continue
    break   # Input was valid — exit the loop
print(f"RECORDING_TIME set to {RECORDING_TIME}")

# ── Neuron Data ──────────────────────────────────────────────
# In a real program this would come from a data file.
# For now we define it directly. Each block is one neuron.

# Neuron 1
n1_id         = 1
n1_type       = "Pyramidal"
n1_region     = "Prefrontal Cortex"
n1_voltage    = -52.3    # mV
n1_spikes     = 187      # spikes in 60 seconds
n1_refractory = False

# Neuron 2
n2_id         = 2
n2_type       = "Interneuron"
n2_region     = "Prefrontal Cortex"
n2_voltage    = -61.8
n2_spikes     = 412
n2_refractory = False

# Neuron 3
n3_id         = 3
n3_type       = "Pyramidal"
n3_region     = "Hippocampus"
n3_voltage    = -70.1
n3_spikes     = 23
n3_refractory = False

# Neuron 4
n4_id         = 4
n4_type       = "Purkinje"
n4_region     = "Cerebellum"
n4_voltage    = -67.4
n4_spikes     = 0
n4_refractory = True

# Neuron 5
n5_id         = 5
n5_type       = "Interneuron"
n5_region     = "Hippocampus"
n5_voltage    = -83.2
n5_spikes     = 61
n5_refractory = False

"""
Exercise 1: Add a sixth neuron to the program — a Granule cell from the cerebellum 
with voltage -68.2 mV, 94 spikes, not in refractory. 
Update the summary statistics to include it.
"""
# Neuron 6
n6_id         = 6
n6_type       = "Granule"
n6_region     = "cerebellum"
n6_voltage    = -68.2
n6_spikes     = 94
n6_refractory = False

"""
Exercise 3: Add a new classification to classify_activity() that 
identifies “Pathological” activity — a firing rate above 100 Hz. 
Print a warning message in the neuron report if this threshold is exceeded.
"""
def classify_activity(spikes, duration):
    """
    Returns an activity label based on spike count and recording duration.
    spikes   — number of spikes recorded
    duration — recording duration in seconds
    """
    rate = spikes / duration if duration > 0 else 0

    if spikes <= 0:
        return "Silent"
    elif rate < 1:
        return "Very Low"
    elif rate < 5:
        return "Low"
    elif rate < 15:
        return "Moderate"
    elif rate < 40:
        return "High"
    elif rate > 100:
        return "Pathological"
    else:
        return "Bursting"


def voltage_state(voltage):
    """Returns a descriptive label for the neuron's voltage state."""
    if voltage >= THRESHOLD:
        return "At/Above Threshold"
    elif voltage >= -60:
        return "Depolarized (subthreshold)"
    elif voltage >= -75:
        return "Near Resting"
    else:
        return "Hyperpolarized"

"""
Exercise 4 (Challenge): Modify print_neuron_report() to also calculate and display 
the coefficient of variation of the ISI — a measure of firing regularity. 
For simplicity, assume CV = 0.1 for rates below 5 Hz and CV = 0.8 for rates above 5 Hz. 
Print “Regular firing” for CV < 0.3 and “Irregular firing” for CV ≥ 0.3.
"""
def print_neuron_report(nid, ntype, region, voltage, spikes, refractory):
    """Prints a formatted analysis report for one neuron."""

    # ── Calculations ─────────────────────────────────────────
    firing_rate = spikes / RECORDING_TIME
    # Inter-Spike Interval: avg. time between spikes
    isi_ms      = (1000 / firing_rate) if firing_rate > 0 else float('inf')
    to_threshold = THRESHOLD - voltage
    activity    = classify_activity(spikes, RECORDING_TIME)
    v_state     = voltage_state(voltage)
    can_fire    = (voltage >= THRESHOLD) and (not refractory)
    cv_isi      = 0.1 if firing_rate < 5 else 0.8

    # Output type based on neuron type
    if ntype == "Interneuron":
        output = "Inhibitory"
    elif ntype in ("Pyramidal", "Purkinje", "Granule"):
        output = "Excitatory"
    else:
        output = "Unknown"

    # ── Report ───────────────────────────────────────────────
    print(SUBSEPARATOR)
    print(f"  NEURON {nid}: {ntype.upper()} — {region}")
    print(SUBSEPARATOR)

    print(f"  Voltage:          {voltage:.1f} mV  ({v_state})")
    print(f"  To threshold:     {to_threshold:+.1f} mV")
    print(f"  Refractory:       {'Yes' if refractory else 'No'}")
    print()
    print(f"  Spikes recorded:  {spikes:,}") # Add comma separators for large numbers
    print(f"  Firing rate:      {firing_rate:.2f} Hz")

    if firing_rate > 0:
        print(f"  Avg ISI:          {isi_ms:.1f} ms")
    else:
        print(f"  Avg ISI:          N/A (silent)")
    
    # coefficient of variation of the ISI
    if cv_isi < 0.3:
        print(f"  Regular firing:   CV {cv_isi}")
    else:
        print(f"  Irregular firing: CV {cv_isi}")

    print(f"  Activity level:   {activity}")
    if activity == "Pathological":
      print(f"  ⚠️  ACTIVITY: Pathological!!!")
    print(f"  Output type:      {output}")
    print()

    # Status
    if can_fire:
        print(f"  ⚡ STATUS: FIRING — action potential conditions met")
    elif refractory and voltage >= THRESHOLD:
        print(f"  ⏳ STATUS: REFRACTORY — will fire when period ends")
    elif voltage >= -60:
        print(f"  ⚠️  STATUS: NEAR THRESHOLD — {to_threshold:+.1f} mV to fire")
    else:
        print(f"  💤 STATUS: SUBTHRESHOLD — {to_threshold:+.1f} mV to threshold")

    print()
    return firing_rate   # Return rate so we can use it in the summary


# ── Header ───────────────────────────────────────────────────
print(SEPARATOR)
print(f"{'MULTI-NEURON ANALYSIS REPORT':^60}")
print(f"{'NEUR 101 — Week 1 Capstone':^60}")
print(SEPARATOR)
print()
print(f"  Recording duration:  {RECORDING_TIME} seconds")
print(f"  Spike threshold:     {THRESHOLD} mV")
print(f"  Neurons analyzed:    6")
print(f"  Regions covered:     Prefrontal Cortex, Hippocampus, Cerebellum")
print()

# ── Neuron Reports ───────────────────────────────────────────
print(SEPARATOR)
print(f"{'INDIVIDUAL NEURON ANALYSIS':^60}")
print(SEPARATOR)
print()

rate1 = print_neuron_report(n1_id, n1_type, n1_region, n1_voltage, n1_spikes, n1_refractory)
rate2 = print_neuron_report(n2_id, n2_type, n2_region, n2_voltage, n2_spikes, n2_refractory)
rate3 = print_neuron_report(n3_id, n3_type, n3_region, n3_voltage, n3_spikes, n3_refractory)
rate4 = print_neuron_report(n4_id, n4_type, n4_region, n4_voltage, n4_spikes, n4_refractory)
rate5 = print_neuron_report(n5_id, n5_type, n5_region, n5_voltage, n5_spikes, n5_refractory)
rate6 = print_neuron_report(n6_id, n6_type, n6_region, n6_voltage, n6_spikes, n6_refractory)

# ── Summary Statistics ───────────────────────────────────────
total_spikes  = n1_spikes + n2_spikes + n3_spikes + n4_spikes + n5_spikes + n6_spikes
avg_rate      = (rate1 + rate2 + rate3 + rate4 + rate5 + rate6) / 5
silent_count  = sum([1 for s in [n1_spikes, n2_spikes, n3_spikes, n4_spikes, n5_spikes, n6_spikes] if s == 0])
active_count  = 5 - silent_count

most_active_rate = max(rate1, rate2, rate3, rate4, rate5, rate6)

print(SEPARATOR)
print(f"{'SESSION SUMMARY':^60}")
print(SEPARATOR)
print()
print(f"  Total spikes recorded:   {total_spikes:,}")
print(f"  Average firing rate:     {avg_rate:.2f} Hz")
print(f"  Active neurons:          {active_count} / 5")
print(f"  Silent neurons:          {silent_count} / 5")
print(f"  Highest firing rate:     {most_active_rate:.2f} Hz")
print()

# Overall network assessment
if avg_rate > 20:
    network_state = "highly active — possible seizure-like activity"
elif avg_rate > 8:
    network_state = "moderately active — normal task engagement"
elif avg_rate > 2:
    network_state = "low activity — resting state or light anesthesia"
else:
    network_state = "near-silent — deep anesthesia or inhibition"

print(f"  Network state:  {network_state.upper()}")
print()
print(SEPARATOR)
print(f"{'END OF REPORT':^60}")
print(SEPARATOR)
