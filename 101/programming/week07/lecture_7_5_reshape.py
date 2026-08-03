"""
Lecture 7.5: Reshaping and Stacking Arrays
"""

import numpy as np

data = np.arange(12)  # [0 1 2 3 4 5 6 7 8 9 10 11]
print(f"Original shape: {data.shape}")  # (12,)

# Rearrange into 3 rows x 4 columns
reshaped = data.reshape(3, 4)
print(f"Reshaped:\n{reshaped}")
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Flatten back to 1D
flat = reshaped.flatten()
print(f"Flattened: {flat}")  # [ 0  1  2  3  4  5  6  7  8  9 10 11]
print()
data = np.arange(12)
reshaped = data.reshape(3, -1)  # NumPy figures out: 12 / 3 = 4 columns
print(reshaped.shape)  # (3, 4)
print()

# A raw EEG recording: 4000 consecutive samples
# (4 channels recorded at 1000 samples/second for 1 second, interleaved)
raw_eeg = np.random.randn(4000)
print(f"Raw shape:    {raw_eeg.shape}")  # (4000,)

# Reorganize into 4 channels x 1000 time points
eeg_matrix = raw_eeg.reshape(4, 1000)
print(f"Matrix shape: {eeg_matrix.shape}")  # (4, 1000)

# Now each row is a channel — easy to work with
channel_0 = eeg_matrix[0, :]  # All 1000 time points for channel 0
mean_per_channel = np.mean(eeg_matrix, axis=1)
print(f"Mean per channel: {mean_per_channel}")
print()

# Spike counts across 5 time bins — two recording sessions
session1 = np.array([15, 23, 8, 31, 19])
session2 = np.array([18, 20, 11, 28, 22])

# Stack vertically: each session becomes a row
combined = np.vstack([session1, session2])
print(f"Stacked:\n{combined}")
# [[15 23  8 31 19]
#  [18 20 11 28 22]]
print(f"Shape: {combined.shape}")  # (2, 5)

h_combined = np.hstack([session1, session2])
print(f"H-stacked: {h_combined}")
# [15 23  8 31 19 18 20 11 28 22] — one long sequence
print(f"Shape: {h_combined.shape}")  # (10,)
print()

# Generate spike count data for 5 sessions, 10 time bins each
sessions = [np.random.randint(5, 30, 10) for _ in range(5)]

# Stack all sessions into a single matrix
all_sessions = np.vstack(sessions)
print(f"All sessions shape: {all_sessions.shape}")  # (5, 10)

# Now compute statistics across sessions with a single call
mean_per_bin = np.mean(all_sessions, axis=0)  # shape (10,) — mean across sessions
mean_per_session = np.mean(all_sessions, axis=1)  # shape (5,) — mean across time bins

print(f"Mean per time bin:  {np.round(mean_per_bin, 1)}")
print(f"Mean per session:   {np.round(mean_per_session, 1)}")
print()
