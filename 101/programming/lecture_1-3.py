#Problem 1: A neuron fires 80 spikes in 4 seconds. 
# Calculate its firing rate in Hz and its average inter-spike interval in milliseconds.

total_spikes = 80
total_time_s = 4
firing_rate_hz = total_spikes / total_time_s
print(f'firing_rate_hz {firing_rate_hz}')
avg_spike_time_ms = total_time_s * 1000 / total_spikes
print(f'avg_spike_time_ms = {avg_spike_time_ms}')

#Problem 2: A current of 0.8 nA flows through a membrane with resistance 15 MΩ. 
# The neuron starts at resting potential (-70 mV). 
# What is the new membrane potential? 
# Does it reach threshold at -55 mV?

membrane_resistance_ohm = 15e6
current_A = 0.8e-9
V_rest = -70e-3

# Ohm's law: voltage change = current × resistance
delta_V = current_A * membrane_resistance_ohm
V_new = V_rest + delta_V

threshold = -55e-3
if V_new >= threshold:
    print("⚡ Threshold reached — neuron fires!")
else:
    needed = threshold - V_new
    print(f"{V_new} Below threshold. Need {needed} more V to fire.")

#Problem 3: An unmyelinated axon conducts at 1.2 m/s. A myelinated axon conducts at 80 m/s. 
# If both need to transmit a signal across a 500 mm nerve, how much time does each take (in milliseconds)? 
# How many times faster is the myelinated axon?
unmyelinated_speed_m_s = 1.2
myelinated_m_s = 80
nerve_length = 500e-3
time_unmyelinated = nerve_length / unmyelinated_speed_m_s
time_myelinated = nerve_length / myelinated_m_s

print(f"myelinated is {time_unmyelinated / time_myelinated} times faster.")