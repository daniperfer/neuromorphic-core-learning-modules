"""
Lecture 3.5: The f-I Curve
"""

# ------------------------------------------
# Building Intuition: Three Regimes of Input

"""
Weak input (below rheobase):
- steady state V_∞ < V_th.
- subthreshold regime.

Input at rheobase:
- V_∞ = V_th
This is the threshold current.

Strong input (above rheobase):
- Firing rate increases with input.

The f-I curve plots this relationship: it is zero
below rheobase, and increases (typically sublinearly
— the rate of increase slows at high input) above rheobase.
"""

# ----------------------
# Deriving the f-I Curve

"""
Solution to the RC charging equation starting from V_reset,
with steady-state V_∞ = V_rest + R·I:

V(t) = V_rest+ R * I * (1 – e^{-t/tau}) + (V_reset – V_rest) * e^{-t/tau}

The time to reach threshold V_th from V_reset is found
by setting V(t) = V_th and solving for t:

t_charge = tau * ln((V_∞ – V_reset)/(V_∞ – V_th))

where V_∞ = V_rest + R·I.

Total inter-spike interval (ISI) is: t_charge + τ_ref.

Firing rate is:

f = 1/( τ_ref + tau * ln((V_∞ – V_reset)/(V_∞ – V_th)) )
"""

# ---------------------------
# Properties of the f-I Curve

"""
Threshold:
The threshold current is: I_rh = (V_th – V_rest)/R
For typical values (V_th − V_rest = 15 mV, R = 10 MΩ): I_rh = 1.5 nA.

Shape:
Above threshold, f increases as I increases, but the relationship is concave.
Saturation of the f-I curve. At very high input,
f approaches its maximum: f_max = 1 / τ_ref
(when the charging time becomes negligible compared to the refractory period)

Gain:
the neuron is most sensitive to weak inputs near threshold
and less sensitive to strong inputs. This is qualitatively
similar to many perceptual systems.

Effect of parameters:
Increasing τ (longer time constant) makes the f-I curve shallower
— the neuron charges more slowly and fires at lower rates for a given input.
Decreasing R (less resistance, more leak) raises the rheobase
— you need more input to fire.
Decreasing τ_ref raises the maximum firing rate.
"""

# -------------------------------
# The f-I Curve and Neural Coding

"""
In rate coding, the neuron’s message to downstream circuits is conveyed
by its firing rate. The f-I curve tells you how that rate is set:
rate is a monotonically increasing, saturating function of input current.
"""

# ------------------------
# Common Mistakes to Avoid

"""
A mistake is forgetting that the f-I curve is defined for
constant input. Real neurons receive fluctuating, noisy input
— and their effective f-I curve in that context is different
(generally smoother, with a smaller effective threshold).

A neuron can have a shallow f-I curve but a fast τ,
or a steep f-I curve but a slow τ. These are independent properties.
"""
