"""
Lecture 3.2: The RC Circuit Analogy
"""

# ---------------------------------------
# The Cell Membrane as a Physical Barrier

"""
A neuron is surrounded by a lipid bilayer membrane.
This membrane separates two salt solutions: the intracellular fluid
(inside the cell) and the extracellular fluid (outside).
Both solutions contain ions — mostly sodium (Na⁺),
potassium (K⁺), and chloride (Cl⁻).
Ions can only cross through specialized protein channels
embedded in the membrane.

Is exactly what defines a capacitor in electrical engineering.
A capacitor stores charge. When positive charge accumulates on one side
of the membrane (inside) and negative charge on the other (outside),
a voltage difference builds up across it. This is the membrane potential,
typically measured in millivolts.
At rest, the inside of a neuron is about 65–70 mV more negative than the outside.
We call this the resting membrane potential, typically written as V_rest ≈ −65 mV.
"""

# ------------------------
# The Membrane Capacitance

"""
It takes a certain amount of charge to change the membrane potential by 1 mV.
The capacitance is one of the parameters that sets the timescale
of the neuron’s response.
"""

# ------------------------------------------
# The Membrane Resistance (Leak Conductance)

"""
The membrane is not a perfect insulator. There are always some ion channels open at rest.
The leak channels dissipate the excess charge, much like a resistor discharging a capacitor.
With the leak, old inputs decay away, and only sufficiently recent or sufficiently strong
input drives the membrane to threshold. This gives the neuron a natural sense of recency
— a built-in forgetting.
"""

# --------------------
# The RC Circuit Model

"""
A capacitor C in parallel with a resistor R — and you have the classic RC circuit:

        I(t) [input current]
           |
     ------+------
     |            |
    [C]           [R]
  membrane      leak
  capacitance  conductance
     |            |
     ------+------
           |
         V_rest (battery = resting potential)


tau * dV/dt = -(V-V_rest) + R*I(t)

V is the membrane potential (voltage across the capacitor)
V_rest is the resting potential (the equilibrium voltage when I = 0)
  The resting potential is negative (typically −65 mV) because the inside
  of the neuron is negative relative to the outside.
R is the membrane resistance
C is the membrane capacitance
I(t) is the input current (synaptic + injected)
tau = RC is the membrane time constant.
  Neurons with short τ respond quickly but forget old inputs fast.

This is the LIF equation.

Loihi implements this RC dynamics using analog or mixed-signal circuits.
TrueNorth implements it digitally with a leaky counter.
SpiNNaker simulates it in software on embedded ARM cores.
All three are, at the end, approximating the same RC circuit.
"""
