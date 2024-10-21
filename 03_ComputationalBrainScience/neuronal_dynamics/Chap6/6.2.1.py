import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.phase_plane_analysis import fitzhugh_nagumo

#fitzhugh_nagumo.plot_flow()
#trajectory = fitzhugh_nagumo.get_trajectory(0,0,1.3)

I_ext=0.0
#u0=0.0
#w0=0.0


def get_jacobian(u0):
    return [[1-3*u0*u0, -1], [0.1,-0.05]]

fixed_point = fitzhugh_nagumo.get_fixed_point(I_ext)
#fixed_point = fitzhugh_nagumo.get_fixed_point()


print("u0=",fixed_point[0])
u0=fixed_point[0]
J=get_jacobian(u0)
print("Jacobian=",J)

ev=np.linalg.eigvals(J)
print("Eigenvalue=",ev)
