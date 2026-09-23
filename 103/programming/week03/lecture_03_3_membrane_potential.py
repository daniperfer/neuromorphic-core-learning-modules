"""
Lecture 3.3: Membrane Potential Dynamics
"""

# ----------------------
# LIF equation revisited

"""
tau * dV/dt = -(V-V_rest) + R*I(t)

Left part:
Rate of change of the membrane potential, scaled by
the time constant. The larger τ is, the more slowly V
changes for a given imbalance between input and leak.

-(V-V_rest):
Is leak term.
negative whenever V is above rest and positive whenever V
is below rest. It always pulls V back toward V_rest.

R*I(t):
Input term:
Positive for depolarizing (excitatory) input and
negative for hyperpolarizing (inhibitory) input.
Synaptic currents, injected currents, and
noise all enter through this term.

The membrane potential changes at a rate determined by
the competition between the leak (which drags V back to rest) and
the input (which drives V away from rest).
The time constant τ sets how quickly this competition plays out.
"""

# -----------------------------------------------
# The Time Constant τ: The Neuron’s Memory Window

"""
It controls how long the neuron “remembers” its inputs.
If two synaptic inputs arrive more than ~3–5τ apart,
the second input finds the membrane essentially at rest.
If they arrive closer together than τ, their effects on the
membrane potential can add — this is temporal summation.
"""

# ----------------------------------------------------
# Subthreshold Dynamics: What Happens Before the Spike

"""
If a constant current I_0 is applied, the membrane potential rises
exponentially from V_rest toward the steady-state value
V_∞ = V_rest + R · I_0, with time constant τ.
If I_0 is large enough that V_∞ > V_th, the neuron will cross threshold and fire.

Each synaptic event produces a brief injection of current,
which causes a momentary rise in V followed by exponential decay.
If multiple EPSPs (excitatory postsynaptic potentials,
or IPSPs inhibitory for inhibitory synapses) arrive close together in time
(within a few τ), they can summate to push V over threshold
— this is temporal summation.
If EPSPs arrive at multiple synapses simultaneously,
they all contribute to V in the same timestep.
— this is spatial summation.
"""

# --------------------------------
# Inhibition and Hyperpolarization

"""
Not all synaptic inputs push V toward threshold.
In the LIF equation, inhibitory input corresponds to I(t) < 0.
"""
