# ============================================================
# Assignment 6: Neuroscience Data Pipeline
# Student Name: Daniel Pereira
# Date: June 12, 2026
# ============================================================

import csv
import json
import os
import random
from datetime import datetime

# ------------------------------------------------------------
# PART 1: Folder Setup
# Create the following structure:
#   assignment6_data/
#       raw/          ← one CSV per trial goes here
#       processed/    ← report.txt goes here
# ------------------------------------------------------------


def create_folder_structure(base_dir="assignment6_data"):
    """
    Create the directory structure for the experiment.
    Returns the paths to raw/ and processed/ subdirectories.
    """
    # Create base_dir/raw/ and base_dir/processed/
    # Use os.makedirs with exist_ok=True
    # Return (raw_path, processed_path) as a tuple
    os.makedirs(base_dir, exist_ok=True)
    raw_path = os.path.join(base_dir, "raw")
    os.makedirs(raw_path, exist_ok=True)
    processed_path = os.path.join(base_dir, "processed")
    os.makedirs(processed_path, exist_ok=True)
    print(f"Created: {raw_path}/")
    print(f"Created: {processed_path}/")
    return (raw_path, processed_path)


# ------------------------------------------------------------
# PART 2: Data Generation
# Generate spike train data for 10 neurons across 5 trials.
# Each trial is a list of 10 dicts — one per neuron.
# ------------------------------------------------------------


def generate_trial_data(trial_num, n_neurons=10):
    """
    Simulate spike train data for one trial.

    Each neuron dict should contain:
        neuron_id      -- string, e.g. "N001"
        trial          -- int, the trial number
        spike_count    -- int, random between 0 and 40
        firing_rate    -- float, spikes per second (assume 2-second trial window)
        active         -- bool, True if firing_rate >= 5.0 Hz
        mean_isi_ms    -- float, mean inter-spike interval in ms
                         (if spike_count > 1: trial_duration_ms / spike_count
                          if spike_count == 1: use 2000.0
                          if spike_count == 0: use 0.0)

    Params:
        trial_num  -- int, trial number (1 - 5)
        n_neurons  -- int, number of neurons to simulate

    Returns:
        list of dicts, one per neuron
    """
    trial_duration_sec = 2.0
    trial_duration_ms = trial_duration_sec * 1000

    data = []
    for i in range(n_neurons):
        # Build each neuron's dict using the formulas above
        # Hint: firing_rate = spike_count / trial_duration_sec
        spike_count = random.randint(0, 40)
        if spike_count == 0:
            mean_isi_ms = 0
        elif spike_count == 1:
            mean_isi_ms = 1
        else:
            mean_isi_ms = trial_duration_ms / spike_count
        firing_rate = spike_count / trial_duration_sec
        data.append(
            {
                "neuron_id": f"N{i:03d}",
                "trial": f"{trial_num:03d}",
                "spike_count": spike_count,
                "firing_rate": firing_rate,
                "active": True if firing_rate > 0.5 else False,
                "mean_isi_ms": mean_isi_ms,
            }
        )

    return data


# ------------------------------------------------------------
# PART 3: Saving Data
# Save each trial as a CSV in raw/, and save the experiment
# metadata as a JSON file in the base directory.
# ------------------------------------------------------------


