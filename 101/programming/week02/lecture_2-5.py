voltages = [-70, -68, -65, -60, -57, -54, -70, -65]
threshold = -55

print("Finding first spike above threshold...")

for i, v in enumerate(voltages):
    if v >= 0 or v < -90:
        continue  # Implausible reading — likely noise, skip it

    if v >= threshold:
        print(f"First spike at t={i} ms (V={v} mV)")
        break  # Found it — no need to scan the rest

print("Scan complete.")
