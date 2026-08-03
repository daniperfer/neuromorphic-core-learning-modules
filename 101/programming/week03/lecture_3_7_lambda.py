"""
Lecture 3.7: Lambda Functions — Small Tools for Quick Jobs
"""


# Regular function
def square(x):
    """Regular function"""
    return x * x


# Lambda — identical behavior, one line
square_lambda = lambda x: x * x  # noqa: E731

print(square(5))  # 25
print(square_lambda(5))  # 25

# Where Lambdas Shine: Sorting, Filtering, and Mapping

# Neurons as (id, voltage) tuples
neurons = [(1, -65.0), (2, -70.0), (3, -55.0), (4, -60.0)]
# Sort by voltage (the second element of each tuple)
sorted_neurons = sorted(neurons, key=lambda n: n[1])
print(sorted_neurons)

voltages = [-70, -65, -60, -55, -50, -45, -75, -80]
# Keep only voltages at or above the firing threshold
above_threshold = list(filter(lambda v: v >= -55, voltages))
print(above_threshold)
# Equivalent, and arguably more readable
above_threshold = [v for v in voltages if v >= -55]
print(above_threshold)

spike_counts = [5, 10, 15, 20]
# Convert spike counts to firing rates (10-second recording)
rates = list(map(lambda s: s / 10, spike_counts))
print(rates)

# Lambda version — technically works, but hard to read
process = lambda v: v + 10 if v > -60 else v - 5 if v < -70 else v  # noqa: E731
print(process(-59))
print(process(-71))
print(process(-65))


# Proper function — what this should be
def adjust_voltage(v):
    """
    Apply a voltage correction based on the current range.
    Above -60 mV: add 10 (compensate for electrode artifact)
    Below -70 mV: subtract 5 (baseline correction)
    Otherwise: leave unchanged
    """
    if v > -60:
        return v + 10
    elif v < -70:
        return v - 5
    else:
        return v
