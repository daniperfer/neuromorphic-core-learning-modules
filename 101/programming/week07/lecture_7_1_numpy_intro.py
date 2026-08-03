"""
Lecture 7.1: Introduction to NumPy
"""

import time

import numpy as np

# A Python list of membrane voltages (millivolts)
voltages_list = [-70.0, -65.0, -60.0, -55.0, -50.0]

# The same data as a NumPy array
voltages_array = np.array([-70.0, -65.0, -60.0, -55.0, -50.0])

print(type(voltages_list))  # <class 'list'>
print(type(voltages_array))  # <class 'numpy.ndarray'>
print(voltages_array.dtype)  # float64  ← all values are 64-bit floats
print(voltages_array.shape)  # (5,)     ← 5 elements, 1 dimension
print()

n = 1_000_000  # one million values

python_list = list(range(n))
numpy_array = np.arange(n)

# Python list: multiply every element by 2
start = time.time()
result = [x * 2 for x in python_list]
python_time = time.time() - start

# NumPy array: multiply every element by 2
start = time.time()
result = numpy_array * 2
numpy_time = time.time() - start

print(f"Python list: {python_time:.3f} seconds")
print(f"NumPy array: {numpy_time:.3f} seconds")
print(f"NumPy is {python_time / numpy_time:.3f}x faster!")
print()

# Initialize 100 membrane potentials at resting state
# np.zeros and np.ones are standard ways to set up arrays before filling them
resting_potentials = np.zeros(100) - 70.0
print(resting_potentials[:5])  # [-70. -70. -70. -70. -70.]

# A 3x3 synaptic weight matrix, all starting at 1.0
weights = np.ones((3, 3))

# Time axis for a 1-second recording at 1 kHz (1 sample per millisecond)
# np.arange works like range() but produces an array
time_points = np.arange(0, 1.0, 0.001)
print(f"Samples in 1-second recording: {len(time_points)}")  # 1000

# 50 evenly spaced frequency values from 1 to 100 Hz
# np.linspace is preferred when you know how many points you want
frequencies = np.linspace(1, 100, 50)
print(frequencies[:5])  # [  1.     3.04   5.08   7.12   9.16]

# Simulated membrane voltages drawn from a realistic range
random_voltages = np.random.uniform(-80, -40, 1000)

# Simulated inter-spike intervals using an exponential distribution
# (real neurons' ISIs follow approximately this distribution)
spike_intervals = np.random.exponential(scale=50, size=100)  # mean ISI of 50ms
print()
