"""
Lecture 5.4: Sets — Unique Collections
"""

# Creating a set — notice the duplicate values
neuron_types = {"pyramidal", "interneuron", "pyramidal", "granule", "interneuron"}
print(neuron_types)  # {'pyramidal', 'interneuron', 'granule'} — duplicates gone!

# The order may vary when printed — sets are unordered
# Don't rely on any particular order

# Creating a set from an existing list — great for deduplication
spike_neurons = [1, 3, 5, 3, 7, 1, 9, 5]
unique_neurons = set(spike_neurons)
print(unique_neurons)  # {1, 3, 5, 7, 9} — each number appears once
print(f"Original list had {len(spike_neurons)} items, set has {len(unique_neurons)}")
print()

excitatory = {"N001", "N003", "N005", "N007", "N009"}
inhibitory = {"N002", "N004", "N006", "N008", "N010"}
active = {"N001", "N003", "N006", "N008", "N011"}

all_neurons = excitatory | active
print(f"All unique neurons: {all_neurons}")
# {'N001', 'N003', 'N005', 'N006', 'N007', 'N008', 'N009', 'N011'}

excitatory_and_active = excitatory & active
print(f"Excitatory AND active: {excitatory_and_active}")  # {'N001', 'N003'}

excitatory_not_active = excitatory - active
print(f"Excitatory but NOT active: {excitatory_not_active}")
# {'N005', 'N007', 'N009'} — excitatory neurons that were silent

print("N001" in excitatory)  # True
print("N002" in excitatory)  # False — N002 is inhibitory, not excitatory
print()

# Neuroscience Application: Multi-Window Activity Analysis
# Neuron IDs that fired in each time window
window1_spikes = {1, 3, 5, 7, 9, 11, 13}  # Pre-stimulus window
window2_spikes = {3, 6, 9, 12, 15, 18}  # Stimulus window
window3_spikes = {1, 5, 9, 13, 17, 21}  # Post-stimulus window

print("=== MULTI-WINDOW ACTIVITY ANALYSIS ===")

# Neurons active in ALL three windows — the most consistently firing cells
always_active = window1_spikes & window2_spikes & window3_spikes
print(f"Always active (all windows): {always_active}")  # {9}
# Neuron 9 fired in every single window — possibly a hub neuron

# Neurons active in ANY window — the total recruited population
ever_active = window1_spikes | window2_spikes | window3_spikes
print(f"Ever active (any window): {sorted(ever_active)}")
print(f"Total unique neurons recruited: {len(ever_active)}")

# Neurons active ONLY during the stimulus — the stimulus-specific response
only_during_stimulus = window2_spikes - window1_spikes - window3_spikes
print(f"Stimulus-specific neurons: {only_during_stimulus}")
# These neurons only fired when the stimulus was present

# Neurons that went SILENT during the stimulus (active before/after but not during)
went_silent = (window1_spikes | window3_spikes) - window2_spikes
print(f"Went silent during stimulus: {went_silent}")
# These neurons may be inhibited by the stimulus
