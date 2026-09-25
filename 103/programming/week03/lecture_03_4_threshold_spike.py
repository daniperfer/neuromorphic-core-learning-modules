"""
Lecture 3.4: Threshold, Spike, and Reset
"""

"""
The transition from continuous subthreshold dynamics
to discrete spike output is the most important event in the LIF model.
It is the moment where analog computation becomes digital communication.
"""

# -------------------
# The Spike Threshold

"""
The LIF model fires a spike when the membrane potential V
reaches the spike threshold V_th (about 15–25 mV above the
resting potential). The neuron fires reliably
when input is strong enough and doesn’t fire when it isn’t.
This 15–25 mV gap is crucial: it’s wide enough that
small random fluctuations in V don’t trigger spurious spikes,
but narrow enough that moderate synaptic input can
reliably drive the neuron to fire.
"""

# -------------------------
# The Spike: All-or-nothing

"""
All of the neuron’s output information is encoded in
the times at which spikes occur — the spike train.
By ignoring the waveform and recording only the timing,
the LIF model captures all of the information while
discarding all of the expensive computation
(“delta spike” convention).
"""

# ---------
# The Reset

"""
Immediately after a spike, the membrane potential is reset
to a fixed value V_reset, which is typically
slightly below V_rest or equal to it
(this corresponds to the hyperpolarization
that follows the action potential).
"""

# ---------------------
# The Refractory Period

"""
After the reset, the neuron enters a refractory period
during which it cannot fire another spike.
Biologically, this corresponds to two distinct mechanisms:
- absolute refractory period (typically 1–2 ms in cortical neurons)
- relative refractory period (typically 5–15 ms following the a.r.p.)
In LIF model, After a spike and reset, V is held fixed at
V_reset for a duration τ_ref before it is allowed to evolve again.
Even with very strong input, the effective maximum rate is substantially
below 1/τ_ref because of the charging time. The stronger the input
(the higher V_∞), the shorter the charging time.
"""
