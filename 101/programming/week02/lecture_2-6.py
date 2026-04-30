rows = 3
cols = 3

print("Neural network grid:")

for row in range(rows):
    for col in range(cols):
        neuron_id = row * cols + col  # Convert 2D position to a unique ID
        """
        The print() with end=" " suppresses the newline that print() normally adds, 
        so all the neurons in a row appear on the same line. 
        The bare print() at the end of the outer loop then adds the newline between rows. 
        This is a small but useful formatting trick.
        """
        print(f"[{neuron_id}]", end=" ")
    print()  # Move to a new line after finishing each row

print()

num_neurons = 4

print("Synaptic connections:")
print("(1 = connected, 0 = not connected)\n")

for pre in range(num_neurons):       # pre = the sending neuron
    for post in range(num_neurons):  # post = the receiving neuron
        if pre == post:
            connected = 0  # A neuron doesn't connect to itself
        else:
            connected = 1  # All other pairs are connected
        print(connected, end=" ")
    print()  # New row after each pre-synaptic neuron
