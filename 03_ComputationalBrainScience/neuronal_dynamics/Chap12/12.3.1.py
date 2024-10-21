import brian2 as b2
from neurodynex3.tools import plot_tools
from neurodynex3.competing_populations import decision_making
import matplotlib.pyplot as plt

results = decision_making.sim_decision_making_network(t_stimulus_start= 50. * b2.ms, coherence_level=-0.6, max_sim_time=1000. * b2.ms)
#plot_tools.plot_network_activity(results["rate_monitor_A"], results["spike_monitor_A"],results["voltage_monitor_A"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Left")
#plot_tools.plot_network_activity(results["rate_monitor_B"], results["spike_monitor_B"],results["voltage_monitor_B"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Right")
#plot_tools.plot_network_activity(results["rate_monitor_Z"], results["spike_monitor_Z"],results["voltage_monitor_Z"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Z")
#plot_tools.plot_network_activity(results["rate_monitor_inhib"], results["spike_monitor_inhib"],results["voltage_monitor_inhib"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Inhibit")

avg_window_width = 100*b2.ms
srA100 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
srB100 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz


plt.plot(srA100, srB100, label = '')

plt.xlim([0,60])
plt.ylim([0,60])

plt.xlabel('Population rate Left')
plt.ylabel('Population rate Right')

plt.legend()
plt.show()
