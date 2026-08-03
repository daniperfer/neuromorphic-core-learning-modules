"""
Lecture 7.7: NumPy Best Practices

This lecture covers three practices that separate beginner NumPy usage from
 professional-grade code:
 replacing loops with vectorized logic,
 choosing data types that fit your data,
 and saving arrays in formats that preserve precision and load fast.
"""

import time

import numpy as np

voltages = np.random.uniform(-80, -40, 100_000)  # 100,000 voltage samples

# Slow approach: loop through every element individually
start = time.time()
result_loop = []
for v in voltages:
    if v > -55:
        result_loop.append(v * 1000)  # above threshold: convert to μV
    else:
        result_loop.append(v)  # below threshold: leave as mV
loop_time = time.time() - start

# Fast approach: np.where applies the condition across the entire array at once
start = time.time()
result_vec = np.where(voltages > -55, voltages * 1000, voltages)
vec_time = time.time() - start

print(f"Loop time:       {loop_time:.4f}s")
print(f"Vectorized time: {vec_time:.4f}s")
print(f"Speedup:         {loop_time / vec_time:.0f}x faster!")
print()


# Three arrays of one million elements each, with different dtypes
voltages_64 = np.zeros(1_000_000, dtype=np.float64)  # default
voltages_32 = np.zeros(1_000_000, dtype=np.float32)  # half the precision, half the memory
spike_counts = np.zeros(1_000_000, dtype=np.int16)  # integers 0–65535, 2 bytes each

print(f"float64:  {voltages_64.nbytes / 1e6:.1f} MB")  # 8.0 MB
print(f"float32:  {voltages_32.nbytes / 1e6:.1f} MB")  # 4.0 MB
print(f"int16:    {spike_counts.nbytes / 1e6:.1f} MB")  # 2.0 MB
"""
A practical guide for neuroscience data:

float64 — use when you need maximum precision:
computed statistics, filtered signals, any value where small numerical errors could
accumulate across many operations.

float32 — use for raw voltage traces and continuous signals.
Modern recording hardware typically has 16-bit precision,
so float32 already exceeds it.
You get half the memory footprint with no meaningful loss of accuracy.

int16 — use for spike counts, trial indices, and other small integer values.
It can store values from -32,768 to 32,767, which covers every realistic spike count per bin.

bool — use for masks and binary conditions
(spike/no-spike, above-threshold/below-threshold). Each element takes 1 byte.
"""
# Set dtype on creation
voltage_trace = np.zeros(500_000, dtype=np.float32)

# Convert an existing array
precise_stats = voltage_trace.astype(np.float64)  # upcast for computation
print()

# Saving and loading numpy arrays
spike_matrix = np.random.poisson(10, (100, 1000))  # 100 neurons, 1000 time bins

# Save
np.save("spike_data.npy", spike_matrix)

# Load — shape, dtype, and values all preserved exactly
loaded = np.load("spike_data.npy")
print(f"Loaded shape: {loaded.shape}")  # (100, 1000)
print(f"Data matches: {np.array_equal(spike_matrix, loaded)}")  # True

# Save multiple arrays under named keys
np.savez(
    "experiment.npz",
    spikes=spike_matrix,
    timestamps=np.arange(1000) * 0.001,  # time axis in seconds
    neuron_ids=np.arange(100),
)

# Load and access by name
data = np.load("experiment.npz")
print(f"Available arrays: {list(data.keys())}")  # ['spikes', 'timestamps', 'neuron_ids']
print(f"Spikes shape: {data['spikes'].shape}")  # (100, 1000)

# Save as CSV — fmt="%d" means format as integers (no decimal points)
np.savetxt("spike_data.csv", spike_matrix, delimiter=",", fmt="%d")

# Load back — note: always comes back as float64, even if saved as integers
loaded_csv = np.loadtxt("spike_data.csv", delimiter=",")
print(f"CSV shape: {loaded_csv.shape}")  # (100, 1000)
"""
The practical recommendation: use .npy or .npz for your working data —
they’re fast and lossless.
Use .csv only when you need to share with tools outside Python.
"""
print()