def save_trial_csv(raw_dir, trial_num, trial_data):
    """
    Save one trial's data as a CSV file.
    Filename format: trial_001.csv, trial_002.csv, etc.

    Returns True on success, False on failure.
    """
    # Save trial_data (list of dicts) to raw_dir/trial_NNN.csv
    # Use csv.DictWriter
    # Handle errors with try/except — return False if anything goes wrong
    if not trial_data:
        print(f"Warning: trial {trial_data} has no data — skipping.")
        return False

    # session_001.csv, session_002.csv, etc.
    session_file = os.path.join(raw_dir, f"trial_{trial_num:03d}.csv")

    fieldnames = list(trial_data[0].keys())
    with open(session_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(trial_data)

    print(f"Trial {trial_num} saved: {len(trial_data)} neurons.")
    return True


def save_metadata_json(base_dir, metadata):
    """
    Save experiment metadata as metadata.json in base_dir.
    """
    # Save metadata dict as JSON with indent=4
    # Handle errors with try/except
    metadata_file = os.path.join(base_dir, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved: {metadata_file}")
    return metadata_file


# ------------------------------------------------------------
# PART 4: Loading Data
# Load all trial CSV files from the raw/ directory.
# ------------------------------------------------------------


def load_all_trials(raw_dir):
    """
    Load every trial_NNN.csv file from raw_dir.

    Returns a dict mapping trial filename → list of row dicts.
    Example: {"trial_001": [{...}, {...}, ...], "trial_002": [...], ...}

    After loading, convert types:
        spike_count  → int
        firing_rate  → float
        active       → bool  (compare string to "True")
        mean_isi_ms  → float
    """
    # Use os.listdir to find files starting with "trial_" and ending with ".csv"
    # Sort them, load each with csv.DictReader, convert types, store in a dict
    # Skip files that fail to load (log a warning, continue)
    session_files = sorted(
        f for f in os.listdir(raw_dir) if f.startswith("trial_") and f.endswith(".csv")
    )

    if not session_files:
        print("No session files found in this experiment directory.")
        return {}

    all_data = {}
    for session_file in session_files:
        filepath = os.path.join(raw_dir, session_file)
        try:
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)
                data = list(reader)
                # Convert from strings to proper numeric types
                for row in data:
                    row["spike_count"] = int(row["spike_count"])
                    row["firing_rate"] = float(row["firing_rate"])
                    row["active"] = row["active"] == "True"
                    row["mean_isi_ms"] = float(row["mean_isi_ms"])
        except Exception as e:
            print(f"File {filepath} failed to load. Skipping.")
            print(f"Error: {e}.")
            continue

        session_name = session_file.replace(".csv", "")
        all_data[session_name] = data
        print(f"Loaded {session_name}: {len(data)} neurons.")

    return all_data


# ------------------------------------------------------------
# PART 5: Analysis
# Compute summary statistics from the loaded trial data.
# ------------------------------------------------------------


def analyze_trials(all_trials):
    """
    Analyze all loaded trial data and return a summary dict.

    {"trial_001": [{...}, {...}, ...], "trial_002": [...], ...}

    {
    "neuron_id",
    "trial",
    "spike_count",
    "firing_rate",
    "active",
    "mean_isi_ms",
    }

    Your summary should include:
        total_trials       -- int
        total_neurons      -- int (neurons per trials)
        overall_avg_rate   -- float, mean firing rate across all neurons and trials
        overall_avg_isi    -- float, mean ISI across all active neurons (skip zeros)
        per_neuron         -- dict mapping neuron_id →
                                 {"avg_rate": float, "active_trials": int}

    Use the per_neuron data to identify the most and least active neurons
    (highest and lowest avg_rate).
    """
    # Flatten all trial data into one list, then compute statistics
    # For per_neuron, group rows by neuron_id across all trials
    per_neuron = {}
    total_trials = len(all_trials.keys())
    neurons = set()
    n_isis = 0
    n_rates = 0
    for _, all_neur_data in all_trials.items():
        # all_neur_data is a list of dicts
        for neur_data in all_neur_data:
            neurons.add(neur_data["neuron_id"])
            n_rates += 1
            if neur_data["active"]:
                n_isis += 1

            if neur_data["neuron_id"] in per_neuron:
                per_neuron[neur_data["neuron_id"]]["firing_rate"] += neur_data["firing_rate"]
                per_neuron[neur_data["neuron_id"]]["mean_isi_ms"] += neur_data["mean_isi_ms"]
                per_neuron[neur_data["neuron_id"]]["spike_count"] += neur_data["spike_count"]
                per_neuron[neur_data["neuron_id"]]["active"] += neur_data["active"]

            else:
                per_neuron[neur_data["neuron_id"]] = {}

                per_neuron[neur_data["neuron_id"]]["firing_rate"] = neur_data["firing_rate"]
                per_neuron[neur_data["neuron_id"]]["mean_isi_ms"] = neur_data["mean_isi_ms"]
                per_neuron[neur_data["neuron_id"]]["spike_count"] = neur_data["spike_count"]
                per_neuron[neur_data["neuron_id"]]["active"] = neur_data["active"]

    # highest and lowest avg_rate
    avg_rates = [(id, neur_data["firing_rate"]) for id, neur_data in per_neuron.items()]
    avg_isi = [(id, neur_data["mean_isi_ms"]) for id, neur_data in per_neuron.items()]
    print(f"LOG: avg_rates = {avg_rates}, n_rates = {n_rates}")
    print(f"LOG: avg_isi = {avg_isi}, n_isis = {n_isis}")
    sorted_rates = sorted(avg_rates, key=lambda n: n[1])
    most_active = sorted_rates[-1]
    least_active = sorted_rates[0]
    results = {
        "total_trials": total_trials,
        "total_neurons": len(neurons),
        "overall_avg_rate": sum(rate[1] for rate in avg_rates) / n_rates,
        "overall_avg_isi": sum(isi[1] for isi in avg_isi) / n_isis,
        "most_active": most_active,
        "least_active": least_active,
        "per_neuron": per_neuron,
    }
    return results


# ------------------------------------------------------------
# PART 6: Report Generation
# Write a human-readable report to processed/report.txt
# ------------------------------------------------------------


def generate_report(processed_dir, metadata, summary):
    """
    Write a summary report to processed/report.txt.

    The report should include:
        - Experiment name, researcher, date
        - Total trials and neurons recorded
        - Overall average firing rate and ISI
        - A table of per-neuron results (neuron_id, avg rate, active trials)
        - The most and least active neurons

    Save the report and also print it to the console.
    """
    # Build the report as a list of strings, join with "\n", write to file
    # Build the report as a list of lines, then join at the end
    lines = [
        "=" * 60,
        f"EXPERIMENT REPORT: {metadata['experiment']}",
        "=" * 60,
        f"Researcher:  {metadata['researcher']}",
        f"Date:     {metadata['date'][:10]}",  # Date only, not full timestamp
        f"Trials:    {summary['total_trials']}",
        f"Neurons:  {summary['total_neurons']}",
        "",
        f"Overall Avg Firing Rate:  {summary['overall_avg_rate']} Hz",
        f"Overall Avg ISI:  {summary['overall_avg_isi']:0.2f} ms",
        "\nPer-Neuron Summary:",
        "Neuron \tAvg Rate (Hz) \tActive Trials",
        "------ \t------------- \t-------------",
    ]
    for nid, neuron in summary["per_neuron"].items():
        lines.append(
            f"{nid} \t{neuron['firing_rate']}      "
            f"\t{neuron['active']}/{summary['total_trials']}"
        )

    lines.append(
        f"\nMost active neuron: {summary['most_active'][0]} ({summary['most_active'][1]} Hz)"
    )
    lines.append(
        f"Least active neuron: {summary['least_active'][0]} ({summary['least_active'][1]} Hz)"
    )
    lines.append("=" * 60)
    report_text = "\n".join(lines)

    # Save and display
    report_file = os.path.join(processed_dir, "report.txt")
    with open(report_file, "w") as f:
        f.write(report_text)

    print(report_text)
    print(f"Report saved: {report_file}")


# ------------------------------------------------------------
# MAIN: Run the full pipeline
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("ASSIGNMENT 6: Neuroscience Data Pipeline")
    print("=" * 55)

    # Part 1: Set up folders
    raw_dir, processed_dir = create_folder_structure("assignment6_data")

    # Part 2 & 3: Generate and save trials
    metadata = {
        "experiment": "Spike Train Study — Multi-Trial",
        "researcher": "Daniel Pereira",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "n_trials": 5,
        "n_neurons": 10,
        "trial_duration_sec": 2.0,
        "active_threshold_hz": 5.0,
    }

    save_metadata_json("assignment6_data", metadata)

    for trial_num in range(1, 6):
        trial_data = generate_trial_data(trial_num)
        save_trial_csv(raw_dir, trial_num, trial_data)

    # Part 4: Load everything back
    all_trials = load_all_trials(raw_dir)
    print()

    # Part 5: Analyze
    summary = analyze_trials(all_trials)

    # Part 6: Generate report
    generate_report(processed_dir, metadata, summary)

    print("\nPipeline complete.")
    print("Output files are in: assignment6_data/")
