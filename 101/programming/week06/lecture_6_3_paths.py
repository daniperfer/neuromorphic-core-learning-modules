"""
Lecture 6.3: File Paths and Organization
"""

import csv
import os

# Don't do this — it's fragile
path = "data/session_01/spikes.csv"

# Do this instead — works on any OS
path = os.path.join("data", "session_01", "spikes.csv")
print(path)
# Mac/Linux: data/session_01/spikes.csv
# Windows:   data\session_01\spikes.csv
print()

# Where is Python running right now?
print(os.getcwd())  # e.g., /home/brad/neuroscience

# Build a path relative to the current directory
data_folder = "data"
filename = "spikes.csv"
full_path = os.path.join(data_folder, filename)
print(full_path)  # data/spikes.csv
print()

# Does this file exist?
if os.path.exists("neurons.csv"):
    print("File found — proceeding with analysis.")
else:
    print("File not found — check the path.")

# Is this path a directory (folder) rather than a file?
if os.path.isdir("data"):
    print("Data folder is present.")
print()


# Creating a Folder Structure for an Experiment
def setup_experiment_folders(experiment_name):
    """Create a standard folder structure for a new experiment."""
    folders = [
        f"experiments/{experiment_name}",
        f"experiments/{experiment_name}/raw_data",
        f"experiments/{experiment_name}/processed",
        f"experiments/{experiment_name}/results",
        f"experiments/{experiment_name}/figures",
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)  # exist_ok=True: don't error if it already exists
        print(f"Created: {folder}")

    return f"experiments/{experiment_name}"


# Set up a new experiment
exp_dir = setup_experiment_folders("lecture_6-3_files")
print(f"\nExperiment directory ready: {exp_dir}")
print()

# List everything in a directory
all_files = os.listdir(exp_dir)
print(f"All files in {exp_dir}/: {all_files}")

# Filter to only CSV files
csv_files = [f for f in os.listdir(exp_dir) if f.endswith(".csv")]
print(f"CSV files: {csv_files}")
csv_files = [f for f in all_files if f.endswith(".csv")]
print(f"CSV files: {csv_files}")

# os.walk() descends into subdirectories recursively
# Walk the entire experiments folder and find every file
for root, dirs, files in os.walk("experiments"):
    for file in files:
        full_path = os.path.join(root, file)
        print(full_path)
print()


"""
A Practical Pattern: Processing All Files in a Folder
"""


def process_all_sessions(data_dir):
    """Load and summarize all CSV session files in a directory."""
    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return

    print(f"Found {len(csv_files)} session files.\n")

    for filename in sorted(csv_files):
        filepath = os.path.join(data_dir, filename)

        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        print(f"{filename}: {len(rows)} rows")


process_all_sessions(f"{exp_dir}/raw_data")
print()
