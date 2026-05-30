# Assignment 4: Neuron Network Class
# Student Name: Daniel Pereira
# Date: May 30, 2026


class Neuron:
    """Simple integrate-and-fire neuron for network simulations."""

    def __init__(self, neuron_id, neuron_type="excitatory"):
        self.id = neuron_id
        self.type = neuron_type
        self.voltage = -70.0
        self.threshold = -55.0
        self.spike_count = 0

    def update(self, I_input):
        """
        Apply one timestep of input current.

        Params
        ----------
        I_input : float
            Input current. Positive values depolarize the membrane.

        Returns
        -------
        bool
            True if the neuron fired this timestep.
        """
        self.voltage += I_input

        if self.voltage >= self.threshold:
            self.spike_count += 1
            self.voltage = -70.0  # Reset after spike
            return True

        # Passive leak toward rest
        self.voltage += (-70.0 - self.voltage) * 0.1
        return False

    def __str__(self):
        return f"Neuron {self.id} ({self.type}): {self.spike_count} spikes"

    def __repr__(self):
        return (
            f"Neuron(id={self.id}, type='{self.type}', "
            f"V={self.voltage:.1f}mV, spikes={self.spike_count})"
        )


class NeuronNetwork:
    """
    A network of neurons.

    Manages a collection of Neuron objects, coordinates simulation,
    and reports population-level statistics.
    """

    def __init__(self, name):
        """
        Initialize the network.

        Params
        ----------
        name : str
            A descriptive name for this network.
        """
        # Initialize instance attributes
        self.name = name
        self.neurons: list[Neuron] = []
        self.simulation_time = 0

    def add_neuron(self, neuron):
        """
        Add a neuron to the network.

        Params
        ----------
        neuron : Neuron
            The neuron object to add.
        """
        # Append neuron to self.neurons
        self.neurons.append(neuron)

    def remove_neuron(self, neuron_id):
        """
        Remove a neuron from the network by ID.

        Params
        ----------
        neuron_id : int
            The ID of the neuron to remove.

        Returns
        -------
        bool
            True if the neuron was found and removed, False if not found.
        """
        # Remove neuron with matching ID and return True if found, return False if not
        previous_len = len(self.neurons)
        self.neurons = [n for n in self.neurons if n.id != neuron_id]
        current_len = len(self.neurons)
        return True if (current_len < previous_len) else False

    def get_neuron(self, neuron_id):
        """
        Look up a neuron by ID.

        Parameters
        ----------
        neuron_id : int
            The ID to search for.

        Returns
        -------
        Neuron or None
            The matching Neuron object, or None if not found.
        """
        # Loop through self.neurons and return the match
        # Return None if no match is found
        matching_neurons = [n for n in self.neurons if n.id == neuron_id]
        return matching_neurons[0] if (len(matching_neurons) > 0) else None

    def simulate(self, duration, input_current):
        """
        Run the simulation for a given duration.

        Applies input_current to every neuron at every timestep.
        Updates self.simulation_time when complete.

        Parameters
        ----------
        duration : int
            Number of timesteps to simulate.
        input_current : float
            Current applied to all neurons at each timestep.

        Returns
        -------
        dict
            A results dictionary with keys:
            - 'duration': the number of timesteps simulated
            - 'total_spikes': total spikes across all neurons
            - 'spike_counts': list of per-neuron spike counts
        """
        # Loop over range(duration)
        # At each timestep, call update() on every neuron
        # Update self.simulation_time
        # Return results dictionary
        # results = {"duration"=duration, "total_spikes":0, "spike_counts":[0]*len(self.neurons)}
        for t in range(duration):
            for neur in self.neurons:
                neur.update(input_current)
        self.simulation_time += duration
        results = {
            "duration": duration,
            "total_spikes": self.get_total_spikes(),
            "spike_counts": [neur.spike_count for neur in self.neurons],
        }
        return results

    def get_total_spikes(self):
        """
        Return the total spike count across all neurons.

        Returns
        -------
        int
            Sum of spike_count for every neuron in the network.
        """
        # Sum spike_count across all neurons
        total_spikes = 0
        for neur in self.neurons:
            total_spikes += neur.spike_count
        return total_spikes

    def get_network_stats(self):
        """
        Compute population-level statistics.

        Returns
        -------
        dict
            Dictionary with keys:
            - 'num_neurons': number of neurons in the network
            - 'total_spikes': total spikes across all neurons
            - 'avg_spikes': mean spikes per neuron (float, 1 decimal place)
            - 'max_spikes': highest spike count of any single neuron
            - 'min_spikes': lowest spike count of any single neuron
        """
        # Handle the edge case of an empty network
        # Calculate and return the statistics dictionary
        spikes_counts = [neur.spike_count for neur in self.neurons]
        empty = len(spikes_counts) <= 0
        statistics = {
            "num_neurons": len(self.neurons),
            "total_spikes": self.get_total_spikes(),
            "avg_spikes": 0 if empty else 1.0 * self.get_total_spikes() / len(self.neurons),
            "max_spikes": 0 if empty else max(spikes_counts),
            "min_spikes": 0 if empty else min(spikes_counts),
        }
        return statistics

    def __str__(self):
        """
        Concise human-readable description.

        Example: "Network 'Visual Cortex': 5 neurons, 47 total spikes"
        """
        # Return a formatted string matching the example format
        return (
            f"Network {self.name}: {len(self.neurons)} neurons, "
            f"{self.get_total_spikes()} total spikes"
        )

    def __repr__(self):
        """
        Technical representation for debugging.

        Example: NeuronNetwork(name='Visual Cortex', neurons=5, total_spikes=47, sim_time=100ms)
        """
        # Return a detailed representation
        return (
            f"NeuronNetwork(name={self.name}, neurons='{len(self.neurons)}', "
            f"total_spikes={self.get_total_spikes()}, sim_time={self.simulation_time})"
        )


