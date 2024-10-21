import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.leaky_integrate_and_fire import LIF
from neurodynex3.tools import input_factory, plot_tools

LIF.V_REST = -70*b2.mV
LIF.V_RESET = -65*b2.mV
LIF.FIRING_THRESHOLD = -50*b2.mV
LIF.MEMBRANE_RESISTANCE = 10. * b2.Mohm
LIF.MEMBRANE_TIME_SCALE = 8. * b2.ms
LIF.ABSOLUTE_REFRACTORY_PERIOD = 2.0 * b2.ms

#print("resting potential: {}".format(LIF.V_REST))

I_amp=3.0
step_current = input_factory.get_step_current(t_start=5, t_end=100, unit_time=b2.ms, amplitude=I_amp*b2.namp)  # set I_min to your value
state_monitor, spike_monitor = LIF.simulate_LIF_neuron(step_current, simulation_time=200 * b2.ms,firing_threshold=LIF.FIRING_THRESHOLD)

plot_tools.plot_voltage_and_current_traces(state_monitor, step_current, title="min input", firing_threshold=LIF.FIRING_THRESHOLD)
print("nr of spikes: {}".format(spike_monitor.count[0])) 
plt.show()
