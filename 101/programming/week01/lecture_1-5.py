"""
Exercise 1: Write a program that asks the user for a neuron’s spike count and recording duration in seconds, 
then calculates and displays the firing rate in Hz and the average inter-spike interval in milliseconds.
"""

"""
Exercise 2: Extend Exercise 1 to also ask for the neuron’s type and brain region. 
Display a formatted report that includes all inputs and all calculated values. 
Use f-strings with appropriate decimal formatting throughout.
"""

"""
Exercise 3: Add a try/except block to Exercise 1 so that if the user types something that isn’t a number, 
the program prints a helpful message and exits gracefully instead of crashing. 
Test it by typing "hello" when prompted for the spike count.
"""

 # DEFAULTS
spike_count_default = 10
duration_s_def = 0.1

print("INPUTS:")

while True:
    try:
        spike_count_raw = input(f"Spike count [default {spike_count_default})]: ")
        spike_count = float(spike_count_raw) if spike_count_raw else spike_count_default
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue
    if spike_count <= 0:
        print("Invalid range. The input number must be greater than 0, like 10 or 40")
        continue
    break   # Input was valid — exit the loop
print(f"Spike count set to {spike_count}")

while True:
    try:
        duration_s_raw = input(f"Interval duration (in seconds)[default {duration_s_def}]: ")
        duration_s = float(duration_s_raw) if duration_s_raw else duration_s_def
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue
    if duration_s <= 0:
        print("Invalid range. The input number must be greater than 0")
        continue
    break   # Input was valid — exit the loop
print(f"Interval duration set to {duration_s}")

firing_rate_hz = spike_count / duration_s
inter_spike_ms = duration_s * 1000 / spike_count

print("more INPUTs:")

neuron_type_default = "Pyramidal"
region_default = "Hippocampus"

neuron_type_raw = input("  Neuron type [default Pyramidal]: ").strip().title()
neuron_type = neuron_type_raw if neuron_type_raw else neuron_type_default
print(f"Neuron type set to {neuron_type}")

region_raw = input("  Brain region [default Hippocampus]: ").strip().title()
region = region_raw if region_raw else region_default
print(f"Brain region set to {region}")

print()
print("-" * 55)
print("RESULTS:")
print("-" * 55)
print("NEURON:")
print(f"  Type:         {neuron_type}")
print(f"  Region:       {region}")
print()
print(f"  Firing rate:                   {firing_rate_hz:+.2f} Hz")
print(f"  Avg. inter-spike interval:     {inter_spike_ms:+.2f} ms")
