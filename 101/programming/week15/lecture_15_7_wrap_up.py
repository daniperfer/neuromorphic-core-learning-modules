"""
Lecture 15.7: Course Wrap-up — What You’ve Built and What Comes Next
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

# ---------------------------------------
# What the Course Did Not Cover — and Why

"""
Synaptic plasticity.
The Brian2 simulations you built use fixed synaptic weights — they do not change as the simulation runs.
Real synapses are plastic: their strengths change based on the activity of the pre- and postsynaptic
neurons. Spike-timing-dependent plasticity (STDP), the most widely studied form of Hebbian plasticity,
can be implemented in Brian2 by adding a learning rule to the Synapses object. STDP is the natural next
Brian2 topic after NEUR 101.

Network learning. Your networks do not learn. They run with fixed parameters and fixed weights.
Training a spiking neural network to perform a task — recognizing a pattern in input spike trains,
for example — requires either surrogate gradient methods (as in snnTorch) or online learning rules
like STDP. This is an active research area at the boundary of computational neuroscience and
machine learning.
"""

# -------------------------------
# What Comes Next: A Personal Map

"""
If the neuromorphic hardware connection in Lecture 15.6 excited you the most, your next step is
NEUR 103, which goes directly into neuromorphic chip design and the programming models for
Intel Loihi and related hardware.

If the machine learning connection excited you the most, the snnTorch documentation and tutorials
are a good starting point — they assume PyTorch familiarity, which can be acquired independently
— and NEUR 102’s linear algebra foundations are also directly relevant.
"""
