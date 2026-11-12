"""
Lecture 5.8: Power, Scale, and the Neuromorphic Promise
"""

# ---------------------------------------------------------
# The Primary Comparison: Neuromorphic vs. GPU vs. Edge MCU

"""
GPUs
are the dominant platform for deep learning training and for dense neural network
inference at scale. Thousands of multiply-accumulate units running in parallel on
large, regular data. But GPUs are energy-hungry. GPUs are also fundamentally synchronous
— they process dense batches of data in lock-step,
which is poorly matched to sparse, event-driven data streams.

Edge MCUs (microcontrollers, like ARM Cortex-M series)
are used for always-on inference in ultra-low-power applications.
They consume milliwatts to tens of milliwatts, but they are slow.

Neuromorphic chips sit between these poles for many applications,
and above both poles in specific regimes.
"""

# ---------------------------------
# Where Neuromorphic Currently Wins

"""
Sparse, event-driven sensory processing.
When the input data is itself event-driven.

Always-on, low-power sensing.
Applications like always-on keyword spotting, thermal anomaly detection,
and patient monitoring in implantable devices require exactly this profile.

Online adaptation in non-stationary environments.
The ability to update weights locally and in real time is a genuine capability
advantage over inference-only platforms.
"""

# ----------------------------------
# Where Neuromorphic Currently Loses

"""
Dense matrix operations. Large language models, vision transformers, and convolutional
networks with many large feature maps are dominated by dense matrix multiplications.

Well-optimized GPU workloads. For tasks where GPU-based deep learning already achieves
high accuracy with reasonable efficiency — image classification on dense cameras,
natural language processing, protein structure prediction.

Software ecosystem maturity. The toolchains for Loihi, TrueNorth, and SpiNNaker are
specialized, require chip access (often through research programs),
and have smaller communities than PyTorch or TensorFlow.
"""

# ----------------------
# The Key Metric: SOPS/W

"""
The standard figure of merit for neuromorphic efficiency is
synaptic operations per second per watt (SOPS/W)
— how many synaptic update events the chip can process per joule of energy consumed.
TrueNorth: 10¹² to 10¹³ SOPS/W for sparse spiking workloads.
Loihi: 10¹¹ SOPS/W.
SpiNNaker: 10⁸ to 10⁹ SOPS/W.
A conventional GPU running equivalent sparse spiking simulations achieves roughly 10⁷ SOPS/W.

Neuromorphic is more efficient than GPUs for sparse, event-driven computation,
which is the regime that many real sensory processing tasks fall in.
"""

# ----------------------------------------------
# What Needs to Happen for Neuromorphic to Scale

"""
The neuromorphic field faces several challenges before it can reach
mainstream deployment beyond specialized applications.

Training algorithms for SNNs.
Backpropagation does not work naturally on spiking networks.
Current approaches (surrogate gradient methods, spike-compatible learning rules,
ANN-to-SNN conversion pipelines) are improving but have not yet matched the performance
and ease-of-use of standard deep learning training.

Hardware-software co-design.
The next generation of neuromorphic hardware will likely be designed in close
collaboration with the software frameworks and algorithms that run on it.

Standardization.
The fragmentation of the neuromorphic programming landscape
(Lava, PyNN, Corelet, Brian2-to-hardware pipelines) raises the barrier to adoption.
Convergence on standard interfaces — similar to what PyTorch represents for
GPU-based deep learning — would significantly lower that barrier.

Application-specific design.
The next wave of neuromorphic devices may not be general-purpose research chips
but application-specific chips designed for particular classes of problems.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Neuromorphic hardware should be evaluated on the problems it is designed for:
always-on sensing, event-based vision, online adaptation.
"""
