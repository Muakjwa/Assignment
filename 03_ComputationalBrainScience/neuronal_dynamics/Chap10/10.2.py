from neurodynex3.brunel_model import LIF_spiking_network
from neurodynex3.tools import plot_tools
from neurodynex3.tools import spike_tools
import brian2 as b2
import matplotlib.pyplot as plt

# Default parameter of a single LIF neuron
V_REST = 0. * b2.mV
V_RESET = +10. * b2.mV
FIRING_THRESHOLD = +20. * b2.mV
MEMBRANE_TIME_SCALE = 20. * b2.ms
ABSOLUTE_REFRACTORY_PERIOD = 2.0 * b2.ms

# Default parameters of the network
SYNAPTIC_WEIGHT_W0 = 0.1 * b2.mV  # note: w_ee=w_ie = w0 and = w_ei=w_ii = -g*w0
RELATIVE_INHIBITORY_STRENGTH_G = 4.  # balanced
CONNECTION_PROBABILITY_EPSILON = 0.1
SYNAPTIC_DELAY = 1.5 * b2.ms
POISSON_INPUT_RATE = 12. * b2.Hz # vthr default
N_POISSON_INPUT = 1000

#RELATIVE_INHIBITORY_STRENGTH_G = 0.1 

# For SR
#RELATIVE_INHIBITORY_STRENGTH_G = 3.  
#POISSON_INPUT_RATE = 20.0 * b2.Hz 

# For SI-fast
#RELATIVE_INHIBITORY_STRENGTH_G = 6.  
#POISSON_INPUT_RATE = 40. * b2.Hz 

# For AI
#RELATIVE_INHIBITORY_STRENGTH_G = 5.  
#POISSON_INPUT_RATE = 20.0 * b2.Hz 

# For SI-slow
RELATIVE_INHIBITORY_STRENGTH_G = 4.5 
POISSON_INPUT_RATE = 9.0 * b2.Hz 


rate_monitor, spike_monitor, voltage_monitor, monitored_spike_idx = LIF_spiking_network.simulate_brunel_network(sim_time=1000. * b2.ms, N_Excit=6000, N_Inhib=1500, poisson_input_rate=POISSON_INPUT_RATE,g=RELATIVE_INHIBITORY_STRENGTH_G)

plot_tools.plot_network_activity(rate_monitor, spike_monitor, voltage_monitor, spike_train_idx_list=monitored_spike_idx, t_min=0.*b2.ms)
plt.show()
print("Total number of spikes : ",format(spike_monitor.num_spikes))
plot_tools.plot_network_activity(rate_monitor, spike_monitor, voltage_monitor, spike_train_idx_list=monitored_spike_idx, t_min=950.*b2.ms)
plt.show()
plot_tools.plot_network_activity(rate_monitor, spike_monitor, voltage_monitor, spike_train_idx_list=monitored_spike_idx,t_min=0.*b2.ms, t_max=50.*b2.ms)
plt.show()


print(spike_tools.get_spike_train_stats(spike_monitor).nr_spikes)

spike_stats=spike_tools.get_spike_train_stats(spike_monitor,window_t_min=500*b2.ms) # looks not working...
print(format(spike_stats.nr_spikes))
print("CV=",format(spike_stats.CV))

plot_tools.plot_ISI_distribution(spike_stats, hist_nr_bins=100, xlim_max_ISI= 100 *b2.ms)
plt.show()
