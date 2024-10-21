import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.tools import input_factory, plot_tools, spike_tools
from neurodynex3.neuron_type import neurons

I=np.arange(0.3,0.6,0.02)
f=[]
a_neuron_of_type_X = neurons.NeuronX()  # we do not know if it's type I or II

for I_amp in I :
    input_current = input_factory.get_step_current(100, 1100, 1.*b2.ms, I_amp*b2.pA)

    state_monitor = a_neuron_of_type_X.run(input_current, 1200*b2.ms)
    # provide nr_of_spike, spike_times, isi, mean_isi, spike_rate)
    st=spike_tools.pretty_print_spike_train_stats(state_monitor, 1.*b2.mV)
    #print(st)
    print("0=",st[0])
    #print("1=",st[1])
    #print("2=",st[2])
    print("3=",st[3])
    f.append(st[3])

plt.plot(I, f)
plt.xlabel('Amplitude of Injecting step current (pA)')
plt.ylabel('Firing rate (Hz)')
plt.grid()
plt.show()
