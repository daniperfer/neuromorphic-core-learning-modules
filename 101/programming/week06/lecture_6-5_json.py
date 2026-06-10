"""
Lecture 6.5: JSON Files for Complex Data
"""

import csv
import json

# A complete experiment record as a Python dictionary
experiment = {
    "name": "Fear Conditioning Study",
    "date": "2026-02-27",
    "subject": "Mouse_042",
    "parameters": {"shock_intensity": 0.5, "tone_frequency": 4000, "n_trials": 10},
    "neurons": {
        "N001": {
            "type": "pyramidal",
            "region": "amygdala",
            "spike_times": [10.5, 23.1, 45.7, 67.2],
            "avg_firing_rate": 12.5,
        },
        "N002": {
            "type": "interneuron",
            "region": "amygdala",
            "spike_times": [5.2, 15.8, 28.4, 41.9, 55.3],
            "avg_firing_rate": 18.2,
        },
    },
    "results": {"freezing_percentage": 78.5, "acquisition_trials": 3, "extinction_trials": 7},
}

# Write to a JSON file
with open("experiment_data.json", "w") as file:
    json.dump(experiment, file, indent=4)  # indent=4 makes the file human-readable

print("Experiment saved.")
# The only type that can surprise you is a Python tuple: tuples become JSON arrays,
# and when loaded back they become Python lists, not tuples.
print()

# Load from JSON file
with open("experiment_data.json", "r") as file:
    loaded_data = json.load(file)

# Access exactly as you would a Python dictionary
print(f"Experiment: {loaded_data['name']}")
print(f"Subject:    {loaded_data['subject']}")
print(f"Freezing:   {loaded_data['results']['freezing_percentage']}%")

# Accessing nested data — just chain the keys
for neuron_id, neuron in loaded_data["neurons"].items():
    print(f"\n{neuron_id} ({neuron['type']}, {neuron['region']}):")
    print(f"  Spike times:  {neuron['spike_times']}")
    print(f"  Firing rate:  {neuron['avg_firing_rate']} Hz")
print()


# JSON vs CSV: When to Use Which
def save_experiment_complete(exp_name, metadata, neuron_rows):
    """
    Save experiment metadata as JSON and tabular neuron data as CSV.

    Params:
        exp_name: string, used as the base filename
        metadata: dict, experiment-level information (parameters, results, notes)
        neuron_rows: list of dicts, one per neuron, all with the same keys
    """
    # Metadata: nested structure → JSON
    json_file = f"{exp_name}_metadata.json"
    with open(json_file, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved: {json_file}")

    # Neuron data: tabular → CSV
    csv_file = f"{exp_name}_neurons.csv"
    if neuron_rows:
        fieldnames = list(neuron_rows[0].keys())
        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(neuron_rows)
        print(f"Neuron data saved: {csv_file}")


# Example use
metadata = {
    "experiment": "fear_conditioning",
    "date": "2026-02-27",
    "subject": "Mouse_042",
    "parameters": {"shock_intensity": 0.5, "tone_frequency": 4000},
    "results": {"freezing_percentage": 78.5},
}

neuron_rows = [
    {
        "neuron_id": "N001",
        "type": "pyramidal",
        "region": "amygdala",
        "spike_count": 4,
        "avg_rate": 12.5,
    },
    {
        "neuron_id": "N002",
        "type": "interneuron",
        "region": "amygdala",
        "spike_count": 5,
        "avg_rate": 18.2,
    },
]

save_experiment_complete("mouse_042_session_01", metadata, neuron_rows)
print()
