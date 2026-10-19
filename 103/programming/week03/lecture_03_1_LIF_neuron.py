"""
Lecture 3.1: Why the LIF Model?
"""

# -----------------------------------------------
# The Modeling Hierarchy: From Biology to Silicon

"""
A biological neuron is extraordinarily complex. To capture all of this
faithfully, you’d need a model with thousands of variables and parameters.
Such models exist. They’re called multi-compartment conductance-based models.
But they’re computationally brutal.
For the purposes of network-level computation, you don’t need all of that detail.
What you need is a model that captures the 4 properties below:

1. How a neuron accumulates input over time
2. How it forgets old inputs (the “leak”)
3. When it fires (the threshold)
4. What happens after it fires (reset and refractoriness)

LIF are mathematically and computationally tractable and capture the essential
computational properties of biological neurons.
"""

# ------------------------------------------------------------
# Worked Example: Comparing the Cost of LIF vs. Hodgkin-Huxley

"""
With LIF neurons:
Each neuron requires evaluating one differential equation per timestep.
Roughly 5 arithmetic operations per neuron per timestep.
For 1,000 neurons at 1,000 timesteps per second: 5 million arithmetic operations per second.
A simple microcontroller can handle this.

With Hodgkin-Huxley neurons:
The HH model requires evaluating 4 coupled ODEs and roughly 12 exponential functions
per neuron per timestep.
Roughly 100–200 arithmetic operations per neuron per timestep — conservatively.
That's 100–200 million operations per second for 1,000 neurons at 1,000 timesteps.
You’ve now crossed into the territory of a GPU or dedicated silicon accelerator.
"""

# ------------------------
# Common Mistakes to avoid

"""
The “spike” in a LIF simulation is an event, not a waveform.
The information is in the timing.
The LIF model is the sweet spot between realism and tractability.
"""
