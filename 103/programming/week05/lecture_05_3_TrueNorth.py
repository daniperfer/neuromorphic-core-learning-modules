"""
Lecture 5.3: IBM TrueNorth — The Ultra-Low-Power Inference Engine
"""

# ----------------------------------------------------
# The TrueNorth Architecture: Scale Through Simplicity

"""
A single chip contains 4,096 neurosynaptic cores, each simulating 256 neurons
with 256 synapses per neuron. The total: approximately 1,000,000 neurons
and 256,000,000 synapses on a chip fabricated in Samsung’s 28nm process.

To put this in perspective: TrueNorth has roughly 7.8 times more neurons and
15 times more synapses per chip than Loihi 1. It achieves this density through a
combination of simplifications, a deliberate design choice.

1) Binary weights. A synapse is on or off. The tradeoff is expressive power:
you cannot represent a “strong” connection vs. a “weak” connection
— only “connected” vs. “not connected.”

2) Simplified neuron model.
TrueNorth does not implement the full LIF dynamics with time constant τ,
refractory period, and threshold adaptation.
It uses a simplified integrate-and-fire model closer to a binary threshold unit.

3) No on-chip learning.
There is no mechanism for updating synaptic weights on the chip.
Weights are loaded once at deployment and remain fixed.
If the task changes, you retrain offline.
"""

# ---------------------------------
# The Power Efficiency of TrueNorth

"""
TrueNorth consumes approximately 70 milliwatts while running at the equivalent of
1,000 frames per second in real-time classification tasks.
(Loihi 1 consumes approximately 1 watt. A low-power GPU would consume 10–100 watts).

Event-driven computation:
In a typical vision task where inputs are sparse — most pixels are not changing,
most neurons are not firing — the vast majority of cores sit idle,
consuming near-zero dynamic power. TrueNorth was measured at roughly 26 pJ per synaptic event.
TrueNorth achieves roughly 46 billion SOPS/W in the sparse inference regime.
"""

# -----------------------------
# The Corelet Programming Model

"""
A Corelet is a reusable network component — a block of cores configured to perform a
specific computation — that can be composed with other Corelets to build larger networks.

Programming challenge unique to TrueNorth is network mapping: converting a trained spiking
neural network into a physical assignment of neurons to TrueNorth cores.

Typical workflow for deploying a model on TrueNorth is:
(1) design and train a spiking network offline, usually using a conversion pipeline that takes
a conventional deep neural network and approximates it as a spiking network with binary weights;
(2) run the TrueNorth compiler to map the network to cores;
(3) load the compiled binary onto the chip;
(4) run inference in the chip.

"""
