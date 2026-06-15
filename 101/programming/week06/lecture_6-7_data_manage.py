"""
Lecture 6.7: Building a Data Management System
"""

import csv
import json
import os
import random
from datetime import datetime


class NeuroscienceDataManager:
    """
    A data management system for neuroscience experiments.
    Creates organized directory structures, saves session data,
    and generates summary reports.
    """

    def __init__(self, base_directory="experiments"):
        self.base_dir = base_directory
        os.makedirs(base_directory, exist_ok=True)
        self.experiment_log = []
        print(f"Data manager ready. Working directory: {base_directory}/")

    def create_experiment(self, name, researcher, parameters):
        """
        Create a new experiment with a timestamped directory and JSON metadata.

        Returns:
            tuple of (experiment_id, experiment_directory_path)
        """
        # Generate a unique ID from the current timestamp
        exp_id = f"EXP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        exp_dir = os.path.join(self.base_dir, exp_id)
        os.makedirs(exp_dir, exist_ok=True)

        metadata = {
            "experiment_id": exp_id,
            "name": name,
            "researcher": researcher,
            "created": datetime.now().isoformat(),
            "parameters": parameters,
            "status": "active",
            "n_sessions": 0,
        }

        # Save metadata as JSON — this is the experiment's permanent record
        metadata_file = os.path.join(exp_dir, "metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)

        self.experiment_log.append(exp_id)
        print(f"Experiment created: {exp_id}")
        return exp_id, exp_dir

    def save_session(self, exp_dir, session_num, neuron_data):
        """
        Save one recording session as a numbered CSV file.

        Params:
            exp_dir     -- path to the experiment directory
            session_num -- integer session number (used in filename)
            neuron_data -- list of dicts, one per neuron

        Returns:
            True on success, False if there was nothing to save
        """
        if not neuron_data:
            print(f"Warning: session {session_num} has no data — skipping.")
            return False

        # session_001.csv, session_002.csv, etc.
        session_file = os.path.join(exp_dir, f"session_{session_num:03d}.csv")

        fieldnames = list(neuron_data[0].keys())
        with open(session_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(neuron_data)

        print(f"Session {session_num} saved: {len(neuron_data)} neurons.")
        return True

    def load_all_sessions(self, exp_dir):
        """
        Load every session CSV from an experiment directory.

        Returns:
            dict mapping session name → list of row dicts
        """
        session_files = sorted(
            f for f in os.listdir(exp_dir) if f.startswith("session_") and f.endswith(".csv")
        )

        if not session_files:
            print("No session files found in this experiment directory.")
            return {}

        all_data = {}
        for session_file in session_files:
            filepath = os.path.join(exp_dir, session_file)
            with open(filepath, "r") as f:
                reader = csv.DictReader(f)
                data = list(reader)

            session_name = session_file.replace(".csv", "")
            all_data[session_name] = data
            print(f"Loaded {session_name}: {len(data)} neurons.")

        return all_data

    def generate_report(self, exp_dir):
        """
        Load the experiment metadata and all sessions,
        then write a plain-text summary report.
        """
        # Load experiment metadata
        metadata_file = os.path.join(exp_dir, "metadata.json")
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        # Load all session data
        all_sessions = self.load_all_sessions(exp_dir)

        # Build the report as a list of lines, then join at the end
        lines = [
            "=" * 60,
            f"EXPERIMENT REPORT: {metadata['name']}",
            "=" * 60,
            f"ID:          {metadata['experiment_id']}",
            f"Researcher:  {metadata['researcher']}",
            f"Created:     {metadata['created'][:10]}",  # Date only, not full timestamp
            f"Sessions:    {len(all_sessions)}",
            "",
        ]

        for session_name, data in all_sessions.items():
            lines.append(f"  {session_name}: {len(data)} neurons recorded")

        lines.append("=" * 60)
        report_text = "\n".join(lines)

        # Save and display
        report_file = os.path.join(exp_dir, "report.txt")
        with open(report_file, "w") as f:
            f.write(report_text)

        print(report_text)
        print(f"\nReport saved to: {report_file}")


# Initialize the manager
manager = NeuroscienceDataManager("my_experiments")

# Create a new experiment
exp_id, exp_dir = manager.create_experiment(
    name="Hippocampal Place Cells Study",
    researcher="Dr. Smith",
    parameters={"n_neurons": 10, "duration": 300, "environment": "linear_track"},
)

# Simulate 3 recording sessions
for session_num in range(1, 4):
    session_data = []
    for i in range(10):
        session_data.append(
            {
                "neuron_id": f"N{i:03d}",
                "type": random.choice(["pyramidal", "interneuron"]),
                "spike_count": random.randint(5, 50),
                "avg_firing_rate": round(random.uniform(1, 20), 1),
                "place_field": random.choice([True, False]),
            }
        )
    manager.save_session(exp_dir, session_num, session_data)

# Generate the summary report
print()
manager.generate_report(exp_dir)
print()
