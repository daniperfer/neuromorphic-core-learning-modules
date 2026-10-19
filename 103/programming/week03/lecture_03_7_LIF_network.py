"""
Lecture 3.7: Networks of LIF Neurons
"""

# -------------------------------
# From One Neuron to a Population

"""
I_i(t) = I_{ext,i}(t) + SUMATORY( w_ij * s_j(t))

where:

I_i(t) is the total input current to neuron i at time t
I_{ext,i}(t) is external input to neuron i
w_{ij} is the synaptic weight from neuron j to neuron i
  (positive for excitatory, negative for inhibitory)
s_j(t) is the synaptic activation from neuron j
  (a filtered version of neuron j's spike train)

The weight matrix W with entries w_{ij} is the synaptic
connectivity matrix of the network.
"""

# ---------------------------------
# Excitatory and Inhibitory Neurons

"""
In a real cortical network, approximately
80% of neurons are excitatory (predominantly pyramidal cells)
and 20% are inhibitory (interneurons, predominantly GABAergic).
In the LIF formalism, this means the weight matrix W has
a mixed sign structure: most entries are zero (sparse connectivity),
excitatory connections are positive,
and inhibitory connections are negative. The network’s dynamics
depend critically on the balance between excitation and inhibition.
"""

# -----------------------------
# Excitatory-Inhibitory Balance

"""
Asynchronous irregular activity:
In a balanced network, neurons fire at low rates (5–20 Hz)
with irregular spike timing (high inter-spike interval variability).
High sensitivity to input:
a small increase in input can rapidly drive a large change in firing rate.
Fast dynamics:
balanced networks can track rapidly changing inputs.
Sparse coding:
the sparsity observed in cortex and exactly what makes neuromorphic systems
energy-efficient. The 1–5% active fraction we discussed in Week 2 Lecture 2.4
is maintained by E/I balance.
"""

# -----------------------------------------
# Recurrent Connectivity and Network Memory

"""
Recurrent connections allow a network to maintain activity over time
even after the input has ended — a form of working memory.
This is believed to be the neural basis of
short-term memory in prefrontal cortex.

The spectral analysis learned in NEUR 102 (eigenvalues, stability)
is the mathematical language for analyzing recurrent LIF networks.
"""

# -------------------------------------------------------
# Oscillations: When E/I Balance Breaks Down Periodically


"""
Oscillatory networks can implement
temporal coding (the phase of a spike relative to
the network oscillation carries information),
phase-locking (a form of synchrony detection),
and sequence generation (motor pattern generators).
These applications are the focus of NEUR 202: Learning in SNNs.
"""

# --------------------------------
# Preview of NEUR 201 and NEUR 104

"""
In NEUR 201: Spiking Neural Networks I, you will build networks of
thousands of LIF neurons, implement STDP learning rules,
and study how these networks can compute with spikes at scale.

NEUR 104: Calculus for Neural Dynamics develops exactly these tools,
with the membrane potential as the running example throughout.
The LIF equation τ dV/dt = -(V – V_rest) + R·I
is a first-order linear ODE.
NEUR 104 will give you the machinery to solve it analytically.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Deep learning weights are typically real-valued and
can be large or small without constraint.
Spiking network weights have signs that are
biologically constrained (a neuron is either excitatory or inhibitory
— it cannot switch, a rule called Dale’s law).
Deep learning activations are continuous;
spiking network activations are binary spike events.

E/I Balance means equal amounts of excitatory and inhibitory current,
on average, at each neuron.
With 80% excitatory neurons and 20% inhibitory neurons,
balance is maintained because inhibitory neurons compensate
with stronger synaptic weights.

In NEUR 202: Learning in SNNs, you’ll implement learning rules
that update the weight matrix in response to network activity.
The weight matrix is not a static blueprint;
it is a dynamic record of everything the network has learned.
"""
