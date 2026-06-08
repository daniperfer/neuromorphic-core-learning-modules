"""
Lecture 6.2: Working with CSV Files
"""
import csv
import random

with open("neurons.csv", "r") as file:
    reader = csv.reader(file)

    header = next(reader)  # Pull off the first row (the column names)
    print(f"Columns: {header}")

    for crow in reader:
        neuron_id = crow[0]
        neuron_type = crow[1]
        voltage = float(crow[2])  # Everything from CSV is a string — convert as needed
        spike_count = int(crow[3])
        region = crow[4]

        print(f"{neuron_id}: {neuron_type}, {voltage}mV, {spike_count} spikes, {region}")

print()

# csv.DictReader
with open("neurons.csv", "r") as file:
    dreader = csv.DictReader(file)  # Reads the header automatically

    neurons = []
    for drow in dreader:
        neurons.append(drow)

# Now access values by column name instead of position
for neuron in neurons:
    print(
        f"ID: {neuron['neuron_id']}, " f"Type: {neuron['type']}, " f"Voltage: {neuron['voltage']}mV"
    )
print()

experiment_data = [
    {"trial": 1, "stimulus": "tone", "response_time": 0.342, "correct": True},
    {"trial": 2, "stimulus": "light", "response_time": 0.289, "correct": True},
    {"trial": 3, "stimulus": "tone", "response_time": 0.445, "correct": False},
    {"trial": 4, "stimulus": "light", "response_time": 0.312, "correct": True},
    {"trial": 5, "stimulus": "tone", "response_time": 0.378, "correct": True},
]

with open("experiment_results.csv", "w", newline="") as file:
    fieldnames = ["trial", "stimulus", "response_time", "correct"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()  # Writes the column names as the first row
    writer.writerows(experiment_data)  # Writes all rows at once
    # If you’re building rows one at a time inside a loop, use writer.writerow() (singular) instead.

print("Experiment data saved!")
print()


# Here’s a more complete example that mirrors a real workflow
def generate_experiment_data(n_trials=20):
    """Simulate a behavioral neuroscience experiment with stimulus and neural response data."""
    data = []
    stimuli = ["tone_low", "tone_high", "light_dim", "light_bright"]

    for trial in range(1, n_trials + 1):
        stimulus = random.choice(stimuli)
        response_time = random.uniform(0.200, 0.600)  # 200–600 ms
        correct = random.random() > 0.2  # ~80% accuracy
        firing_rate = random.uniform(5, 50)  # Hz

        data.append(
            {
                "trial": trial,
                "stimulus": stimulus,
                "response_time": round(response_time, 3),
                "correct": correct,
                "firing_rate": round(firing_rate, 1),
            }
        )

    return data


def save_experiment(filename, data):
    """Save experiment data to a CSV file."""
    fieldnames = ["trial", "stimulus", "response_time", "correct", "firing_rate"]

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} trials to {filename}")


def analyze_experiment(filename):
    """Load a CSV file and compute summary statistics."""
    with open(filename, "r") as file:
        dreader = csv.DictReader(file)
        data = list(dreader)

    # Convert from strings to proper types
    for row in data:
        row["response_time"] = float(row["response_time"])
        row["correct"] = row["correct"] == "True"  # "True"/"False" strings → bool
        row["firing_rate"] = float(row["firing_rate"])

    n_trials = len(data)
    n_correct = sum(1 for row in data if row["correct"])
    accuracy = n_correct / n_trials * 100
    avg_rt = sum(row["response_time"] for row in data) / n_trials
    avg_fr = sum(row["firing_rate"] for row in data) / n_trials

    print("\n=== EXPERIMENT ANALYSIS ===")
    print(f"Total Trials:          {n_trials}")
    print(f"Accuracy:              {accuracy:.1f}%")
    print(f"Avg Response Time:     {avg_rt * 1000:.0f} ms")
    print(f"Avg Firing Rate:       {avg_fr:.1f} Hz")

    # Break down accuracy and RT per stimulus type
    stimuli = sorted(set(row["stimulus"] for row in data))
    print("\nPer Stimulus Breakdown:")
    for stim in stimuli:
        stim_rows = [row for row in data if row["stimulus"] == stim]
        stim_acc = sum(1 for r in stim_rows if r["correct"]) / len(stim_rows) * 100
        stim_rt = sum(r["response_time"] for r in stim_rows) / len(stim_rows)
        print(f"  {stim:<15}: {stim_acc:.0f}% accuracy, {stim_rt * 1000:.0f} ms Resp. Time")


# Run the full pipeline
data = generate_experiment_data(20)
save_experiment("experiment_001.csv", data)
analyze_experiment("experiment_001.csv")
