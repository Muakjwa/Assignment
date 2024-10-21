import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory
#passive_cable.getting_started()

t_spikes = [100, 150, 200]
l_spikes = [100. * b2.um, 200. * b2.um, 300. * b2.um]
current = input_factory.get_spikes_current(t_spikes, 10*b2.us, 0.8*b2.namp, append_zero=True)

voltage_monitor1, cable_model1 = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=l_spikes, input_current=current, nr_compartments=100, simulation_time= 5 * b2.ms)

t_spikes = [100, 150, 200]
l_spikes = [300. * b2.um, 200. * b2.um, 100. * b2.um]
current = input_factory.get_spikes_current(t_spikes, 10*b2.us, 0.8*b2.namp, append_zero=True)

voltage_monitor2, cable_model2 = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=l_spikes, input_current=current, nr_compartments=100, simulation_time= 5 * b2.ms)

#print("Time unit=",b2.defaultclock.dt)

## 4.2.3 plot together

plt.figure()
probe_location = 0.0 * b2.mm
v1 = voltage_monitor1[cable_model1.morphology[probe_location]].v
plt.plot(voltage_monitor1.t/b2.ms, v1/b2.mV, label='0(first)')

probe_location = 0.0 * b2.mm
v2 = voltage_monitor2[cable_model2.morphology[probe_location]].v
plt.plot(voltage_monitor2.t/b2.ms, v2/b2.mV, label='0(second)')

plt.xlabel("time (ms)")
plt.ylabel("Voltage (mV)")
plt.legend()
plt.show()

