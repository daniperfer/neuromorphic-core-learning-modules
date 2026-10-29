"""
Lecture 4.3: The Hopfield Network as Content-Addressable Memory

The capacity to retrieve a complete memory from a partial or noisy cue
is called content-addressable memory, and it is one of the most useful
and biologically realistic things a neural network can do.

The Hopfield network is the simplest model of content-addressable memory,
it is built in the weight matrix using the outer product rule.
That matrix is storing patterns as attractors — stable states that the network settles
into when given a sufficiently similar starting point.
Corrupted or partial inputs fall into the basin of attraction
of the nearest stored pattern, and the network fills in the missing pieces.
"""

# ----------------------------------------------
# Attractors: What the Network Is Actually Doing

"""
In a Hopfield network, all neurons are interconnected
with symmetric weights (w_{ij} = w_{ji}) and no self-connections.
Each neuron takes one of two states: +1 (active) or −1 (inactive).
The network is updated by computing, for each neuron i:

h_i = Σ_j w_ij · s_j
s_i → sign(h_i)

where s is the current state vector and h_i is the total input to neuron i.
If the input is positive, the neuron becomes active; if negative, it becomes inactive.

What makes this network special is that it has an energy function:

E = -(1/2) · Σ_{ij} w_ij · s_i · s_j

Each update step can only decrease (or maintain) the energy — never increase it.
This means the network always flows downhill in energy space, eventually stopping
at a local minimum: the attractors.
The Hebbian learning rule is designed precisely so that
the stored patterns p₁, p₂, … become low-energy states — local minima.
"""

# ------------------------------------------
# Capacity: How Many Patterns Can Be Stored?

"""
The Hopfield network has a capacity limit.
Storing too many patterns causes them to interfere with each other.
P_max ≈ 0.14 · N
For a network of N = 100 neurons, you can reliably store about 14 patterns.
Spurious attractors multiply.

Modern variants — including modern Hopfield networks or Dense Associative Memories —
achieve exponentially higher capacity by using
higher-order interactions instead of pairwise weights.

A network model derived from first principles using the outer product rule
turns out to describe the function of
an actual brain region: hippocampus CA3 subfield region.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Students also sometimes conflate the attractors of the Hopfield network
with the stored patterns. They are not the same.
The attractors include the stored patterns, but also spurious states
— combinations of stored patterns that are accidentally stable.
Understanding the difference matters for understanding
retrieval errors and why the capacity limit exists.
"""
