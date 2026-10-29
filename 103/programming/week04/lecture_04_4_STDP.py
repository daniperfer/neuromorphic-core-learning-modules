"""
Lecture 4.4: Spike-Timing-Dependent Plasticity (STDP)

Hebbian learning, as we described it in Lecture 4.2, is a rate-based rule:
it responds to average co-activity, measured over some time window.
But the brain has a more refined instrument.
Spike-timing-dependent plasticity (STDP) updates synaptic weights based on
the precise millisecond-scale timing of individual spikes.
STDP is, in this interpretation, a biological implementation of causal inference.
"""

# ------------------------
# The STDP Learning Window

"""
Weight update in STDP:
Δt = t_pre − t_post,
where t_pre is the time of the presynaptic spike and
t_post is the time of the postsynaptic spike.

For small positive Δt (pre fires shortly before post):
Δw = +A_+ · exp(−Δt / τ_+)       [Long-Term Potentiation, LTP]

For small negative Δt (pre fires shortly after post):
Δw = −A_- · exp(+Δt / τ_-)       [Long-Term Depression, LTD]

The parameters A_+ and A_- set the maximum magnitude of potentiation and depression.
The time constants τ_+ and τ_- (typically 20–50 ms) set how quickly the effect decays
as the spike timing becomes less precise. Together, these define the STDP learning window:
a curve showing how the weight change depends on the inter-spike interval.

Key features:
Assymetry:
Random, uncorrelated activity leads to net depression rather than net potentiation
Temporal locality:
the window is typically narrow, spanning only ±50 ms.
Event-drivenness:
STDP only fires when spikes occur. If a neuron is silent, its synapses do not change.
"""

# ---------------------------------
# STDP and the Event-Based Paradigm

"""
There is no global synchronization required;
each synapse operates locally and independently.

In NEUR 202, you will implement this in full detail, with thousands of
synapses learning in parallel. Here, the key point is the conceptual fit:
STDP is an inherently event-driven, locally computable learning rule.
"""

# -
# Common Mistakes To Avoid

"""
The full STDP rule must account for all spike pairs, or use an approximation.
The simple pair-based rule is a useful starting point, but it becomes incorrect
when neurons fire at high rates.
This is one reason why NEUR 202 covers more sophisticated formulations.
"""
