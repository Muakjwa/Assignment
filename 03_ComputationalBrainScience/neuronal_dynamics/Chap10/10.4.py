from neurodynex3.brunel_model import LIF_spiking_network
from neurodynex3.tools import plot_tools, spike_tools
import brian2 as b2
import matplotlib.pyplot as plt

# Specify the parameters of the desired network state (e.g. SI fast)
poisson_rate = 20.0 *b2.Hz
g = 3
CE = 5000

# Specify the signal and simulation properties:
delta_t = 0.1 * b2.ms
delta_f = 5.0 * b2.Hz
T_init = 100.0 * b2.ms
k = 5

# compute the remaining values:
f_max = 5000.0 * b2.Hz
N_samples = 5000
T_signal = 500.0 * b2.ms
T_sim = k * T_signal + T_init

# replace the XXXX by appropriate values:

print("Start simulation. T_sim={}, T_signal={}, N_samples={}".format(T_sim, T_signal, N_samples))
b2.defaultclock.dt = delta_t
# for technical reason (solves rounding issues), we add a few extra samples:
stime = T_sim + (10 + k) * b2.defaultclock.dt
rate_monitor, spike_monitor, voltage_monitor, monitored_spike_idx = \
    LIF_spiking_network.simulate_brunel_network(
        N_Excit=CE, poisson_input_rate=poisson_rate, g=g, sim_time=stime)

#plot_tools.plot_network_activity(rate_monitor, spike_monitor, voltage_monitor,spike_train_idx_list=monitored_spike_idx, t_min=0*b2.ms)
#plt.show()
#plot_tools.plot_network_activity(rate_monitor, spike_monitor, voltage_monitor,spike_train_idx_list=monitored_spike_idx, t_min=T_sim - 100 *b2.ms)
#plt.show()
#spike_stats = spike_tools.get_spike_train_stats(spike_monitor, window_t_min= T_init)
#plot_tools.plot_ISI_distribution(spike_stats, hist_nr_bins= 100, xlim_max_ISI= 100 *b2.ms)
#plt.show()

##  Power Spectrum => looks not working...
pop_freqs, pop_ps, average_population_rate = spike_tools.get_population_activity_power_spectrum(rate_monitor, delta_f, k, T_init) # This part is not working, Have no idea...
#pop_freqs, pop_ps, average_population_rate = spike_tools.get_population_activity_power_spectrum(rate_monitor, delta_f, k, 100.0*b2.ms)
#plot_tools.plot_population_activity_power_spectrum(pop_freqs, pop_ps, 1 *b2.Hz, average_population_rate)
#plt.show()
#freq, mean_ps, all_ps, mean_firing_rate, all_mean_firing_freqs = \
#    spike_tools.get_averaged_single_neuron_power_spectrum(
#        spike_monitor, sampling_frequency=1./delta_t, window_t_min= T_init,
#        window_t_max=T_sim, nr_neurons_average= XXXX )
#plot_tools.plot_spike_train_power_spectrum(freq, mean_ps, all_ps, max_freq= XXXX * b2.Hz,
#                                           mean_firing_freqs_per_neuron=all_mean_firing_freqs,
#                                           nr_highlighted_neurons=2)
print("done")
