"""
Lecture 6.1: Introduction to File Handling
"""

"""
# Read the entire file into one string
with open("neuron_data.txt", "r") as file:
    content = file.read()
    print(content)

# Read line by line — useful for large files that don't fit in memory
with open("neuron_data.txt", "r") as file:
    for line in file:
        print(line.strip())   # strip() removes the \n at the end of each line

# Read all lines into a list at once
with open("neuron_data.txt", "r") as file:
    lines = file.readlines() # readlines() preserves the newline character \n at the end
    print(lines)   # ['line1\n', 'line2\n', ...]

# Read one line at a time, manually
with open("neuron_data.txt", "r") as file:
    first_line = file.readline()
    second_line = file.readline()
"""

# Save a list of spike times, one per line
spike_times = [10.5, 23.1, 45.7, 67.2, 89.0]

with open("spike_output.txt", "w") as file:
    for spike in spike_times:
        file.write(f"{spike}\n")  # \n moves to the next line

print("Spike times saved!\n")


def save_recording_session(filename, neuron_id, spike_times, duration):
    """Save a complete recording session to a text file."""
    with open(filename, "w") as file:
        file.write("RECORDING SESSION LOG\n")
        file.write("=" * 40 + "\n")
        file.write(f"Neuron ID: {neuron_id}\n")
        file.write(f"Duration: {duration} seconds\n")
        file.write(f"Total Spikes: {len(spike_times)}\n")
        file.write(f"Firing Rate: {len(spike_times) / duration:.1f} Hz\n")
        file.write("\nSpike Times (ms):\n")
        for i, spike in enumerate(spike_times, 1):
            file.write(f"  Spike {i:3d}: {spike:.2f} ms\n")

    print(f"Session saved to {filename}")


def load_recording_session(filename):
    """Load and display a recording session."""
    print(f"\nLoading: {filename}")
    print("-" * 40)
    with open(filename, "r") as file:
        content = file.read()
        print(content)


# Try it out
spike_data = [10.5, 23.1, 45.7, 67.2, 89.0, 102.3, 118.9]
save_recording_session("session_001.txt", "N042", spike_data, 10)
load_recording_session("session_001.txt")
