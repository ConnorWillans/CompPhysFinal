#Connor Willans - Unit 3 Project

#Code inspired by Program 5.6 From:
#Computational Modeling and Visualization of
#Physical Systems with Python - Jay Wang

import matplotlib.pyplot as plt
import ode
import numpy as np

#restrict theta between -pi:pi
def restrict(value):
    if (abs(value) > pi):
        if value > 0:
            value = value - 2*pi
        else:
            value = value + 2*pi
    #else - return the original value
    return value

#diffeq for RK4
def DDPendulum(y, t):
    x = -np.sin(y[0]) - damp * y[1] + lcv * np.cos(omegaDrive * t)
    return [y[1], x]

def poincare(burst, numPeriods):
    pts_period = 40

    # init values
    t = 0.0

    #[theta, omega]
    y = [0.6,0.0]

    h = 2*pi/(omegaDrive*pts_period)

    theta = []
    omega = []
    #run through 800 iterations
    for i in range(pts_period*burst):
        t = t+h
        y = ode.RK4n(DDPendulum, y, t, h)
        y[0] = restrict(y[0])

    #store data every period/2 (ie - every 20 times in i)
    for i in range(pts_period*numPeriods):
        if (i%(pts_period//2) == 0):         # record every half a period
            theta.append(y[0])
            omega.append(y[1])
        t = t + h
        y = ode.RK4n(DDPendulum, y, t, h)
        y[0] = restrict(y[0])

    return theta, omega

damp = 0.5
omegaDrive = 0.6
plotNum, pi = 1, np.pi

burst = 20
numPeriods = 400
plt.figure()

for lcv in [0.7, 1.1, 1.2]:
    theta, omega = poincare(burst, numPeriods)

    graph = plt.subplot(3, 1, plotNum)     # 3x1 subplots
    graph.plot(theta, omega, '.')
    graph.set_xlim(-pi, pi)

    if (plotNum == 2):
        graph.set_ylabel('$\\omega$ (rad/s)')
    plotNum = plotNum + 1
    #lcvtxt = '$F_d=$'+repr(lcv)
    graph.text(-3, min(omega), '$F_d=$'+repr(lcv))

plt.xlabel('$\\theta$ (rad)')
plt.show()
