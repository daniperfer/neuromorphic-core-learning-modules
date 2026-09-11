"""
Lecture 2.6: Event-Based Computing as a Paradigm Shift
"""

# --------------------------------------------------------------------
# Three Assumptions of Frame-Based Computing (and Event-Based Doesn’t)

"""
1: Time is uniform and discrete.
2: All spatial locations are equally informative.
3: Computation and sensing are separate stages.
"""

# ------------------------------------
# The Von Neumann Bottleneck Revisited

"""
Neuromorphic hardware implements compute-in-memory — synaptic
weights are stored physically close to the neurons that use them,
so the “distance” between memory and computation is minimized.
"""

# ------------------------------
# Where This Paradigm Is Heading

"""
Edge AI:
Event-based neuromorphic systems are among the few architectures
that can deliver real-time inference at milliwatt power levels.
Autonomous systems:
The latency advantages of event-based sensing are directly relevant
to these applications.
Brain-machine interfaces:
The input in this case is literally a stream of spikes.
Scientific understanding of the brain:
Neuromorphic systems serve as computational models of neural circuits.


A frame-based system computes a dense representation of the world at each moment.
An event-based system computes a sparse representation of what changed in the world.
These are different answers to a different question.
"""
