import brian2 as b2
import numpy as np
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory


b2.defaultclock.dt = 0.1 * b2.ms
current = input_factory.get_step_current(0, 0, unit_time=b2.ms, amplitude=0.1 * b2.namp, append_zero=False)

voltage_monitor, cable_model = passive_cable.simulate_passive_cable(length=0.5 * b2.mm, current_injection_location=[0.0 * b2.mm], input_current=current, nr_compartments=100, simulation_time= 100 * b2.ms)

#print("Time unit=",b2.defaultclock.dt)

plt.figure()
plt.imshow(voltage_monitor.v / b2.volt)
plt.colorbar(label="voltage")
plt.xlabel("time index")
plt.ylabel("location index")
plt.title("vm at (t,x), raw data voltage_monitor.v")
plt.show()

## 4.4.1

plt.figure()
probe_location = 0.0 * b2.mm
v1 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v1/b2.mV, label='x=0')

probe_location = 0.495* b2.mm
v2 = voltage_monitor[cable_model.morphology[probe_location]].v
plt.plot(voltage_monitor.t/b2.ms, v2/b2.mV, label='x=500')

plt.xlabel("time (ms)")
plt.ylabel("Voltage (mV)")
plt.legend()
plt.show()

##
plt.figure()
x = np.arange(1,100)  # a range of current inputs

plt.plot(x/0.2,voltage_monitor.v[x,1000-1]/b2.mV, label='t=100ms')
plt.plot(x/0.2,voltage_monitor.v[x,100-1]/b2.mV, label='t=10ms')

plt.xlabel("location (um)")
plt.ylabel("Voltage (mV)")

plt.legend()
plt.show()

