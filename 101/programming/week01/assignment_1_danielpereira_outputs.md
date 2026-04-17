# Assignment_1 Daniel Pereira

A short document showing outputs of `assignment_1_danielpereira.py` from four test cases.

## Test Case 1

```
============================================================
               NEUROSCIENCE CALCULATOR v1.0
          Neuron Voltage Simulator
============================================================

This program models how a neuron's voltage changes
when it receives an input current.
Formula: ΔV = I × R  (Ohm's Law)

------------------------------------------------------------
Enter Neuron Parameters
------------------------------------------------------------
Enter Neuron ID: 1
Enter Neuron type (e.g., Pyramidal, Interneuron): Pyramidal
Enter initial voltage (mV): -70
Enter input current (nA): 0.8
Enter membrane resistance (MΩ): 20
Enter time step duration (ms): 10

============================================================
                  SIMULATION RESULTS
============================================================

NEURON INFORMATION:
  Neuron ID:   1
  Type:        Pyramidal

INPUT PARAMETERS:
  Initial voltage:     -70.00 mV
  Input current:       +0.80 nA
  Membrane resistance: +20.00 MΩ
  Time step:           +10.00 ms

CALCULATED RESULTS:
  Voltage change (ΔV):     +16.00 mV
  New membrane potential:  -54.00 mV
  Spike threshold:         -55.00 mV

SPIKE STATUS:
  ⚡ SPIKE DETECTED!
  The neuron fired an action potential.
  Voltage exceeded threshold by 1.00 mV

------------------------------------------------------------
BIOLOGICAL INTERPRETATION:
------------------------------------------------------------
The neuron reached threshold and fired an action potential.
The spike will propagate down the axon to downstream neurons.

============================================================
Simulation complete.
Keep exploring — one neuron at a time.
============================================================
============================================================
BONUS: Additional Calculations.
============================================================
  Firing rate 100.00 Hz
```

## Test Case 2

```
============================================================
               NEUROSCIENCE CALCULATOR v1.0
          Neuron Voltage Simulator
============================================================

This program models how a neuron's voltage changes
when it receives an input current.
Formula: ΔV = I × R  (Ohm's Law)

------------------------------------------------------------
Enter Neuron Parameters
------------------------------------------------------------
Enter Neuron ID: 2
Enter Neuron type (e.g., Pyramidal, Interneuron): Pyramidal
Enter initial voltage (mV): -70
Enter input current (nA): 0.3
Enter membrane resistance (MΩ): 20
Enter time step duration (ms): 20

============================================================
                  SIMULATION RESULTS
============================================================

NEURON INFORMATION:
  Neuron ID:   2
  Type:        Pyramidal

INPUT PARAMETERS:
  Initial voltage:     -70.00 mV
  Input current:       +0.30 nA
  Membrane resistance: +20.00 MΩ
  Time step:           +20.00 ms

CALCULATED RESULTS:
  Voltage change (ΔV):     +6.00 mV
  New membrane potential:  -64.00 mV
  Spike threshold:         -55.00 mV

SPIKE STATUS:
  ✗ No spike.
  Voltage is 9.00 mV below threshold.
  Would need 0.45 more nA to reach threshold.

------------------------------------------------------------
BIOLOGICAL INTERPRETATION:
------------------------------------------------------------
The neuron is depolarized but has not yet reached threshold.
It's receiving excitatory input but not enough to fire.

============================================================
Simulation complete.
Keep exploring — one neuron at a time.
============================================================

============================================================
BONUS: Additional Calculations.
============================================================
  Firing rate 50.00 Hz
```

## Test Case 3

```
============================================================
               NEUROSCIENCE CALCULATOR v1.0
          Neuron Voltage Simulator
============================================================

This program models how a neuron's voltage changes
when it receives an input current.
Formula: ΔV = I × R  (Ohm's Law)

------------------------------------------------------------
Enter Neuron Parameters
------------------------------------------------------------
Enter Neuron ID: 3
Enter Neuron type (e.g., Pyramidal, Interneuron): Pyramidal
Enter initial voltage (mV): -70
Enter input current (nA): -0.5
Enter membrane resistance (MΩ): 20
Enter time step duration (ms): 15

============================================================
                  SIMULATION RESULTS
============================================================

NEURON INFORMATION:
  Neuron ID:   3
  Type:        Pyramidal

INPUT PARAMETERS:
  Initial voltage:     -70.00 mV
  Input current:       -0.50 nA
  Membrane resistance: +20.00 MΩ
  Time step:           +15.00 ms

CALCULATED RESULTS:
  Voltage change (ΔV):     -10.00 mV
  New membrane potential:  -80.00 mV
  Spike threshold:         -55.00 mV

SPIKE STATUS:
  ✗ No spike.
  Voltage is 25.00 mV below threshold.
  Would need 1.25 more nA to reach threshold.

------------------------------------------------------------
BIOLOGICAL INTERPRETATION:
------------------------------------------------------------
The neuron is hyperpolarized — more negative than resting.
Inhibitory inputs (or open K⁺ channels) are suppressing activity.

============================================================
Simulation complete.
Keep exploring — one neuron at a time.
============================================================

============================================================
BONUS: Additional Calculations.
============================================================
  Firing rate 66.67 Hz
```

## Test Case 4

```
============================================================
               NEUROSCIENCE CALCULATOR v1.0
          Neuron Voltage Simulator
============================================================

This program models how a neuron's voltage changes
when it receives an input current.
Formula: ΔV = I × R  (Ohm's Law)

------------------------------------------------------------
Enter Neuron Parameters
------------------------------------------------------------
Enter Neuron ID: 4
Enter Neuron type (e.g., Pyramidal, Interneuron): Pyramidal
Enter initial voltage (mV): -70
Enter input current (nA): 0.75
Enter membrane resistance (MΩ): 20
Enter time step duration (ms): 10

============================================================
                  SIMULATION RESULTS
============================================================

NEURON INFORMATION:
  Neuron ID:   4
  Type:        Pyramidal

INPUT PARAMETERS:
  Initial voltage:     -70.00 mV
  Input current:       +0.75 nA
  Membrane resistance: +20.00 MΩ
  Time step:           +10.00 ms

CALCULATED RESULTS:
  Voltage change (ΔV):     +15.00 mV
  New membrane potential:  -55.00 mV
  Spike threshold:         -55.00 mV

SPIKE STATUS:
  ⚡ SPIKE DETECTED!
  The neuron fired an action potential.
  Voltage exceeded threshold by 0.00 mV

------------------------------------------------------------
BIOLOGICAL INTERPRETATION:
------------------------------------------------------------
The neuron reached threshold and fired an action potential.
The spike will propagate down the axon to downstream neurons.

============================================================
Simulation complete.
Keep exploring — one neuron at a time.
============================================================

============================================================
BONUS: Additional Calculations.
============================================================
  Firing rate 100.00 Hz
```
