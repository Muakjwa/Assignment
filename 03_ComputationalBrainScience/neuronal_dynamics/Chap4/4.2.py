import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory
#passive_cable.getting_started()


t_spikes = [100, 150, 200]
l_spikes = [100. * b2.um, 200. * b2.um, 300. * b2.um]
current = input_factory.get_spikes_current(t_spikes, 10*b2.us, 0.8*b2.namp, append_zero=True)

voltage_monitor, cable_model = passive_cable.simulate_passive_cable(length=0.8 * b2.mm, current_injection_location=l_spikes, input_current=current, nr_compartments=100, simulation_time= 5 * b2.ms)

#print("Time unit=",b2.defaultclock.dt)

# 4.2.0
plt.figure()
plt.imshow(voltage_monitor.v / b2.volt)
plt.colorbar(label="voltage")
plt.xlabel("time index")
plt.ylabel("location index")
plt.title("vm at (t,x), raw data voltage_monitor.v")
plt.show()

