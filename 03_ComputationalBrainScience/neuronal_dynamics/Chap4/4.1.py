import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory
#passive_cable.getting_started()


current = input_factory.get_step_current(1000, 1100, unit_time=b2.us, amplitude= 0.8 * b2.namp)

voltage_monitor, cable_model = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=[0.2 * b2.mm], input_current=current, nr_compartments=100, simulation_time= 3 * b2.ms)

#print("Time unit=",b2.defaultclock.dt)

plt.figure()
plt.imshow(voltage_monitor.v / b2.volt)
plt.colorbar(label="voltage")
plt.xlabel("time index")
plt.ylabel("location index")
plt.title("vm at (t,x), raw data voltage_monitor.v")
plt.show()

### 4.1.2

probe_location = 0.0 * b2.mm
v1 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v1/b2.mV, label='0')

probe_location = 0.1 * b2.mm
v2 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v2/b2.mV, label='100')

probe_location = 0.2 * b2.mm
v3 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v3/b2.mV, label='200')

probe_location = 0.3 * b2.mm
v4 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v4/b2.mV, label='300')

probe_location = 0.4 * b2.mm
v5 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v5/b2.mV, label='400')

probe_location = 0.5 * b2.mm
v6 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v6/b2.mV, label='500')

probe_location = 0.6 * b2.mm
v7 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v7/b2.mV, label='600')

plt.xlabel("time (ms)")
plt.ylabel("Voltage (mV)")

plt.legend()
plt.show()

