"""
Lecture 15.5: Presenting Your Results — Figures, Captions, and the Story Arc
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import matplotlib.pyplot as plt
import numpy as np
from week12.lecture_12_2_isi import isi_statistics
from week13.lecture_13_7_oscillation_dynamics_alt import (
    compute_population_rate,
    compute_power_spectrum,
)

# --- Define your color palette ONCE at the top of your plotting code ---
COLORS = {
    "excitatory": "#2c4a8c",  # dark blue  — for E neurons, E raster
    "inhibitory": "#c0392b",  # dark red   — for I neurons, I raster
    "population": "#2c3e50",  # near-black — for population rate
    "sweep_line": "#2c4a8c",  # dark blue  — for sweep curve
    "sweep_marker": "#e74c3c",  # bright red — for individual sweep points
    "reference": "#95a5a6",  # gray       — for reference lines
    "condition_low": "#3498db",  # light blue — for low-w_IE condition
    "condition_med": "#e67e22",  # orange     — for medium condition
    "condition_high": "#8e44ad",  # purple     — for high condition
}

# Standard figure settings
plt.rcParams.update(
    {
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": 150,  # screen display
        "savefig.dpi": 300,  # saved files — always 300 for final project
    }
)


def plot_comparison_figure(results_dict, conditions, save_path="final_figure1_comparison.png"):
    """
    Plot raster plots and population rate for multiple named conditions.

    Parameters
    ----------
    results_dict : dict
        Dictionary mapping condition label to simulation result dict.
    conditions : list of str
        Ordered list of condition labels to plot.
    save_path : str
        Filename for saved figure.
    """
    n_cond = len(conditions)
    fig, axes = plt.subplots(2, n_cond, figsize=(5 * n_cond, 7))

    condition_colors = [
        COLORS["condition_low"],
        COLORS["condition_med"],
        COLORS["condition_high"],
    ][:n_cond]

    for col, (label, color) in enumerate(zip(conditions, condition_colors)):
        result = results_dict[label]
        spike_times = result["spike_times_E"]
        spike_ids = result["spike_ids_E"]
        N = result["N_E"]
        duration = result["duration"]
        params = result["params"]

        # Top row: raster plot
        ax_raster = axes[0, col]
        ax_raster.scatter(spike_times, spike_ids, s=0.5, color=color, alpha=0.6)
        ax_raster.set_xlim(0, duration)
        ax_raster.set_ylim(0, N)
        ax_raster.set_ylabel("Neuron Index" if col == 0 else "", fontsize=12)
        ax_raster.set_title(f"w_IE = {params.w_IE:.2f} nA", fontsize=11)
        ax_raster.text(
            0.02,
            0.96,
            f"({chr(65 + col)})",
            transform=ax_raster.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
        )

        # Bottom row: population rate
        ax_rate = axes[1, col]
        t_pop, rate_pop = compute_population_rate(
            spike_times, spike_ids, N, duration, bin_size=0.01
        )
        ax_rate.plot(t_pop, rate_pop, color=COLORS["population"], linewidth=1.2)
        ax_rate.set_xlabel("Time (s)", fontsize=12)
        ax_rate.set_ylabel("Firing Rate (Hz)" if col == 0 else "", fontsize=12)
        ax_rate.set_xlim(0, duration)
        ax_rate.text(
            0.02,
            0.96,
            f"({chr(65 + n_cond + col)})",
            transform=ax_rate.transAxes,
            fontsize=12,
            fontweight="bold",
            va="top",
        )

        # Compute and display mean CV
        isis, cv = isi_statistics(spike_times, spike_ids, N)
        mean_cv = np.nanmean(cv)
        ax_raster.text(
            0.98,
            0.96,
            f"CV = {mean_cv:.2f}",
            transform=ax_raster.transAxes,
            ha="right",
            va="top",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
        )

    plt.suptitle(
        "Figure 15.5.1: Network Activity Under Three Inhibitory Weight Conditions",
        fontsize=13,
        fontweight="bold",
        y=1.01,
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print()
    print(f"Figure 1 saved: {save_path}")


# --- CAPTION ---
CAPTION_FIGURE1 = """
Figure 1. Network activity under three inhibitory synaptic weight conditions.
(A–C) Raster plots showing spike times for all 400 excitatory neurons over 2 s
of simulation. Each dot represents one spike. Mean coefficient of variation (CV)
of interspike intervals is shown in the upper right of each panel.
(D–F) Population firing rate estimated by binning all excitatory spikes in 10 ms
bins and normalizing by neuron count. Inhibitory weights are w_IE = 0.3, 0.5, and
0.9 nA for panels A/D, B/E, and C/F respectively. All other parameters are held
constant (see Methods).
"""
print(CAPTION_FIGURE1)


def plot_sweep_figure(
    w_IE_values, mean_cv_values, mean_rate_values, save_path="final_figure2_sweep.png"
):
    """
    Two-panel sweep figure: CV and firing rate vs. inhibitory weight.
    """
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    fig.suptitle(
        "Figure 15.5.2: Effect of Inhibitory Weight on Network Statistics",
        fontsize=13,
        fontweight="bold",
    )

    # Panel A: CV vs w_IE
    ax = axes[0]
    ax.plot(
        w_IE_values,
        mean_cv_values,
        "-o",
        color=COLORS["sweep_line"],
        markerfacecolor=COLORS["sweep_marker"],
        linewidth=2.0,
        markersize=8,
        zorder=5,
    )
    ax.axhline(
        y=1.0, color=COLORS["reference"], linestyle="--", linewidth=1.2, label="CV = 1 (Poisson)"
    )
    ax.set_xlabel("Inhibitory Synaptic Weight w_IE (nA)", fontsize=12)
    ax.set_ylabel("Mean Coefficient of Variation (CV)", fontsize=12)
    ax.set_title("(A) Firing Regularity", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.25)
    ax.set_ylim(bottom=0)

    # Panel B: Firing rate vs w_IE
    ax = axes[1]
    ax.plot(
        w_IE_values,
        mean_rate_values,
        "-o",
        color=COLORS["sweep_line"],
        markerfacecolor=COLORS["sweep_marker"],
        linewidth=2.0,
        markersize=8,
        zorder=5,
    )
    ax.set_xlabel("Inhibitory Synaptic Weight w_IE (nA)", fontsize=12)
    ax.set_ylabel("Mean Firing Rate (Hz)", fontsize=12)
    ax.set_title("(B) Population Firing Rate", fontsize=11)
    ax.grid(True, alpha=0.25)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print()
    print(f"Figure 2 saved: {save_path}")


CAPTION_FIGURE2 = """
Figure 2. Effect of inhibitory synaptic weight on network statistics.
(A) Mean coefficient of variation (CV) of interspike intervals as a function of
inhibitory synaptic weight w_IE. Each point represents the mean CV across all
excitatory neurons with at least two spikes, averaged over one 2 s simulation.
The dashed line indicates CV = 1 (Poisson process). Error bars represent ± SD.
(B) Mean excitatory population firing rate (Hz) as a function of w_IE.
The sweep covers 8 evenly spaced values from 0.2 to 1.0 nA (numpy.linspace).
All other parameters held constant (see Methods).
"""
print(CAPTION_FIGURE2)


def plot_analysis_figure(results_dict, conditions, save_path="final_figure3_analysis.png"):
    """
    ISI histograms and power spectra for named conditions.
    """
    n_cond = len(conditions)
    fig, axes = plt.subplots(2, n_cond, figsize=(5 * n_cond, 8))

    condition_colors = [
        COLORS["condition_low"],
        COLORS["condition_med"],
        COLORS["condition_high"],
    ][:n_cond]

    for col, (label, color) in enumerate(zip(conditions, condition_colors)):
        result = results_dict[label]
        spike_times = result["spike_times_E"]
        spike_ids = result["spike_ids_E"]
        N = result["N_E"]
        duration = result["duration"]
        params = result["params"]

        # Top row: ISI histogram
        ax = axes[0, col]
        isis, cv = isi_statistics(spike_times, spike_ids, N)
        all_isis = np.concatenate([isi for isi in isis if len(isi) > 0])
        ax.hist(
            all_isis * 1000,
            bins=50,
            range=(0, 200),
            color=color,
            alpha=0.75,
            edgecolor="white",
            linewidth=0.5,
        )
        ax.set_xlabel("Interspike Interval (ms)", fontsize=12)
        ax.set_ylabel("Count" if col == 0 else "", fontsize=12)
        ax.set_title(f"({chr(65 + col)}) ISI: w_IE = {params.w_IE:.2f} nA", fontsize=11)
        ax.text(
            0.97,
            0.97,
            f"CV = {np.nanmean(cv):.2f}",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
        )

        # Bottom row: power spectrum
        ax = axes[1, col]
        t_pop, rate_pop = compute_population_rate(
            spike_times, spike_ids, N, duration, bin_size=0.01
        )
        freqs, power = compute_power_spectrum(rate_pop, fs=100.0)
        # Plot only up to 100 Hz
        mask = freqs <= 100
        ax.plot(freqs[mask], power[mask], color=COLORS["population"], linewidth=1.5)
        ax.fill_between(freqs[mask], power[mask], alpha=0.2, color=color)
        ax.set_xlabel("Frequency (Hz)", fontsize=12)
        ax.set_ylabel("Power (a.u.)" if col == 0 else "", fontsize=12)
        ax.set_title(f"({chr(65 + n_cond + col)}) Power Spectrum", fontsize=11)
        peak_freq = freqs[mask][np.argmax(power[mask])]
        ax.axvline(
            x=peak_freq,
            color=COLORS["reference"],
            linestyle="--",
            linewidth=1.2,
            label=f"Peak: {peak_freq:.0f} Hz",
        )
        ax.legend(fontsize=9)

    plt.suptitle(
        "Figure 15.5.3: ISI Distributions and Power Spectra by Condition",
        fontsize=13,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print()
    print(f"Figure 3 saved: {save_path}")
