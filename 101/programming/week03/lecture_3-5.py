"""
Lecture 3.5: Variable Scope — Where Variables Live and Why It Matters
"""

threshold = -55.0


def adjust_threshold():
    """
    This creates a NEW local variable, not modifying the global!
    """
    threshold = -50.0  # This creates a NEW local variable, not modifying the global!
    #  it looks like you changed something, but you didn’t.
    print(f"Inside function: {threshold}")


adjust_threshold()
print(f"Outside function: {threshold}")


# Global recording parameters
threshold = -55.0
dt = 1.0


# Neuroscience Application: Why This Matters in Practice
def simulate_neuron(V_start, I_input, steps=100):
    """
    Simulate a neuron for a fixed number of time steps.
    Returns the voltage trace as a list.
    """
    V = V_start
    trace = []  # Local — this list belongs to this function call only

    for _ in range(steps):
        dV = I_input * dt  # Reads global dt — fine, it's just a lookup
        V = V + dV
        trace.append(V)

        if V >= threshold:  # Reads global threshold — fine
            break

    return trace  # Returns the result — does NOT modify anything global


def count_spikes(trace, thresh=-55.0):
    """Count threshold crossings in a voltage trace."""
    count = 0
    for v in trace:
        if v >= thresh:
            count += 1
    return count


# Main analysis
trace_a = simulate_neuron(-70.0, I_input=2.0)
trace_b = simulate_neuron(-70.0, I_input=5.0)

spikes_a = count_spikes(trace_a)
spikes_b = count_spikes(trace_b)

print(f"Neuron A: {spikes_a} threshold crossings")
print(f"Neuron B: {spikes_b} threshold crossings")
