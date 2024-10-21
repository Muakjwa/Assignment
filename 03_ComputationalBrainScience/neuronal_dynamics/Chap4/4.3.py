import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory


current = input_factory.get_step_current(50, 60, unit_time=b2.us, amplitude= 0.8 * b2.namp)

b2.defaultclock.dt = 0.005 * b2.ms

voltage_monitor, cable_model = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=[0.4 * b2.mm], input_current=current, nr_compartments=100, simulation_time= 0.2 * b2.ms)
#voltage_monitor, cable_model = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=[0.4 * b2.mm], input_current=current, nr_compartments=100, simulation_time= 0.2 * b2.ms, r_transversal = 5.0 * b2.Mohm * b2.mm ** 2, capacitance = 0.2 * b2.uF / b2.cm ** 2)

#print("Time unit=",b2.defaultclock.dt)

plt.figure()
plt.imshow(voltage_monitor.v / b2.volt)
plt.colorbar(label="voltage")
plt.xlabel("time index")
plt.ylabel("location index")
plt.title("vm at (t,x), raw data voltage_monitor.v")
plt.show()

## 4.3

plt.figure()
probe_location = 0.5 * b2.mm
v1 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v1/b2.mV, label='0')

plt.xlabel("time (ms)")
plt.ylabel("Voltage (mV)")
plt.legend()
plt.show()

