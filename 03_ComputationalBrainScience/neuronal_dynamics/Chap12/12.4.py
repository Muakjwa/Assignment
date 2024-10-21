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
    #print(t_A,t_B)

    return t_A,t_B

for i in range(10):


    #results = decision_making.sim_decision_making_network(t_stimulus_start= 50. * b2.ms, coherence_level=-0.6, max_sim_time=1000. * b2.ms)
    results = decision_making.sim_decision_making_network(t_stimulus_start= 50. * b2.ms, coherence_level=0.1, max_sim_time=1000. * b2.ms)

    avg_window_width = 100*b2.ms
    rate_threshold=10.0*b2.Hz
    srA100 = results["rate_monitor_A"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
    srB100 = results["rate_monitor_B"].smooth_rate(window="flat", width=avg_window_width)/b2.Hz
    det=get_decision_time(results["rate_monitor_A"], results["rate_monitor_B"], avg_window_width, rate_threshold)
    print(det)

#plt.xlim([0,60])
#plt.ylim([0,60])

#plt.xlabel('Population rate Left')
#plt.ylabel('Population rate Right')

#plt.plot(srA100, srB100, label = 'width=100')

#plt.legend()
#plt.show()
