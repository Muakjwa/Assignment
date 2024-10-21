import neurodynex3.ojas_rule.oja as oja
import matplotlib.pyplot as plt
#import numpy as np

cloud = oja.make_cloud(n=200, ratio=0.3, angle=60)

#wcourse = oja.learn(cloud, initial_angle=-20, eta=0.2)

for i in range(3):
    wcourse = oja.learn(cloud,  eta=0.04)
    #wcourse = oja.learn(cloud,  eta=0.2)

    plt.scatter(cloud[:, 0], cloud[:, 1], marker=".", alpha=.2)
    plt.plot(wcourse[0, 0], wcourse[0, 1], "or", markersize=5, label='init') # adding init..
    plt.plot(wcourse[-1, 0], wcourse[-1, 1], "or", markersize=10,label='end')
    plt.legend()
    plt.axis('equal')
    plt.figure()


    wnorm = ((wcourse[:,0])**2 + wcourse[:,1]**2)**0.5
    #print(wnorm)

    plt.plot(wcourse[:, 0], "g", label='w1')
    plt.plot(wcourse[:, 1], "b", label='w2')
    plt.plot(wnorm[:], "r", label='w')
    plt.legend()
    plt.show()
    print("The final weight vector w is: ({},{})".format(wcourse[-1,0],wcourse[-1,1]))
