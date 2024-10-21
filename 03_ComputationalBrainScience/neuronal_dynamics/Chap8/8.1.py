import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.tools import input_factory, plot_tools, spike_tools
from neurodynex3.neuron_type import neurons

# create an input current
input_current = input_factory.get_step_current(50, 150, 1.*b2.ms, 0.5*b2.pA)

a = neurons.neurontype_random_reassignment()
#print( a )
#print( a )
#random_type = neurons.neurontype_random_reassignment()
#print(random_type)
#state_monitor = random_type.run(input_current, 200*b2.ms)
# plot state vs. time
#neurons.plot_data(state_monitor, title="Neuron of Random type")

#a_neuron_of_type_Y = neurons.NeuronY()  # we do not know if it's type I or II
#state_monitor = a_neuron_of_type_Y.run(input_current, 200*b2.ms)
#neurons.plot_data(state_monitor, title="Neuron of Type Y")
