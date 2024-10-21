import matplotlib.pyplot as plt
import numpy as np

ri=8.0
tau=12.0
urh=-55.0
urest =-65.0
u = np.arange(-70.0, -50.0, 0.01)
#u = np.arange(-55.1, -54.9, 0.01)
dT=2

devu0 = 1.0/tau*(urest - u + np.exp((u-urh)/dT)*dT)
devu = 1.0/tau*(urest - u + np.exp((u-urh)/dT)*dT +ri)

#print(u,devu*tau)

plt.plot(u, devu0, label=' I=0 ')
plt.plot(u, devu, label=' I=Irh ')

plt.xlabel('u (mV)')
plt.ylabel('du/dt')
plt.title('test')
plt.grid()
plt.legend()

#fig.savefig("test.png")
plt.show()
