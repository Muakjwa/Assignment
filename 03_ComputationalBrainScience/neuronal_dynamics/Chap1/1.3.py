
import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.leaky_integrate_and_fire import LIF
from neurodynex3.tools import input_factory, plot_tools


# get a random parameter. provide a random seed to have a reproducible experiment
#random_parameters = LIF.get_random_param_set(random_seed=432)
random_parameters = LIF.get_random_param_set(random_seed=120)

# define your test current
I_amp=10.0
test_current = input_factory.get_step_current(t_start=10, t_end=50, unit_time=b2.ms, amplitude= I_amp* b2.namp)

# probe the neuron. pass the test current AND the random params to the function
state_monitor, spike_monitor = LIF.simulate_random_neuron(test_current, random_parameters)

# plot
plot_tools.plot_voltage_and_current_traces(state_monitor, test_current, title="experiment")
plt.show()

# print the parameters to the console and compare with your estimates
# LIF.print_obfuscated_parameters(random_parameters)
