"""
Lecture 7.2: Array Operations
"""

import numpy as np

voltages = np.array([-70.0, -65.0, -60.0, -55.0, -50.0])

print(voltages + 10)  # [-60. -55. -50. -45. -40.]  ← shift baseline by 10 mV
print(voltages * 1000)  # convert mV to μV — multiply every value by 1000
print(voltages**2)  # square all values
print(np.abs(voltages))  # [ 70.  65.  60.  55.  50.]  ← absolute value of each
print()

# Spike counts across 5 time bins for two neurons
neuron_A = np.array([15, 23, 8, 31, 19])
neuron_B = np.array([12, 27, 10, 28, 22])

# How many total spikes in each bin across both neurons?
total = neuron_A + neuron_B
print(f"Total spikes per bin: {total}")

# Which neuron was more active in each bin?
diff = neuron_A - neuron_B
print(f"Difference (A minus B): {diff}")

# What fraction of spikes did neuron A contribute?
ratio = neuron_A / neuron_B
print(f"Ratio A/B: {ratio}")

# Dot product — a measure of how similarly two neurons respond
dot_product = np.dot(neuron_A, neuron_B)
print(f"Dot product: {dot_product}")
print()


# UFUNCS

voltages = np.array([-70.0, -65.0, -60.0, -55.0, -50.0])

# Square root (of absolute values, since voltages are negative)
print(np.sqrt(np.abs(voltages)))

# Exponential — useful for decay curves and time constants
print(np.exp(voltages / 100))

# Natural log
print(np.log(np.abs(voltages)))


def sigmoid(x):
    """
    Sigmoid converts any input into a value between 0 and 1,
    which is how many neural network models represent a neuron’s firing probability
    """
    return 1 / (1 + np.exp(-x))


inputs = np.linspace(-5, 5, 100)  # 100 evenly spaced input values
outputs = sigmoid(inputs)

print(f"Sigmoid range: {outputs.min():.3f} to {outputs.max():.3f}")
# Sigmoid range: 0.007 to 0.993
print()


# This is vectorized thinking in practice: no loops, no manual iteration, just
# operations on whole arrays that read almost like
# the mathematical description of the phenomenon itself.
def simulate_action_potential(t):
    """
    We’ll simulate the voltage trace of an action potential — the rapid rise and
    fall that occurs when a neuron fires — using nothing but array math.
    """
    V_rest = -70.0  # resting membrane potential (mV)
    V_peak = 40.0  # peak depolarization (mV)

    # Rising phase: Gaussian peak centered at 0.5 ms
    rising = V_peak * np.exp(-((t - 0.5) ** 2) / 0.1)

    # Falling phase: hyperpolarization centered at 1.5 ms
    falling = -20 * np.exp(-((t - 1.5) ** 2) / 0.2)

    voltage = V_rest + rising + falling
    return voltage


# Time axis: 0 to 5 ms, sampled at 500 points
t = np.linspace(0, 5, 500)
voltage = simulate_action_potential(t)

print(f"Resting potential: {voltage[0]:.1f} mV")
print(f"Peak voltage:      {voltage.max():.1f} mV")
print(f"Time of peak:      {t[voltage.argmax()]:.2f} ms")
print(f"Duration above threshold (-55 mV): {np.sum(voltage > -55) * 0.01:.2f} ms")
print()
