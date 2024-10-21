
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
input_current = input_factory.get_step_current(
    t_start=20, t_end=320, unit_time=b2.ms, amplitude=0.8 * b2.namp)

state_monitor, spike_monitor = exp_IF.simulate_exponential_IF_neuron(
    v_spike=exp_IF.FIRING_THRESHOLD_v_spike,I_stim=input_current, simulation_time=350*b2.ms)

plot_tools.plot_voltage_and_current_traces(
    state_monitor, input_current,title="step current",
    firing_threshold=exp_IF.FIRING_THRESHOLD_v_spike)
print("nr of spikes: {}".format(spike_monitor.count[0]))
plt.show()
