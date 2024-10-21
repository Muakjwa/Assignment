import neurodynex3.ojas_rule.oja as oja
import matplotlib.pyplot as plt
import numpy as np

cloud0 = oja.make_cloud(n=1000, ratio=0.4, angle=-45)
cloud = (3,5)+cloud0

cloud2 = np.zeros((1000,2))

cloudnorm = ((cloud0[:,0])**2 + cloud0[:,1]**2)**0.5
cloud2[:,0] = cloud0[:,0] / cloudnorm
cloud2[:,1] = cloud0[:,1] / cloudnorm

cloud2s = cloud2 +(3,5)

#wcourse = oja.learn(cloud, initial_angle=-20, eta=0.2)

for i in range(1):
    wcourse = oja.learn(cloud,  eta=0.04)
    #wcourse = oja.learn(cloud,  eta=0.2)

    plt.scatter(cloud[:, 0], cloud[:, 1], marker=".", alpha=.2)
    plt.scatter(cloud2[:, 0], cloud2[:, 1], marker=".", alpha=.3)
    plt.plot(wcourse[0, 0], wcourse[0, 1], "or", markersize=5, label='init') # adding init..
    plt.plot(wcourse[-1, 0], wcourse[-1, 1], "or", markersize=10,label='end')
    plt.legend()
    plt.axis('equal')


    wnorm = ((wcourse[:,0])**2 + wcourse[:,1]**2)**0.5
    #print(wnorm)


    plt.figure()
    plt.plot(wcourse[:, 0], "g", label='w1')
    plt.plot(wcourse[:, 1], "b", label='w2')
    plt.plot(wnorm[:], "r", label='w')
    plt.legend()

    y = wcourse[-1,0]*cloud2s[:,0]+wcourse[-1,1]*cloud2s[:,1]
    plt.figure()
    plt.plot(y)

    plt.show()
    print("The final weight vector w is: ({},{})".format(wcourse[-1,0],wcourse[-1,1]))

    ymax = np.max(y)
    ymin = np.min(y)

    print("Max y = ",format(ymax))
    print("Min y = ",format(ymin))

