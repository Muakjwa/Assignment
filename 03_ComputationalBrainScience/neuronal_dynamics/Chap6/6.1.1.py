import numpy as np
import matplotlib.pyplot as plt


x = np.arange(-2.5, 2.51, .1)  # create an array of x values
y = -x**3 + x + 0  # calculate the function values for the given x values
plt.plot(x, y, color='black')  # plot y as a function of x
plt.xlim(-2.5, 2.5)  # constrain the x limits of the plot

x = np.arange(-2.5, 2.51, .1)  # create an array of x values
y = 2*x + 2  # calculate the function values for the given x values
plt.plot(x, y, color='blue')  # plot y as a function of x
plt.show()
