"""
Lecture 1.5: Neural Codes — How Spikes Carry Information
"""

# -------------------------------
# Rate Coding: The Classical View

"""
To estimate a firing rate reliably, you need enough spikes to count.
At 100 spikes per second, a 10 ms window gives you only 1 spike
— not enough for a reliable rate estimate.
Reliable rate estimation typically requires 50–100 ms windows.
But many biological behaviors happen in 100–200 ms total
(a tennis return, a catching reflex, a spoken syllable).
If rate coding requires 50–100 ms just to read the code,
how can the brain react fast enough?

This tension drove neuroscientists to look for faster coding strategies.
"""

# --------------------------------------
# Temporal Coding: Timing Is the Message

"""
Temporal coding is more information-dense than rate coding:
a single spike can carry far more than one bit of information
if its precise timing is meaningful. But it requires precise synaptic transmission
and tight coordination — and it is more vulnerable to noise.
A few milliseconds of jitter in spike timing can corrupt a temporal code.

For neuromorphic hardware, temporal coding is attractive because
it is fast (information is in the first spike) and sparse
(you only need one spike per neuron per stimulus, rather than many).
Intel’s Loihi supports spike timing at 1-millisecond resolution specifically
to enable temporal coding experiments.
"""

# --------------------------------------
# Population Coding: Strength in Numbers

"""
The population vector method (computing the weighted sum of preferred directions)
is a specific decoding algorithm for this kind of distributed representation.

Population coding is robust: if one neuron dies or goes silent,
the rest of the population still carries the information.
It is also precise: a population of neurons with overlapping tuning curves
can collectively encode a stimulus value more finely than
any single neuron’s tuning width would suggest.
"""

# ----------------------------------------------
# Sparse Coding: The Brain’s Efficiency Strategy

"""
A particularly important variant of population coding is sparse coding:
the idea that at any given moment, only a small fraction of neurons in a population are active.
Most neurons are silent; information is carried by the pattern of which few neurons fire.
This is directly relevant to neuromorphic hardware.
Event-based chips consume power approximately in proportion to spike rate.
A sparse neural code — where most neurons rarely fire
— means most of the chip is idle most of the time, consuming minimal power.
The efficiency of neuromorphic computing depends critically on exploiting sparsity.
"""

# ------------------------
# Common mistakes to avoid

"""
The most persistent mistake is treating rate coding and temporal coding as
competing theories where one must be right and the other wrong.
In reality, the brain likely uses different codes in different regions for different purposes.

Students also sometimes assume that sparse coding is always better. Sparsity has real costs.
The brain trades off sparsity against coverage depending on
the computational demands of each region.

Do not confuse population coding with redundancy.
In a population code, each neuron carries unique information.
Redundancy exists too (many neurons with similar preferred stimuli add robustness),
but it is different from the combinatorial power of a true population.
"""
