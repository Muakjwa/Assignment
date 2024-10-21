import brian2 as b2
import numpy as np
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory
#passive_cable.getting_started()


current = input_factory.get_step_current(1000, 1100, unit_time=b2.us, amplitude= 0.8 * b2.namp)

voltage_monitor, cable_model = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=[0.2 * b2.mm], input_current=current, nr_compartments=100, simulation_time= 3 * b2.ms)

#print("Time unit=",b2.defaultclock.dt)

#plt.figure()
#plt.imshow(voltage_monitor.v / b2.volt)
#plt.colorbar(label="voltage")
#plt.xlabel("time index")
#plt.ylabel("location index")
#plt.title("vm at (t,x), raw data voltage_monitor.v")
#plt.show()

### 4.1.3

x = np.arange(1,100)  # a range of current inputs

plt.plot(x/0.123,voltage_monitor.v[x,100]/b2.mV, label='t=1.0ms')
plt.plot(x/0.123,voltage_monitor.v[x,110]/b2.mV, label='t=1.1ms')
plt.plot(x/0.123,voltage_monitor.v[x,120]/b2.mV, label='t=1.2ms')
plt.plot(x/0.123,voltage_monitor.v[x,130]/b2.mV, label='t=1.3ms')
plt.plot(x/0.123,voltage_monitor.v[x,140]/b2.mV, label='t=1.4ms')
plt.plot(x/0.123,voltage_monitor.v[x,150]/b2.mV, label='t=1.5ms')
plt.plot(x/0.123,voltage_monitor.v[x,160]/b2.mV, label='t=1.6ms')

plt.xlabel("location (um)")
plt.ylabel("Voltage (mV)")

plt.legend()
plt.show()


