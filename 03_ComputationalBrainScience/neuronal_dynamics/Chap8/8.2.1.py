import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.tools import input_factory, plot_tools, spike_tools
from neurodynex3.neuron_type import neurons


# create an input current
I_amp=0.38
input_current = input_factory.get_step_current(100, 1100, 1.*b2.ms, I_amp*b2.pA)

a_neuron_of_type_X = neurons.NeuronX()  # we do not know if it's type I or II
state_monitor = a_neuron_of_type_X.run(input_current, 1200*b2.ms)
spike_times = spike_tools.get_spike_time(state_monitor, 1.*b2.mV)
print(spike_times)
#print(type(spike_times))
print(len(spike_times))
isi=spike_times[1:]-spike_times[:-1]
print(isi)
ave_isi=np.average(isi)
print(ave_isi)
rate=1.0/ave_isi
print(rate)

# provide nr_of_spike, spike_times, isi, mean_isi, spike_rate)
st=spike_tools.pretty_print_spike_train_stats(state_monitor, 1.*b2.mV)
print(st)
neurons.plot_data(state_monitor, title="Neuron of Type X")
