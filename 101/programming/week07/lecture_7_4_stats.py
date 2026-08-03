"""
Lecture 7.4: Statistical Functions for Neural Data
"""

import numpy as np

firing_rates = np.array([15.2, 23.8, 8.4, 31.5, 19.1, 42.3, 5.7, 27.6])

print(f"Mean:    {np.mean(firing_rates):.1f} Hz")
print(f"Median:  {np.median(firing_rates):.1f} Hz")
print(f"Std Dev: {np.std(firing_rates):.1f} Hz")
print(f"Variance:{np.var(firing_rates):.1f}")
print(f"Min:     {np.min(firing_rates):.1f} Hz")
print(f"Max:     {np.max(firing_rates):.1f} Hz")

print(f"Slowest neuron index: {np.argmin(firing_rates)}")
print(f"Fastest neuron index: {np.argmax(firing_rates)}")

print(f"25th percentile: {np.percentile(firing_rates, 25):.1f} Hz")
print(f"75th percentile: {np.percentile(firing_rates, 75):.1f} Hz")
print()

# 5 neurons, 10 trials — spike counts drawn from a Poisson distribution
# (Poisson is the standard model for neural spike counts)
activity = np.random.poisson(lam=10, size=(5, 10))

print(f"Array shape: {activity.shape}")  # (5, 10)
print(f"Overall mean: {np.mean(activity):.1f}")  # one number — everything averaged

# axis=1 collapses across columns (trials) → one value per row (neuron)
neuron_means = np.mean(activity, axis=1)
print(f"Mean per neuron: {neuron_means}")  # shape (5,)

# axis=0 collapses across rows (neurons) → one value per column (trial)
trial_means = np.mean(activity, axis=0)
print(f"Mean per trial:  {trial_means}")  # shape (10,)

# Same axis logic applies to std, sum, min, max, etc.
neuron_std = np.std(activity, axis=1)
print(f"Std per neuron:  {neuron_std}")
print()

# Spike counts across 20 trials for two neurons
neuron1 = np.array([10, 15, 8, 20, 12, 18, 9, 22, 14, 16, 11, 19, 7, 23, 13, 17, 10, 21, 15, 18])
neuron2 = np.array([12, 14, 9, 19, 11, 17, 8, 20, 13, 15, 10, 18, 8, 22, 12, 16, 11, 20, 14, 17])

# np.corrcoef returns a 2x2 matrix — we want the off-diagonal value
correlation = np.corrcoef(neuron1, neuron2)[0, 1]
print(f"Correlation between neurons: {correlation:.3f}")

if correlation > 0.7:
    print("Strongly correlated — neurons may be in the same circuit.")
elif correlation > 0.3:
    print("Moderately correlated.")
else:
    print("Weakly correlated — neurons are firing largely independently.")
print()

# 5 neurons, 20 trials each
all_neurons = np.random.randn(5, 20)

# Returns a 5x5 matrix — entry [i, j] is the correlation between neuron i and neuron j
corr_matrix = np.corrcoef(all_neurons)
print(f"Correlation matrix shape: {corr_matrix.shape}")  # (5, 5)
print(np.round(corr_matrix, 2))
print()
