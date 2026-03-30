"""
Exercise 1: Write a program that asks for a neuron's membrane voltage and prints one of four messages: 
“Hyperpolarized” (below -80 mV), 
“Resting” (-80 to -65 mV), 
“Depolarized” (-65 to -55mV), or 
“Firing” (-55 mV and above). 
Test it with at least five different voltages.
"""

"""
Exercise 2: Extend Exercise 1 to also ask for the neuron type (“Pyramidal” or “Interneuron”). 
If the neuron is firing, print whether it's sending an excitatory or inhibitory signal. 
If the type is neither, print “Unknown neuron type.”
"""
neuron_type = input("Neuron type (Pyramidal/Interneuron): ").strip().title()
voltages = [-53, -56, -62, -73, -84]
for v in voltages:
  firing = False
  signal = ""
  if v >= -55:
    voltage_state = "Firing"
    firing = True
    if neuron_type.lower() == "pyramidal":
      signal = "excitatory"
    elif neuron_type.lower() == "interneuron":
      signal = "inhibitory"
    else:
      signal = "Unknown neuron type."
  elif v >= -60:
    voltage_state = "near- threshold (highly excitable)"
  elif v >= -70:
    voltage_state = "mildly depolarized"
  elif v >= -80:
    voltage_state = "resting / slightly hyperpolarized"
  else:
    voltage_state = "strongly hyperpolarized"
  print(f"Voltage state for membrane voltage {v} mV: {voltage_state}")
  if firing:
    print(f"Signal in neuron {neuron_type} is of type: {signal}")

"""
Exercise 3: Write a program that asks for three neuron voltages (representing three connected neurons in 
a chain). Using conditionals, determine whether a signal propagates: 
Neuron 1 fires if its voltage ≥ -55 mV. 
If Neuron 1 fires, add 20 mV to Neuron 2's voltage. 
If Neuron 2's updated voltage ≥ -55 mV, add 20 mV to Neuron 3. 
Report the final state of all three neurons.
"""
voltage1 = float(input("Current membrane 1 voltage (mV): "))
voltage2 = float(input("Current membrane 2 voltage (mV): "))
voltage3 = float(input("Current membrane 3 voltage (mV): "))

if voltage1 >= -55:
  print(f"Neuron 1 is Firing")
  voltage2 += 20
else:
  print("Neuron 1 is NOT firing")

if voltage2 >= -55:
  print(f"Neuron 2 is Firing")
  voltage3 += 20
else:
  print("Neuron 2 is NOT firing")

if voltage3 >= -55:
  print(f"Neuron 3 is Firing")
else:
  print("Neuron 3 is NOT firing")
