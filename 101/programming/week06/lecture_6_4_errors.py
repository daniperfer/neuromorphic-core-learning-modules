"""
Lecture 6.4: Error Handling for Files
"""
import csv
import os
import shutil

"""
try:
    with open("neuron_data.txt", "r") as file:
        content = file.read()
    print("File loaded successfully.")

except FileNotFoundError:
    print("Error: that file doesn't exist. Check the filename and path.")

except PermissionError:
    print("Error: Python doesn't have permission to read that file.")

except Exception as e:
    print(f"Something unexpected went wrong: {e}")
"""


def safe_load_csv(filename):
    """
    Load a CSV file with comprehensive error handling.
    Returns a list of dicts on success, or None if loading fails.
    """
    # Check existence before trying to open — gives a clearer error message
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found.")
        print(f"  Running from: {os.getcwd()}")
        print(f"  Files here: {os.listdir('.')}")
        return None

    # Catch empty files before the CSV reader sees them
    if os.path.getsize(filename) == 0:
        print(f"Error: '{filename}' is empty.")
        return None

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)

        if not data:
            print(f"Warning: '{filename}' has a header but no data rows.")
            return []

        print(f"Loaded {len(data)} rows from '{filename}'.")
        return data

    except csv.Error as e:
        print(f"CSV format error in '{filename}': {e}")
        return None

    except Exception as e:
        print(f"Unexpected error loading '{filename}': {e}")
        return None


# Using the function safely
data = safe_load_csv("neurons.csv")

if data is not None:
    print(f"Processing {len(data)} neurons...")
else:
    print("Cannot proceed — file loading failed.")
print()


# Saving Files Safely
def safe_save_csv(filename, data, fieldnames, overwrite=False):
    """
    Save data to a CSV file, with optional overwrite protection and backup.
    Returns True on success, False on failure.
    """
    # If file already exists and overwrite isn't explicitly allowed, ask
    if os.path.exists(filename) and not overwrite:
        print(f"Warning: '{filename}' already exists.")
        response = input("Overwrite? (yes/no): ").strip().lower()
        if response != "yes":
            print("Save cancelled.")
            return False

        # Create a backup before overwriting
        backup_name = filename.replace(".csv", "_backup.csv")
        shutil.copy(filename, backup_name)
        print(f"Backup saved as '{backup_name}'.")

    try:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"Saved {len(data)} rows to '{filename}'.")
        return True

    except PermissionError:
        print(f"Error: no permission to write to '{filename}'.")
        return False

    except Exception as e:
        print(f"Unexpected error saving '{filename}': {e}")
        return False


print()


def process_session_files(data_dir):
    """Process all CSV files in a directory, logging any failures."""
    csv_files = sorted(f for f in os.listdir(data_dir) if f.endswith(".csv"))

    if not csv_files:
        print(f"No CSV files found in '{data_dir}'.")
        return

    results = []
    failed = []

    for filename in csv_files:
        filepath = os.path.join(data_dir, filename)
        data = safe_load_csv(filepath)

        if data is None:
            failed.append(filename)
            continue  # Skip to the next file — don't stop the whole run

        # Process the file
        spike_counts = [int(row["spike_count"]) for row in data]
        avg_spikes = sum(spike_counts) / len(spike_counts)
        results.append({"file": filename, "avg_spikes": avg_spikes})

    # Summary
    print(f"\nProcessed {len(results)} of {len(csv_files)} files.")
    if failed:
        print(f"Failed files ({len(failed)}):")
        for f in failed:
            print(f"  {f}")


print()
