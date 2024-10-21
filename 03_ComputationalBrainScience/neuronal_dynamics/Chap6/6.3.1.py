import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np
from neurodynex3.phase_plane_analysis import fitzhugh_nagumo

def get_jacobian(u0):
    return [[1-3*u0*u0, -1], [0.1,-0.05]]

currents = np.arange (0,4,0.1)

for I in currents:
    fixed_point = fitzhugh_nagumo.get_fixed_point(I)
    u0=fixed_point[0]
    J=get_jacobian(u0)
    #print("Jacobian=",J)
    ev=np.linalg.eigvals(J)
    #print("Eigenvalue=",ev)
    print("I=",I, "EV=",ev)
