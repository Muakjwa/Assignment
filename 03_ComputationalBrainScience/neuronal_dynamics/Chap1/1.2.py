
import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.leaky_integrate_and_fire import LIF
from neurodynex3.tools import input_factory, plot_tools


plt.figure()  # new figure

#neuron = NeuronClass()  # instantiate the neuron class

I = np.arange(0.0,50.0,2.0)  # a range of current inputs
f = []

# loop over current values

for I_amp in I:

    step_current = input_factory.get_step_current(t_start=10, t_end=1010, unit_time=b2.ms, amplitude=I_amp*b2.namp)
    state_monitor, spike_monitor = LIF.simulate_LIF_neuron(step_current, simulation_time=1100 * b2.ms,firing_threshold=LIF.FIRING_THRESHOLD)
    #plot_tools.plot_voltage_and_current_traces(state_monitor, step_current, title="min input", firing_threshold=LIF.FIRING_THRESHOLD)
    #plt.show()
    firing_rate = spike_monitor.count[0]
    #firing_rate = 2.0 * spike_monitor.count[0]
    f.append(firing_rate)

plt.plot(I, f)
plt.xlabel('Amplitude of Injecting step current (nA)')
#plt.ylabel('Firing rate (Hz)')
plt.ylabel('# of firing')
plt.grid()
plt.show()
