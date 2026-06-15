"""
Lecture 6.6: Real Neuroscience Data Formats
"""

import csv
import io
import random


def simulate_eeg_recording(duration_sec=10, sample_rate=250):
    """
    Simulate a resting-state EEG recording.

    Params:
        duration_sec: recording length in seconds
        sample_rate: samples per second (250 Hz is typical for clinical EEG)

    Returns:
        list of dicts, one per sample
    """
    n_samples = duration_sec * sample_rate
    data = []

    for i in range(n_samples):
        timestamp = i / sample_rate  # Convert sample index to seconds
        alpha_wave = 10 * random.uniform(-1, 1)  # Simplified alpha band (8–12 Hz)
        noise = 2 * random.uniform(-1, 1)  # Background noise
        voltage = alpha_wave + noise

        data.append(
            {
                "sample": i,
                "timestamp": round(timestamp, 4),
                "voltage_uV": round(voltage, 3),
                "channel": "Oz",  # Standard occipital electrode position
            }
        )

    return data


def save_eeg_data(filename, data, metadata):
    """
    Save EEG data to a CSV file with a commented metadata header.

    The header lines all start with '#' so they can be skipped during loading.
    """
    with open(filename, "w", newline="") as file:
        # Write metadata as comment lines — one key piece of information per line
        file.write("# EEG Recording\n")
        file.write(f"# Subject: {metadata['subject']}\n")
        file.write(f"# Sample Rate: {metadata['sample_rate']} Hz\n")
        file.write(f"# Duration: {metadata['duration']} seconds\n")
        file.write(f"# Samples: {len(data)}\n")
        file.write("#\n")

        # Write the actual data as CSV
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} samples to '{filename}'.")


def analyze_eeg_file(filename):
    """
    Load an EEG CSV file that starts with '#' comment lines,
    then compute basic statistics on the voltage data.
    """
    with open(filename, "r") as file:
        # Split into comment lines and data lines
        data_lines = [line for line in file if not line.startswith("#")]

    # Join the data lines back into a string, then parse as CSV
    reader = csv.DictReader(io.StringIO("".join(data_lines)))
    data = list(reader)

    # Convert from strings to proper numeric types
    for row in data:
        row["voltage_uV"] = float(row["voltage_uV"])
        row["timestamp"] = float(row["timestamp"])

    voltages = [row["voltage_uV"] for row in data]

    print("\n=== EEG ANALYSIS ===")
    print(f"Total samples:   {len(data)}")
    print(f"Duration:        {data[-1]['timestamp']:.1f} seconds")
    print(f"Max voltage:     {max(voltages):.2f} μV")
    print(f"Min voltage:     {min(voltages):.2f} μV")
    print(f"Mean voltage:    {sum(voltages) / len(voltages):.2f} μV")

    return data


# Putting it all together
# Full pipeline: simulate → save → analyze

metadata = {
    "subject": "Subject_042",
    "sample_rate": 250,
    "duration": 10,
    "condition": "resting_state",
}

eeg_data = simulate_eeg_recording(duration_sec=10, sample_rate=250)
save_eeg_data("eeg_recording_001.csv", eeg_data, metadata)
results = analyze_eeg_file("eeg_recording_001.csv")
print()
