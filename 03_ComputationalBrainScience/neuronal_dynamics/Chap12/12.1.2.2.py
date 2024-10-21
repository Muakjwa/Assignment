import brian2 as b2
from neurodynex3.tools import plot_tools
from neurodynex3.competing_populations import decision_making
import matplotlib.pyplot as plt

results = decision_making.sim_decision_making_network(t_stimulus_start= 50. * b2.ms, coherence_level=0.1, max_sim_time=1000. * b2.ms)

plot_tools.plot_network_activity(results["rate_monitor_A"], results["spike_monitor_A"],results["voltage_monitor_A"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Left")
plot_tools.plot_network_activity(results["rate_monitor_B"], results["spike_monitor_B"],results["voltage_monitor_B"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Right")
#plot_tools.plot_network_activity(results["rate_monitor_Z"], results["spike_monitor_Z"],results["voltage_monitor_Z"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Z")
#plot_tools.plot_network_activity(results["rate_monitor_inhib"], results["spike_monitor_inhib"],results["voltage_monitor_inhib"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Inhibit")

avg_window_width = 10*b2.ms
srA10 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
srB10 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
avg_window_width = 50*b2.ms
srA50 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
srB50 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
avg_window_width = 100*b2.ms
srA100 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
srB100 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
avg_window_width = 150*b2.ms
srA150 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
srB150 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
avg_window_width = 200*b2.ms
srA200 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
srB200 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
avg_window_width = 300*b2.ms
srA300 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
srB300 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz


fig, sr  = plt.subplots(2)

sr[0].plot(srA10, label = 'width=10')
sr[0].plot(srA50, label = 'width=50')
sr[0].plot(srA100, label = 'width=100')
sr[0].plot(srA150, label = 'width=150')
sr[0].plot(srA200, label = 'width=200')
sr[0].plot(srA300, label = 'width=300')

sr[1].plot(srB10, label = 'width=10')
sr[1].plot(srB50, label = 'width=50')
sr[1].plot(srB100, label = 'width=100')
sr[1].plot(srB150, label = 'width=150')
sr[1].plot(srB200, label = 'width=200')
sr[1].plot(srB300, label = 'width=300')

plt.legend()
plt.show()
