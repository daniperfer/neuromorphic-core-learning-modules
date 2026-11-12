"""
Lecture 5.5: BrainChip Akida and the Commercial Neuromorphic Landscape

Loihi, TrueNorth, and SpiNNaker were each designed primarily to advance the science.
Akida was designed to ship in products.
"""

# ---------------------------------
# BrainChip and the Akida Processor

"""
(Akida 2.0) — targets edge AI deployment in automotive, industrial IoT, medical devices,
and smart home applications. It is a production chip, available for purchase, designed
to be integrated on a PCB and shipped in a product.

Akida 1.0 key specifications:
Up to 1.2 million neurons and 10 billion synapses (configurable, not fixed)
Supports convolutional, fully-connected, and recurrent spiking layers
On-chip learning via a few-shot STDP variant
Power: approximately 25–30 mW for inference at the edge
Process: TSMC 28nm

Akida 2.0 improvements:
Hybrid processing: spiking and non-spiking layers can coexist in the same network
Support for transformer-style attention in event-driven mode
Improved CNN-to-SNN conversion pipeline
Automotive-grade qualification process (AEC-Q100)

The hybrid architecture in Akida 2.0 acknowledges that the path to mainstream deployment is
to build hardware that can run today’s conventional models while also supporting
spiking computation where it provides an advantage.
"""

# -------------------------
# On-Chip Few-Shot Learning

"""
Akida supports on-chip learning. BrainChip implements few-shot learning on-chip:
the chip can learn to recognize new classes from as few as one to five examples.
"""

# ------------------------------------------
# The MetaTF Toolchain: Lowering the Barrier

"""
BrainChip provides MetaTF — a conversion pipeline from TensorFlow/Keras models to
Akida-compatible spiking networks.
MetaTF assumes the user has deep learning knowledge and wants to get to neuromorphic hardware
as painlessly as possible. The tradeoff is that MetaTF-converted networks are not designed
with spiking in mind from the ground up — they are approximations of conventional networks,
not native spiking architectures. This limits some of the potential efficiency gains,
but dramatically lowers the barrier to entry.
"""

# --------------------------------
# The Broader Commercial Landscape

"""
SynSense (formerly aiCTX),
a Swiss startup, produces the Xylo chip — an event-driven processor targeting audio and biosignal
processing at sub-milliwatt power, designed specifically for always-on keyword detection.
More power-constrained than Akida, more narrowly scoped.

Innatera Nanosystems,
a Dutch startup, builds analog neuromorphic processors for biosignal applications (EEG, EMG, ECG).
Their approach uses analog circuits — closer to Carver Mead’s original vision — rather than
digital approximations, achieving extreme power efficiency in a narrow domain.

GrAI Matter Labs,
a French startup, produces the GrAI One chip with a neuromorphic-inspired
sparse event-driven architecture targeting general edge inference.

What these commercial efforts share is a focus on the edge deployment scenario
— always-on, power-constrained, low-latency sensing —
rather than the large-scale simulation use case that SpiNNaker serves.
The commercial bet is that the economic opportunity in neuromorphic computing lies in
replacing power-hungry edge MCUs and small GPUs in sensing applications.

You can purchase the Akida chip, integrate it on a custom PCB, and ship the drone to a customer.
With Loihi, you would need an INRC research partnership to access hardware
— viable for a university lab, but not for a company shipping a commercial product.
"""

# ------------------------
# Common Mistakes to Avoid

"""
It is tempting to read the breadth of the commercial landscape
— BrainChip, SynSense, Innatera, GrAI Matter Labs —
as a sign that neuromorphic computing has arrived. It has not yet.
Most of these companies are small, deployments are early-stage,
and the killer application that drives mass adoption has not yet clearly emerged.
The landscape is promising and moving fast. It is still early.
"""
