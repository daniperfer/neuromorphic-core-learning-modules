"""
Exercise 1: You receive a neuron label from a data file: " INTERNEURON_TYPE_2 ". 
Write code that cleans it to read "Interneuron Type 2" — stripped of spaces, 
with underscores replaced by spaces, and properly capitalized.
"""
neuron_label = " INTERNEURON_TYPE_2 "
print(f"Input: {neuron_label}")
output = neuron_label.strip()
output = output.split("_")
output = [f"{o.title()} " for o in output]
final = ""
for o in output:
  final += o
print(f"Output: {final}")

"""
Exercise 2: Create an f-string that produces this output from the variables below:
Neuron 15 (Purkinje) fired 89 spikes in 20.0 seconds — rate: 4.45 Hz
Variables: neuron_id = 15, neuron_type = "Purkinje", spikes = 89, duration = 20.0
"""
neuron_id = 15
neuron_type = "Purkinje"
spikes = 89
duration = 20.0
print(f"\nNeuron {neuron_id} ({neuron_type}) fired {spikes} in {duration} seconds - rate: {spikes/duration} Hz")

"""
Exercise 3: Given the string data = "14.2,23.7,8.9,31.4,19.0" representing spike times, 
use .split() to separate it into a list, 
then print the number of spikes and the first and last spike time.
"""
data = "14.2,23.7,8.9,31.4,19.0"
spikes_list = data.split(",")
print(f"\nNumber of spikes: {len(spikes_list)}")
print(f"First: {spikes_list[0]}")
print(f"Last: {spikes_list[-1]}")