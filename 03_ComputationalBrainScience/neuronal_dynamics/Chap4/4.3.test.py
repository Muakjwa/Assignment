import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory


current = input_factory.get_step_current(50, 60, unit_time=b2.us, amplitude= 0.8 * b2.namp)

b2.defaultclock.dt = 0.005 * b2.ms

voltage_monitor1, cable_model1 = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=[0.4 * b2.mm], input_current=current, nr_compartments=100, simulation_time= 0.2 * b2.ms)

voltage_monitor2, cable_model2 = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=[0.4 * b2.mm], input_current=current, nr_compartments=100, simulation_time= 0.2 * b2.ms, r_transversal = 5.0 * b2.Mohm * b2.mm ** 2, capacitance = 0.2 * b2.uF / b2.cm ** 2)

## 4.3

plt.figure()
probe_location = 0.5 * b2.mm
v1 = voltage_monitor1[cable_model1.morphology[probe_location]].v
plt.plot(voltage_monitor1.t/b2.ms, v1/b2.mV, label='R=1.25MOh,C=0.8')
v2 = voltage_monitor2[cable_model2.morphology[probe_location]].v
plt.plot(voltage_monitor2.t/b2.ms, v2/b2.mV, label='R=5MOhm, C=0.2')

plt.xlabel("time (ms)")
plt.ylabel("Voltage (mV)")
plt.legend()
plt.show()

