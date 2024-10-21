import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.hodgkin_huxley import HH
from neurodynex3.tools import input_factory


I_min=2.5
current = input_factory.get_step_current(5, 7, b2.ms, I_min *b2.uA)
state_monitor = HH.simulate_HH_neuron(current, 30 * b2.ms)
HH.plot_data(state_monitor, title="HH Neuron, minimal current")
plt.show()
