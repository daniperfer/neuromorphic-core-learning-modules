"""
Lecture 1.2: Von Neumann vs. the Brain
"""

# ----------------------------
# The Von Neumann Architecture

"""
The critical feature — and the critical weakness — is that computation and memory are separate.
Data is shuttling back and forth constantly.
Modern CPUs spend a substantial fraction of their time waiting for data
that is stuck in the pipeline between CPU and RAM. The computation unit is idle,
burning power, doing nothing.

Data movement, not computation, dominates energy consumption.
"""

"""
In the brain,

1) computation and memory are co-located at every synapse.
A synapse does two things simultaneously: it transmits a signal (computation)
and it stores a weight (memory).

2) The second architectural difference is parallelism. A conventional CPU executes
one instruction at a time (or a small handful with superscalar execution).
The brain executes billions of operations simultaneously.

3) The third difference is event-driven vs. clock-driven operation.
A CPU is clocked — it does something on every tick of a global clock,
whether or not there is meaningful work to do. Neurons are event-driven
— they only consume energy when they fire. In a sparse neural code
(which the brain typically uses), most neurons are silent most of the time.
The idle ones cost almost nothing.
"""

"""
Neuromorphic chips are most promising for sparse, event-driven,
low-power inference — things like always-on sensors, edge AI,
and robotic control. The two paradigms will likely coexist for decades.
"""
