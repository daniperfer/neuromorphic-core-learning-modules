"""
Lecture 7.6: NumPy for Spike Train Analysis
"""

import numpy as np


def analyze_spike_train(spike_times):
    """
    The inter-spike interval (ISI) is the time between consecutive spikes.
    The distribution of ISIs tells you more about a neuron's firing pattern than
    the firing rate alone.
    A neuron firing at 20 Hz could be doing so with machine-like regularity (ISIs all near 50 ms)
    or in rapid bursts separated by long silences — the same average rate, very different biology.

    The coefficient of variation (CV) of the ISI is the standard measure for this:
    it's the standard deviation divided by the mean.
    A CV near 0 means perfectly regular.
    A CV near 1 (matching a Poisson process) means irregular but not bursty.
    A CV above 1 means the neuron is firing in bursts.
    """
    spike_times = np.array(spike_times)

    # Basic statistics
    n_spikes = len(spike_times)
    duration = spike_times[-1] - spike_times[0]  # total recording duration (ms)
    firing_rate = n_spikes / (duration / 1000)  # convert ms to seconds for Hz

    # Inter-spike intervals — np.diff computes the difference between consecutive elements
    isi = np.diff(spike_times)
    mean_isi = np.mean(isi)
    std_isi = np.std(isi)
    cv_isi = std_isi / mean_isi  # coefficient of variation

    # Burst detection: ISIs shorter than 10 ms indicate burst firing
    burst_threshold = 10.0
    burst_spikes = np.sum(isi < burst_threshold)

    print("=== SPIKE TRAIN ANALYSIS ===")
    print(f"Total spikes:  {n_spikes}")
    print(f"Duration:      {duration:.1f} ms")
    print(f"Firing rate:   {firing_rate:.1f} Hz")
    print(f"Mean ISI:      {mean_isi:.1f} ms")
    print(f"CV of ISI:     {cv_isi:.3f}")

    if cv_isi < 0.3:
        print("Firing pattern: Regular (clock-like)")
    elif cv_isi < 0.8:
        print("Firing pattern: Irregular")
    else:
        print("Firing pattern: Bursty")

    print(f"Burst spikes:  {burst_spikes}")


# Compare a regular neuron vs. an irregular one
np.random.seed(42)

# Regular: ISIs drawn from a tight normal distribution (mean 50ms, std 5ms)
regular_spikes = np.cumsum(np.random.normal(50, 5, 20))

# Irregular: ISIs drawn from an exponential distribution — the Poisson process model
irregular_spikes = np.cumsum(np.random.exponential(50, 20))

print("REGULAR NEURON:")
analyze_spike_train(regular_spikes)

print("\nIRREGULAR NEURON:")
analyze_spike_train(irregular_spikes)
print()


def compute_psth(spike_times_list, stimulus_times, window=(-100, 500), bin_size=10):
    """
    Compute a peri-stimulus time histogram.

    Params:
    spike_times_list : list of arrays, one per trial
    stimulus_times   : array of stimulus onset times (ms), one per trial
    window           : (pre, post) time window around stimulus (ms)
    bin_size         : width of each time bin (ms)

    Returns bin_centers (ms) and firing rate (Hz) per bin.
    """
    # Build the bin edges from the window boundaries
    bins = np.arange(window[0], window[1] + bin_size, bin_size)
    psth = np.zeros(len(bins) - 1)  # one count per bin

    for trial_spikes, stim_time in zip(spike_times_list, stimulus_times):
        # Express spike times relative to stimulus onset
        relative_spikes = np.array(trial_spikes) - stim_time

        # Count spikes in each bin
        counts, _ = np.histogram(relative_spikes, bins=bins)
        psth += counts

    # Convert accumulated counts to firing rate (Hz)
    n_trials = len(spike_times_list)
    psth_rate = (psth / n_trials) / (bin_size / 1000)  # spikes per trial per bin → Hz

    # Bin centers for plotting (midpoint of each bin)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    return bin_centers, psth_rate


# Simulate 20 trials — background firing plus a response window after each stimulus
np.random.seed(42)
n_trials = 20
stimulus_times = np.arange(n_trials) * 1000  # one stimulus every 1000 ms

spike_trains = []
for trial in range(n_trials):
    stim = stimulus_times[trial]
    background = np.random.uniform(stim - 100, stim + 500, 3)  # 3 background spikes
    response = np.random.uniform(stim + 50, stim + 200, 5)  # 5 response spikes
    spikes = np.sort(np.concatenate([background, response]))
    spike_trains.append(spikes)

bin_centers, psth_rate = compute_psth(spike_trains, stimulus_times)

# Print a text-based visualization
print("PSTH Results:")
print(f"{'Time (ms)':<12} {'Rate (Hz)':<10}")
print("-" * 22)
for time, rate in zip(bin_centers, psth_rate):
    bar = "█" * int(rate / 2)
    print(f"{time:<12.0f} {rate:<10.1f} {bar}")
print()
