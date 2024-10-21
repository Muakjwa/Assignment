import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.phase_plane_analysis import fitzhugh_nagumo

#fitzhugh_nagumo.plot_flow()
#plt.figure()
trajectory = fitzhugh_nagumo.get_trajectory(0,0,1.3)

x = np.arange(-2.5, 2.51, .1)  # create an array of x values
y = -x**3 + x + 1.3  # calculate the function values for the given x values
plt.plot(x, y, color='black', label='u nullcline')  # plot y as a function of x

x = np.arange(-2.5, 2.51, .1)  # create an array of x values
y = 2*x + 2  # calculate the function values for the given x values
plt.plot(x, y, color='blue', label='w nullcline')  # plot y as a function of x

plt.plot(trajectory[1], trajectory[2], label='FN - u/w' )
plt.xlim(-1.5, 1.5)  # constrain the x limits of the plot
plt.ylim(-0.5, 2.0)  # constrain the y limits of the plot
plt.xlabel('u')
plt.ylabel('w')

fitzhugh_nagumo.plot_flow(1.3)
plt.show()

