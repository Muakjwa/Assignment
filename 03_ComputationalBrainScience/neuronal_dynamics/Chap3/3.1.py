import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex3.adex_model import AdEx
from neurodynex3.tools import plot_tools, input_factory

#default : Init bursting
#AdEx.MEMBRANE_TIME_SCALE_tau_m = 5 * b2.ms
#AdEx.MEMBRANE_RESISTANCE_R = 500*b2.Mohm
#AdEx.V_REST = -70.0 * b2.mV
#AdEx.V_RESET = -51.0 * b2.mV
#AdEx.RHEOBASE_THRESHOLD_v_rh = -50.0 * b2.mV
#AdEx.SHARPNESS_delta_T = 2.0 * b2.mV
#AdEx.ADAPTATION_VOLTAGE_COUPLING_a = 0.5 * b2.nS
#AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
#AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 7.0 * b2.pA

# Tonic
AdEx.MEMBRANE_TIME_SCALE_tau_m = 20 * b2.ms
AdEx.ADAPTATION_VOLTAGE_COUPLING_a = 0.0 * b2.nS
AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 30.0 * b2.ms
AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 60.0 * b2.pA
AdEx.V_RESET = -55.0 * b2.mV

# Adapting
AdEx.MEMBRANE_TIME_SCALE_tau_m = 20 * b2.ms
AdEx.ADAPTATION_VOLTAGE_COUPLING_a = 0.0 * b2.nS
AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 5.0 * b2.pA
AdEx.V_RESET = -55.0 * b2.mV

# Init. burst
AdEx.MEMBRANE_TIME_SCALE_tau_m = 5.0 * b2.ms
AdEx.ADAPTATION_VOLTAGE_COUPLING_a = 0.5 * b2.nS
AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 7.0 * b2.pA
AdEx.V_RESET = -51.0 * b2.mV

# Bursting
AdEx.MEMBRANE_TIME_SCALE_tau_m = 5.0 * b2.ms
AdEx.ADAPTATION_VOLTAGE_COUPLING_a = -0.5 * b2.nS
AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 7.0 * b2.pA
AdEx.V_RESET = -46.0 * b2.mV

# Irregular
AdEx.MEMBRANE_TIME_SCALE_tau_m = 9.9 * b2.ms
AdEx.ADAPTATION_VOLTAGE_COUPLING_a = -0.5 * b2.nS
AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 7.0 * b2.pA
AdEx.V_RESET = -46.0 * b2.mV

# Transient
AdEx.MEMBRANE_TIME_SCALE_tau_m = 10.0 * b2.ms
AdEx.ADAPTATION_VOLTAGE_COUPLING_a = 1.0 * b2.nS
AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 10.0 * b2.pA
AdEx.V_RESET = -60.0 * b2.mV

# Delayed
AdEx.MEMBRANE_TIME_SCALE_tau_m = 5.0 * b2.ms
AdEx.ADAPTATION_VOLTAGE_COUPLING_a = -1.0 * b2.nS
AdEx.ADAPTATION_TIME_CONSTANT_tau_w = 100.0 * b2.ms
AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b = 10.0 * b2.pA
AdEx.V_RESET = -60.0 * b2.mV

#current = input_factory.get_step_current(10, 250, 1. * b2.ms, 25.0 * b2.pA) # for dealy
current = input_factory.get_step_current(10, 250, 1. * b2.ms, 65.0 * b2.pA)
state_monitor, spike_monitor = AdEx.simulate_AdEx_neuron(I_stim=current, simulation_time=400 * b2.ms, tau_m =AdEx.MEMBRANE_TIME_SCALE_tau_m, a = AdEx.ADAPTATION_VOLTAGE_COUPLING_a, tau_w =AdEx.ADAPTATION_TIME_CONSTANT_tau_w, b= AdEx.SPIKE_TRIGGERED_ADAPTATION_INCREMENT_b , v_reset= AdEx.V_RESET)



plot_tools.plot_voltage_and_current_traces(state_monitor, current)
print("nr of spikes: {}".format(spike_monitor.count[0]))
plt.show()

AdEx.plot_adex_state(state_monitor)
