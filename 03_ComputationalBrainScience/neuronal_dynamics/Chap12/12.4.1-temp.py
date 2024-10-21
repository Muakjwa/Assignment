import brian2 as b2
from neurodynex3.tools import plot_tools
from neurodynex3.competing_populations import decision_making
import matplotlib.pyplot as plt
import numpy as np

def get_decision_time(monitorA, monitorB,avg_window_width,rate_threshold):
    srA=monitorA.smooth_rate(window="flat",width=avg_window_width) / b2.Hz
    srB=monitorB.smooth_rate(window="flat",width=avg_window_width) / b2.Hz
    idx_A=np.argmax(srA > rate_threshold/b2.Hz)
    idx_B=np.argmax(srB > rate_threshold/b2.Hz)
    t_A = idx_A * b2.defaultclock.dt
    t_B = idx_B * b2.defaultclock.dt
    print(t_A,t_B)

    return t_A,t_B

coherence_levels = [-0.1, -0.5]  # for negative values, B is the correct decision.
nr_repetitions = 3

rate_threshold=10.0*b2.Hz
ave_window_width=10.0*b2.Hz

time_to_A, time_to_B, count_A, count_B, count_No = decision_making.run_multiple_simulations(get_decision_time(monitorA,monitorB,avg_window_width, rate_threshold),coherence_levels, nr_repetitions, max_sim_time=1000. *b2.ms, rate_threshold=10.0*b2*Hz, avg_window_width=100*b2.ms)
#time_to_A, time_to_B, count_A, count_B, count_No = decision_making.run_multiple_simulations(coherence_levels, nr_repetitions, max_sim_time=1000. *b2.ms, rate_threshold=10.0*b2*Hz, avg_window_width=100*b2.ms)

print(time_to_A)


#results = decision_making.sim_decision_making_network(t_stimulus_start= 50. * b2.ms, coherence_level=-0.6, max_sim_time=1000. * b2.ms)
#plot_tools.plot_network_activity(results["rate_monitor_A"], results["spike_monitor_A"],results["voltage_monitor_A"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Left")
#plot_tools.plot_network_activity(results["rate_monitor_B"], results["spike_monitor_B"],results["voltage_monitor_B"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Right")
#plot_tools.plot_network_activity(results["rate_monitor_Z"], results["spike_monitor_Z"],results["voltage_monitor_Z"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Z")
#plot_tools.plot_network_activity(results["rate_monitor_inhib"], results["spike_monitor_inhib"],results["voltage_monitor_inhib"], t_min=0. * b2.ms, avg_window_width=2. * b2.ms,sup_title="Inhibit")



#avg_window_width = 100*b2.ms
#rate_threshold=10.0*b2.Hz
#srA100 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
#srB100 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz


#det=get_decision_time(results["rate_monitor_A"], results["rate_monitor_B"], avg_window_width, rate_threshold)
#print(det)

#plt.xlim([0,60])
#plt.ylim([0,60])

#plt.xlabel('Population rate Left')
#plt.ylabel('Population rate Right')

#plt.plot(srA100, srB100, label = 'width=100')

#plt.legend()
#plt.show()