# ── Test code ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # --- Test 1: Build the network ---
    print("=== Test 1: Building the network ===")
    net = NeuronNetwork("Visual Cortex")

    for i in range(5):
        net.add_neuron(Neuron(i, "excitatory"))

    print(net)  # Should show 5 neurons, 0 spikes
    print()

    # --- Test 2: Run simulation ---
    print("=== Test 2: Simulation ===")
    results = net.simulate(duration=100, input_current=2.0)
    print("Simulation complete.")
    print(f"Total spikes: {net.get_total_spikes()}")
    print()

    # --- Test 3: Network statistics ---
    print("=== Test 3: Statistics ===")
    stats = net.get_network_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()

    # --- Test 4: Neuron lookup ---
    print("=== Test 4: Neuron lookup ===")
    found = net.get_neuron(2)
    if found:
        print(f"Found: {found}")
    missing = net.get_neuron(99)
    print(f"get_neuron(99): {missing}")  # Should print None
    print()

    # --- Test 5: Remove a neuron ---
    print("=== Test 5: Remove neuron ===")
    removed = net.remove_neuron(2)
    print(f"Removed neuron 2: {removed}")  # True
    not_found = net.remove_neuron(99)
    print(f"Removed neuron 99: {not_found}")  # False
    print(net)  # Should show 4 neurons
    print()

    # --- Your additional test cases go here ---
    print("=== Your Additional Tests ===")
    print()
    # Add at least 2 test cases of your own below.
    # Ideas: test an empty network, add neurons of different types,
    # run multiple simulations back to back, try edge-case inputs.

    # --- Aditional Test ---------------------------------------
    print("=== Test 6: Empty network ===")
    empty_net = NeuronNetwork("Empty network")
    print(empty_net)  # Should show 0 neurons, 0 spikes
    results = empty_net.simulate(duration=10, input_current=1.0)
    print("Simulation complete.")
    print("Results:")
    for key, value in results.items():
        print(f"  {key}: {value}")
    print("Statistics:")
    stats = empty_net.get_network_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()

    # --- Aditional Test ---------------------------------------
    print("=== Test 7: Remove two neurons with same ID ===")
    net_test = NeuronNetwork("Test 7")
    net_test.add_neuron(Neuron(1, "pyramidal"))
    net_test.add_neuron(Neuron(2, "excitatory"))
    net_test.add_neuron(Neuron(2, "pyramidal"))
    net_test.add_neuron(Neuron(3, "excitatory"))
    print(net_test)  # 4 neurons
    # Remove all neuron with ID=2
    removed = net_test.remove_neuron(2)
    print(f"Removed neuron 2: {removed}")  # True
    found = net.get_neuron(2)
    print(f"get_neuron(2): {found}")  # Should print None
    print(net_test)  # 2 neurons
    print()

    # --- Aditional Test ---------------------------------------
    print("=== Test 8: Input current 0 produces no spikes ===")
    results = net_test.simulate(100, 0.0)
    print("Simulation complete.")
    print("Results:")
    for key, value in results.items():
        print(f"  {key}: {value}")
    print("Statistics:")
    stats = net_test.get_network_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()


"""
My approach and design decisions:

Method remove_neuron(self, neuron_id):
After removing a neuron, the neuron list should be shorter.
Therefore, I use the length of the neuron list to infer whether a neuron was removed.
If there are several neurons with the same ID, the method removes all of them.

Method get_network_stats():
I used a boolen variable ("empty") to check if the list if empty, so as to
call max() and min() functions depending on that variable.

Method simulate(self, duration, input_current):
I call the method self.get_total_spikes() from inside the method simulate, thus
simplyfing the code avoiding to repeat the same logic again.
"""
