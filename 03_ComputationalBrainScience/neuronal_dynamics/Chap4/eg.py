import brian2 as b2
import matplotlib.pyplot as plt
from neurodynex3.cable_equation import passive_cable
from neurodynex3.tools import input_factory
passive_cable.getting_started()


#current = input_factory.get_step_current(500, 510, unit_time=b2.us, amplitude=3. * b2.namp)
#voltage_monitor, cable_model = passive_cable.simulate_passive_cable(length=0.5 * b2.mm, current_injection_location=[0.1 * b2.mm], input_current=current,nr_compartments=100, simulation_time=2 * b2.ms)

#plt.plot(voltage_monitor.t/b2.ms, voltage_monitor[0].v/b2.mV, label='0')
#plt.plot(voltage_monitor.t/b2.ms, voltage_monitor[10].v/b2.mV,label='10')
#plt.plot(voltage_monitor.t/b2.ms, voltage_monitor[30].v/b2.mV,label='30')
#plt.legend()
#plt.show()
