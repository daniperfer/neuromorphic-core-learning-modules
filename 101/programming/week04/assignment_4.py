# Assignment 4: Neuron Network Class
# Student Name: [YOUR NAME]
# Date: [DATE]


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

        Parameters
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

        Parameters
        ----------
        name : str
            A descriptive name for this network.
        """
        # TODO: Initialize instance attributes
        # Hint: you need self.name, self.neurons (empty list), self.simulation_time
        pass

    def add_neuron(self, neuron):
        """
        Add a neuron to the network.

        Parameters
        ----------
        neuron : Neuron
            The neuron object to add.
        """
        # TODO: Append neuron to self.neurons
        pass

    def remove_neuron(self, neuron_id):
        """
        Remove a neuron from the network by ID.

        Parameters
        ----------
        neuron_id : int
            The ID of the neuron to remove.

        Returns
        -------
        bool
            True if the neuron was found and removed, False if not found.
        """
        # TODO: Search for neuron with matching ID
        # TODO: Remove it and return True if found, return False if not
        # Hint: don't modify a list while iterating over it —
        #       build a new list using a list comprehension instead
        pass

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
        # TODO: Loop through self.neurons and return the match
        # TODO: Return None if no match is found
        pass

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
        # TODO: Loop over range(duration)
        # TODO: At each timestep, call update() on every neuron
        # TODO: Update self.simulation_time
        # TODO: Return results dictionary
        pass

    def get_total_spikes(self):
        """
        Return the total spike count across all neurons.

        Returns
        -------
        int
            Sum of spike_count for every neuron in the network.
        """
        # TODO: Sum spike_count across all neurons
        pass

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
        # TODO: Handle the edge case of an empty network
        # TODO: Calculate and return the statistics dictionary
        pass

    def __str__(self):
        """
        Concise human-readable description.

        Example: "Network 'Visual Cortex': 5 neurons, 47 total spikes"
        """
        # TODO: Return a formatted string matching the example format
        pass

    def __repr__(self):
        """
        Technical representation for debugging.

        Example: NeuronNetwork(name='Visual Cortex', neurons=5, total_spikes=47, sim_time=100ms)
        """
        # TODO: Return a detailed representation
        pass


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
    # Add at least 2 test cases of your own below.
    # Ideas: test an empty network, add neurons of different types,
    # run multiple simulations back to back, try edge-case inputs.
