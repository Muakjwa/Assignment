#matplotlib inline
import matplotlib.pyplot as plt
from neurodynex3.hopfield_network import network, pattern_tools, plot_tools

pattern_size = 4

# create an instance of the class HopfieldNetwork
hopfield_net = network.HopfieldNetwork(nr_neurons= pattern_size**2)


#Visualize the weight matrix
plot_tools.plot_network_weights(hopfield_net)
#plt.show()

# instantiate a pattern factory
factory = pattern_tools.PatternFactory(pattern_size, pattern_size)

# create a checkerboard pattern and add it to the pattern list
#checkerboard = factory.create_checkerboard()
checkerboard = factory.create_checkerboard()
L_pattern = factory.create_L_pattern()
pattern_list = [checkerboard,L_pattern]

##Visualize the weight matrix after defining checkboard
###plot_tools.plot_network_weights(hopfield_net)

# add random patterns to the list
#pattern_list.extend(factory.create_random_pattern_list(nr_patterns=3, on_probability=0.5))
#pattern_list.extend(factory.create_random_pattern_list(nr_patterns=5, on_probability=0.5))
plot_tools.plot_pattern_list(pattern_list)
# how similar are the random patterns and the checkerboard? Check the overlaps
overlap_matrix = pattern_tools.compute_overlap_matrix(pattern_list)
#plot_tools.plot_overlap_matrix(overlap_matrix)

# let the hopfield network "learn" the patterns. Note: they are not stored
# explicitly but only network weights are updated !
hopfield_net.store_patterns(pattern_list)


#Visualize the weight matrix after defining checkboard
plot_tools.plot_network_weights(hopfield_net)
plt.show()

plt.figure()
plt.hist(hopfield_net.weights.flatten())
plt.show()

# create a noisy version of a pattern and use that to initialize the network
#noisy_init_state = pattern_tools.flip_n(checkerboard, nr_of_flips=4)
#noisy_init_state = pattern_tools.flip_n(checkerboard, nr_of_flips=3)
#hopfield_net.set_state_from_pattern(noisy_init_state)



# from this initial state, let the network dynamics evolve.
#states = hopfield_net.run_with_monitoring(nr_steps=4)

# each network state is a vector. reshape it to the same shape used to create the patterns.
#states_as_patterns = factory.reshape_patterns(states)
# plot the states of the network
#plot_tools.plot_state_sequence_and_overlap(states_as_patterns, pattern_list, reference_idx=0, suptitle="Network dynamics")
