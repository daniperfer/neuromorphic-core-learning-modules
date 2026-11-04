"""
Lecture 5.4: SpiNNaker — The Million-Core Simulator

SpiNNaker — the Spiking Neural Network Architecture — was designed
at the University of Manchester with a single primary goal:
simulate large, biologically realistic spiking neural networks for neuroscience research.
It is trying to be the most flexible chip.
"""

# ------------------------------------------------
# The ARM-Core Architecture: Flexibility by Design

"""
Each SpiNNaker chip (in SpiNNaker 1) contains 18 ARM968 cores.
Each ARM core is responsible for simulating approximately
1,000 neurons in software (timestep is 1ms).
On SpiNNaker, the neuron model is a C function running on an ARM core.
You can implement LIF, Hodgkin-Huxley, Izhikevich, AdEx,
or any other model you can express in code.
This flexibility comes at a cost: energy efficiency.
"""

# ---------------------------------
# Scale: The Full SpiNNaker Machine

"""
A single SpiNNaker chip has 18 ARM cores × ~1,000 neurons each =
roughly 18,000 simulated neurons per chip.
The full SpiNNaker 1 machine contains approximately 500,000 to 1,000,000 ARM cores
spread across roughly 55,000 chips — the scale of a mouse brain, or about 1% of a human brain.
"""

# --------------------------------------------
# Spike Routing: Packets Over a Custom Network

"""
SpiNNaker handles this with a packet-switched communication network
— a custom router on each chip that routes small spike packets between cores.
Each spike is a packet. The packet contains the address of the source neuron
(encoded as a multicast key). The SpiNNaker router looks up the destination list
for that key and forwards copies of the packet to all destinations.
This is a hardware multicast: one spike can be delivered to thousands
of downstream neurons in a single routing operation.
SpiNNaker’s routing network operates asynchronously.
"""

# ------------------------------------
# SpiNNaker 2: Adding On-Chip Learning

"""
SpiNNaker 2, developed at TU Dresden and released as a research platform starting
around 2022–2023, addresses this. It uses more powerful ARM Cortex-M4 cores with
hardware multiply-accumulate units, improving energy efficiency.
More importantly, it adds dedicated hardware support for on-chip plasticity
— the Cortex-M4’s DSP extensions enable fast synaptic weight updates,
making real-time STDP practical on SpiNNaker for the first time.
"""
