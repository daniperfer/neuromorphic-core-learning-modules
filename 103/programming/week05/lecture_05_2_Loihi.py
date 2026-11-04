"""
Lecture 5.2: Intel Loihi — Architecture and On-Chip Learning
"""

# ---------------------------------------
# The Neurocore: Loihi’s Fundamental Unit

"""
A neurocore as a small, specialized processor that does exactly one thing:
simulate LIF neurons and route spikes.
Loihi 1 contains 128 neuromorphic cores per chip.
Each core simulates approximately 1,024 LIF neurons, giving roughly 128,000 neurons per chip.
Each neurocore (Loihi 1) also holds a local synaptic memory of up to 131,072 synapses,
which stores the incoming connection weights for the neurons on that core.

The most important architectural feature is that synaptic memory is
co-located with computation.
Each neurocore holds its own synaptic memory. When a spike arrives at a core,
the weight lookup and the state update happen locally, without any off-chip memory access.
This is compute-in-memory, realized in hardware.

Each neurocore maintains the state variables:
- the membrane potential V,
- the synaptic current u,
- and the refractory counter.

The neurocore in Loihi 2 (2021) can execute custom neuron update rules defined by the user.
"""

# -------------------------------------------
# The Mesh Network-on-Chip: How Spikes Travel

"""
Loihi handles spike delivery with a mesh network-on-chip (NoC):
a grid of routers connecting all 128 cores,
with each router passing packets to its neighbors.
Each spike is represented as a small packet containing the address of the source neuron.
The NoC routes this packet through the mesh grid to every destination core that
has a synapse connected to that source. When the packet arrives at a destination core,
the core looks up the synapse weight and updates the target neuron’s state.
This is an event-driven, asynchronous communication paradigm.
Loihi chips can also be connected to one another via off-chip links,
forming multi-chip configurations.
"""

# ----------------------------------
# On-Chip STDP: Learning in Hardware

"""
Each synapse stores not just the weight w but also two trace variables:
x_pre (tracking presynaptic activity), and
x_post (tracking postsynaptic activity).
When a presynaptic spike arrives, x_pre is incremented and decays exponentially with τ_pre.
When a postsynaptic neuron fires, x_post is incremented and decays with τ_post.

The weight update follows:

Δw = η_+ · x_pre (when postsynaptic spike occurs — LTP)
Δw = η_- · x_post (when presynaptic spike occurs — LTD)

This is exactly the learning window you studied in Lecture 4.4:
pre-before-post strengthens the synapse (LTP), post-before-pre weakens it (LTD).
Loihi executes this rule locally on each neurocore.
Loihi 1 implements the learning rule in hardware with 9-bit integer weights.
Loihi 2 adds greater programmability, allowing users to define custom update functions.
"""

# ------------------------
# The x86 Management Cores

"""
Each Loihi 1 chip also contains 3 embedded x86 processors that serve as host management cores.
The x86 cores are not part of the neuromorphic computation — they are the
system’s administrative layer, needeed to interface with conventional software infrastructure.
"""

# --------------------------------------------------------
# Worked Example: Mapping the Fly Visual System to Loihi 1

"""
The bottleneck is often synapses, not neurons. A biologically realistic network
with high connectivity can exhaust synaptic memory before it exhausts neuron capacity.
The neuromorphic compiler (the software that maps your network to hardware) must solve
this packing problem — assigning neurons to cores so that each core’s synaptic budget is not
exceeded while keeping related neurons physically close to minimize spike routing distance.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Loihi 1 consumes approximately 1 watt at full operation — impressive compared to a GPU,
but not nothing. This figure assumes moderate activity; power scales with spike rate,
just as biological energy consumption scales with neural firing rates.
A Loihi chip running at 100% spike rate is not operating in its power-efficient regime.
The efficiency advantage of neuromorphic hardware emerges under sparse activity,
which is the regime that natural sensory signals typically fall in.
"""
