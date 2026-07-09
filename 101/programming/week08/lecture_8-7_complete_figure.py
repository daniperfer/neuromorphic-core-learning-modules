"""
Lecture 8.7: Building a Complete Analysis Figure
"""

import matplotlib.pyplot as plt
import numpy as np

# Demonstrate GridSpec layout before the full example
fig = plt.figure(figsize=(14, 10))
gs = plt.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.35)

ax_top = fig.add_subplot(gs[0, :])  # Row 0, all columns → full-width panel
ax_mid_l = fig.add_subplot(gs[1, 0])  # Row 1, left column
ax_mid_r = fig.add_subplot(gs[1, 1])  # Row 1, right column
ax_bot_l = fig.add_subplot(gs[2, 0])  # Row 2, left column
ax_bot_r = fig.add_subplot(gs[2, 1])  # Row 2, right column

# Label each panel to show the layout
for ax, label in zip(
    [ax_top, ax_mid_l, ax_mid_r, ax_bot_l, ax_bot_r],
    ["Full-width top panel", "Mid left", "Mid right", "Bottom left", "Bottom right"],
):
    ax.text(
        0.5, 0.5, label, transform=ax.transAxes, ha="center", va="center", fontsize=11, color="gray"
    )

plt.savefig("figure_8-7-1_gridspec.png", dpi=300, bbox_inches="tight", facecolor="white")
print("GridSpec example completed...")


def create_neuron_report(neuron_id, spike_times, duration=1000):
    """
    Creates a Complete Analysis Figure
    """
    spike_times = np.array(spike_times)
    isi = np.diff(spike_times)  # Time between each consecutive pair of spikes

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle(f"Neuron {neuron_id} — Complete Analysis", fontsize=16, fontweight="bold")

    gs = plt.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.35)

    # --- Panel 1: Full-width spike train across the top row ---
    ax1 = fig.add_subplot(gs[0, :])
    ax1.vlines(spike_times, 0, 1, colors="black", linewidth=1.5)
    ax1.set_xlim(0, duration)
    ax1.set_ylim(-0.2, 1.2)
    ax1.set_xlabel("Time (ms)")
    ax1.set_title(f"Spike Train ({len(spike_times)} spikes)")
    ax1.set_yticks([])  # No y-axis ticks — spike train is binary

    # --- Panel 2: ISI distribution ---
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.hist(isi, bins=20, color="steelblue", edgecolor="white")
    ax2.axvline(np.mean(isi), color="red", linestyle="--", label=f"Mean: {np.mean(isi):.1f}ms")
    ax2.set_xlabel("ISI (ms)")
    ax2.set_ylabel("Count")
    ax2.set_title("ISI Distribution")
    ax2.legend(fontsize=9)

    # --- Panel 3: Cumulative spike count over time ---
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.step(
        spike_times,
        np.arange(1, len(spike_times) + 1),
        where="post",
        color="darkgreen",
        linewidth=2,
    )
    ax3.set_xlabel("Time (ms)")
    ax3.set_ylabel("Cumulative Spikes")
    ax3.set_title("Cumulative Spike Count")
    ax3.grid(True, alpha=0.3)

    # --- Panel 4: Formatted statistics text box ---
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.axis("off")  # No axes drawn — this panel is pure text

    cv_isi = np.std(isi) / np.mean(isi)
    firing_rate = len(spike_times) / (duration / 1000)

    if cv_isi < 0.3:
        pattern = "Regular"
    elif cv_isi < 0.8:
        pattern = "Irregular"
    else:
        pattern = "Bursty"

    stats_text = (
        f"NEURON STATISTICS\n"
        f"{'─' * 28}\n"
        f"Total Spikes:   {len(spike_times)}\n"
        f"Firing Rate:    {firing_rate:.1f} Hz\n"
        f"Mean ISI:       {np.mean(isi):.1f} ms\n"
        f"ISI Std Dev:    {np.std(isi):.1f} ms\n"
        f"CV ISI:         {cv_isi:.3f}\n"
        f"Pattern:        {pattern}"
    )
    ax4.text(
        0.05,
        0.95,
        stats_text,
        transform=ax4.transAxes,
        fontsize=11,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    # --- Panel 5: Instantaneous firing rate over time ---
    ax5 = fig.add_subplot(gs[2, 1])
    inst_rate = 1000 / isi  # Convert ISI (ms) to Hz
    spike_midpts = (spike_times[:-1] + spike_times[1:]) / 2  # Midpoint between each spike pair
    ax5.plot(spike_midpts, inst_rate, "r-o", markersize=3, linewidth=1)
    ax5.set_xlabel("Time (ms)")
    ax5.set_ylabel("Inst. Rate (Hz)")
    ax5.set_title("Instantaneous Firing Rate")
    ax5.grid(True, alpha=0.3)

    plt.savefig(f"figure_8-7-2_neuron_{neuron_id}_report.png", dpi=300, bbox_inches="tight")


# Generate a test spike train and run the report
np.random.seed(42)
spike_times = np.cumsum(np.random.exponential(40, 30))  # Exponential ISIs → ~25 Hz
spike_times = spike_times[spike_times < 1000]  # Keep only spikes within 1 second

create_neuron_report("N042", spike_times)
print("Neuron creation report example completed...")
