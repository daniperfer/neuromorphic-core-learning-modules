"""
Lecture 3.6: LIF Variations — Conductance-Based, Adaptive, and Exponential
"""

# -----------------------------------------------------------------------
# Conductance-Based LIF (also called Current-Based vs. Conductance-Based)

"""
The basic LIF model we’ve been studying is technically a current-based LIF.
This is a simplification.
The conductance-based LIF (also called the “conductance-based point neuron”
or COBA model) incorporates this more accurate synaptic model:

tau dV/dt = -(V – V_rest) – g_E(t)(V – E_E) – g_I(t)(V – E_I)

The critical difference from the current-based model: the synaptic current depends on V.
"""

# ---------------------------------------------------------------
# Adaptive LIF (AdLIF or Adaptive Exponential Integrate-and-Fire)

"""
Many real neurons display spike-rate adaptation:
when driven by a constant input, they fire rapidly at first and
then gradually slow down over tens to hundreds of milliseconds.

tau dV/dt = -(V – V_rest) + R I(t) – R  w

Here w is the adaptation current: it increases by Δ_w after each spike
and then decays exponentially with time constant τ_w.
Spike-rate adaptation is computationally important because it makes
neurons sensitive to changes in input rather than to sustained input.
"""

# ---------------------------------------------
# Exponential Integrate-and-Fire (EIF and AdEx)

"""
The basic LIF model has a sharp threshold: the membrane evolves smoothly
until V = V_th, then a spike is declared.
Real neurons don’t have a sharp threshold.

The exponential integrate-and-fire (EIF) model adds an exponential
term to capture this:

tau dV/dt = -(V – V_rest) + Delta_T exp((V – V_T)(Delta_T}) + R I(t)

The exponential term becomes significant only
when V approaches V_T (the “softthreshold”).

The adaptive exponential integrate-and-fire (AdEx) model combines
the EIF exponential term with the adaptation current from the adaptive LIF.
"""

# The choice is always about the right tool for the specific problem.
