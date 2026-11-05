"""
Lecture 5.6: Four Philosophies — Comparing Loihi, TrueNorth, SpiNNaker, and Akida
"""

# ------------------
# The Four Arguments

"""
Intel Loihi’s argument:
The most important thing neuromorphic hardware can do that GPUs cannot is
learn on-chip, in real time, without communicating with an external server.
The architecture should therefore be organized around on-chip STDP,
with LIF neuron models (programmable in Loihi 2) that support local learning rules.
Access through the INRC research program is acceptable because the primary audience
is researchers advancing the science.

IBM TrueNorth’s argument:
The most important thing neuromorphic hardware can do is run continuously
in power-constrained environments — on batteries, at the edge, in always-on sensing applications.
The architecture should therefore be optimized above everything else for
minimum energy per synaptic operation, accepting binary weights
and no on-chip learning as the price. Research access is sufficient because TrueNorth’s target
application profile never required a commercial product line.

SpiNNaker’s argument:
The most important thing neuromorphic hardware can do is simulate large,
biologically faithful neural circuits at real-time scale, so neuroscientists can test
hypotheses about how the brain works. The architecture should therefore be maximally flexible
— software-defined neuron models, arbitrary connectivity, massive scale —
accepting lower efficiency and multi-chip requirements as the price.
A university research machine is exactly the right form factor.

BrainChip Akida’s argument: The most important thing neuromorphic hardware can do right now
is exist as a purchasable product that engineers can integrate into real devices.
The architecture should bridge spiking and conventional computation (hybrid mode),
support on-chip learning for field adaptation, and come with a toolchain accessible
to engineers who already know TensorFlow, not just neuromorphic researchers.
Commercial availability is not a side feature — it is the entire point.
"""

# --------------------
# The Comparison Table

"""
Commercial availability: only Akida Brainchip.
On-chip learning: is expensive in hardware area and power.
Neuron model: TrueNorth’s and Loihi’s LIF are both fixed in hardware — fast and efficient,
but constrained to what the hardware designers chose. SpiNNaker’s software-defined models
are the most flexible but least efficient. Akida’s hybrid mode.
"""

# -----------------------------------------------------
# Decision Framework: Which Platform for Which Problem?

"""
Comparison does not hace a winner. The “best” neuromorphic platform is always relative
to a specific application:

Neuroscience research --> SpiNNaker.
Task is fixed and power is the dominant constraint --> TrueNorth.
On-chip adaptation is required and the deployment context is a research lab --> Loihi 2.
The requirement is a deployed product --> Akida.
"""

# ------------------------------------------------------------
# Worked Example: The Fly Optic Lobe Across All Four Platforms

"""
Bringing together the sizing calculations from Lectures 5.2–5.5,
here is a unified comparison of how a 60,000-neuron fly optic lobe model maps to each platform.

|===========================================================================================|
| Platform    |	Chips needed | Chip utilization |	On-chip learning | Commercially available |
|===========================================================================================|
| Loihi 1     |	1 chip       |	~47% of neurons	| Yes (STDP)       | No                     |
| TrueNorth   |	1 chip       |	~6% of neurons	| No	             | No                     |
| SpiNNaker 1 |	4 chips      |	~83% per chip	  | No (SpiNNaker 1) | No                     |
| Akida 1.0   |	1 chip       |	~5% of capacity	| Yes (few-shot)   | ✅ Yes                 |
|===========================================================================================|

The four we have studied in depth were chosen because they best illustrate the design space.
The broader ecosystem is richer and growing.
"""
