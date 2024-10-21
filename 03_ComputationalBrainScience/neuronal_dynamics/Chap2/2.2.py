
import brian2 as b2
import matplotlib.pyplot as plt
import neurodynex3.exponential_integrate_fire.exp_IF as exp_IF
from neurodynex3.tools import plot_tools, input_factory

#default value (we can change..)

exp_IF.MEMBRANE_TIME_SCALE_tau = 12.0 * b2.ms
exp_IF.MEMBRANE_RESISTANCE_R = 20.0 * b2.Mohm
exp_IF.V_REST = -65.0 * b2.mV
exp_IF.V_RESET = -60.0 * b2.mV
exp_IF.RHEOBASE_THRESHOLD_v_rh = -55.0 * b2.mV
exp_IF.SHARPNESS_delta_T = 2.0 * b2.mV

# Threshold change Not working at any points... why?? changing working around -30 lower... => looks like resolution due to quite big values...
exp_IF.FIRING_THRESHOLD_v_spike = -30.0 * b2.mV

# Irh = 0.4 namp
#===============================================================

i=0  #change i and find the value that goes into min_amp
durations = [1,   2,    5,  10,   20,   50, 100]
#min_amp =   [0., 4.42, 0., 1.10, .70, .48, 0.]
min_amp =   [8.58, 4.42, 1.93, 1.10, .70, .48, 0.43]

t=durations[i]
I_amp = min_amp[i]*b2.namp
title_txt = "I_amp={}, t={}".format(I_amp, t*b2.ms)

input_current = input_factory.get_step_current(t_start=10, t_end=10+t-1, unit_time=b2.ms, amplitude=I_amp)

state_monitor, spike_monitor = exp_IF.simulate_exponential_IF_neuron(I_stim=input_current, simulation_time=(t+20)*b2.ms)


plot_tools.plot_voltage_and_current_traces(state_monitor, input_current,
                                           title=title_txt, firing_threshold=exp_IF.FIRING_THRESHOLD_v_spike,
                                          legend_location=2)
print("nr of spikes: {}".format(spike_monitor.count[0]))

#plt.xlim([0,t+20])
plt.show()

plt.plot(durations, min_amp)
#plt.loglog(durations, min_amp)
plt.title("Strength-Duration curve")
plt.xlabel("t [ms]")
plt.ylabel("min amplitude [nAmp]")
plt.grid()
plt.show()
