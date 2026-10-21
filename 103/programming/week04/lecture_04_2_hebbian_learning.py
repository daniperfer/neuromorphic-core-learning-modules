"""
Lecture 4.2: Hebbian Learning and the Outer Product Rule
"""

# ----------------------------
# The Hebb Postulate, Formally

"""
Δw_ij = η · x_i · x_j

The rule rewards correlated activity and ignores uncorrelated activity.
This rule is sometimes stated as “neurons that fire together, wire together”.
"""

# -----------------------------------------------------
# The Matrix Form: Hebbian Learning Across a Population

"""
Now consider an entire weight matrix W governing connections among
a population of N neurons. If the network presents
an activity pattern p — a vector in ℝᴺ each component is activity of one neuron:

ΔW = η · p · pᵀ
This is the outer product of p with itself. (matmul operation @ in python)
The (i,j) entry of the outer product is exactly p_i · p_j
— the product of the activities of neurons i and j
— which is precisely the Hebbian update Δw_{ij} = η · x_i · x_j.

If the network experiences a sequence of patterns p₁, p₂, p₃, …,
the accumulated weight matrix is:

W = (η/N) · Σ_μ p_μ · p_μᵀ

where the sum runs over all patterns the network has seen.
"""

# ----------------------------------------
# The Limitations of Pure Hebbian Learning

"""
Nothing in Δw prevents weights from growing without bound.

The brain addresses this with several mechanisms.

1. Normalization constraints limit the total
synaptic weight a neuron can receive.

2. Forgetting terms (also called weight decay) add a
negative factor proportional to the current weight,
so that rarely-used synapses drift toward zero.

3. Competitive learning forces neurons to specialize: when one neuron
wins the competition to represent a pattern,
its weights strengthen while others weaken.

4 Homeostatic scaling: the neuron monitors its own average firing rate
and adjusts all its incoming synaptic weights
up or down to keep activity in a target range
(a thermostat for neural activity).
"""

# ------------------------
# Common Mistakes to Avoid

"""
Hebbian learning is not supervised. It is a local, unsupervised rule:
the weight update at each synapse depends only on the activity of
the two neurons that synapse connects, with no global information
about network performance.
"""
