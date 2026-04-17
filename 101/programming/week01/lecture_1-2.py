# Neuron Firing Rate Calculator

print("=" * 50)
print("NEURON FIRING RATE CALCULATOR")
print("=" * 50)
print()

# Store our data in variables
num_spikes = 100
time_seconds = 5

# Calculate firing rate
firing_rate = num_spikes / time_seconds

# Display results
print("Number of spikes:", num_spikes)
print("Time period:", time_seconds, "seconds")
print("Firing rate:", firing_rate, "Hz")
print()
print("This neuron is moderately active.")
print("Typical cortical neurons fire at 1-20 Hz.")

total_neurons = 86e9
average_firing_rate = 5
total_spikes_second = total_neurons * average_firing_rate

print("\nTotal spikes per second:", total_spikes_second)