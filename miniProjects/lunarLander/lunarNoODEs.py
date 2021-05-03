#Connor Willans
#Unit 1 Project
#Lunar Landing Game

from vpython import *
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import ode

def keyCheck():
    global Fboost
    k = keysdown()
    if 'left' in k:
        if 'right' not in k:
            if 'up' not in k:
                Fboost=bstAmt*vec(-1,0,0) #solo-left
                fuel.size.y = fuel.size.y - fuelloss
            else:
                Fboost=bstAmt*vec(-1,1.2,0) #up-left
                fuel.size.y = fuel.size.y - fuelloss
    elif 'right' in k:
        if 'left' not in k:
            if 'up' not in k:
                Fboost=bstAmt*vec(1,0,0) #solo-right
                fuel.size.y = fuel.size.y - fuelloss
            else:
                Fboost=bstAmt*vec(1,1.2,0) #up-right
                fuel.size.y = fuel.size.y - fuelloss
    elif 'up' in k:
        if 'left' not in k:
            if 'right' not in k:
                Fboost=bstAmt*vec(0,1.2,0) #solo-up
                fuel.size.y = fuel.size.y - fuelloss
    else:
        Fboost=vec(0,0,0) #no-input
    print(k)

def boom():
    boomSize = 0.1
    boom = sphere(pos=vec(lander.pos.x,lander.pos.y,lander.pos.z), size=vec(boomSize,boomSize,boomSize), color=vec(1,0.5,0))
    tboom = 0
    while tboom < 10:
        rate(100)
        boom.size =vec(boomSize+1*tboom,boomSize+1*tboom,boomSize+1*tboom)
        tboom = tboom + 1
    lander.size=vec(0.001,0.001,0.001)
    while tboom > 0:
        rate(100)
        boom.size =vec(boomSize-1*tboom,boomSize-1*tboom,boomSize-1*tboom)
        tboom = tboom - 1
    boom.size=vec(0.001,0.001,0.001)

#scene setup
scene1 = canvas(center = vector(0,30,0), title="\t\t\t\t\t- Connor Willans - Lunar Lander -\n\t\t\t\t\tClick to start - Use the Arrow Keys to move\n\t\t\t\t\tLand with a speed less than 3.0 Unit/Second")
#walls
Bot_Wall = box(pos=vec(0, 0, 0), size=vec(40.5,1,0.1), color=color.white)
Top_Wall = box(pos=vec(0, 60, 0), size=vec(40.5,1,0.1), color=color.white)
Left_Wall = box(pos=vec(-20, 30, 0), size=vec(1,60.5,0.1), color=color.white)
Right_Wall = box(pos=vec(20, 30, 0), size=vec(1,60.5,0.1), color=color.white)
#lander
lander = box(pos=vec(-0, 55, 0), size=vec(2.5, 2.5, 0.1), color=color.orange, shininess=0, mass =100, vel = vec(0,0,0))
#ground
ground = box(pos=vec(0,5,0), size=vec(39,9.5,.1), color=vec(.65,.65,.65))
#spot
spot = box(pos=vec(0,9,0), size=vec(4.5,1.5,0.1), color=color.red)
#randomize lander & spot
rand1 = rand.randrange(-17,17,1)
lander.pos.x = rand1
rand2 = rand.randrange(-17,17,1)
spot.pos.x = rand2
#stars
lcv = 0
while lcv < 40:
    star = sphere(pos=vec(rand.randrange(-19,19,1),rand.randrange(10,59,1),-3), size=vec(.5,.5,.5), color=color.white)
    lcv = lcv + 1
#fuel
fuel = box(pos=vec(24,30,0), size=vec(3,60.5,0.1), color = color.red, shininess=0,)
fuelloss = .04


#more vars
grav = vec(0,-1.62,0)
Fboost=vec(0,0,0)

bstAmt = 170 #used in keyCheck for Fbooost

t = 0 #indep var
h = 0.01 #time step
#lander.vel.x #depend var?
#lander.vel.y #depend var?

xarray = np.array([lander.pos.x, lander.vel.x, lander.pos.y, lander.vel.y])

Nsteps = 5000

time = np.zeros(Nsteps)
xpos = np.zeros(Nsteps)
ypos = np.zeros(Nsteps)
xvel = np.zeros(Nsteps)
yvel = np.zeros(Nsteps)

inc = 1 #increment var for arrays

#begin
scene1.pause()

while lander.pos.y > 11:
    rate(100)
    if fuel.size.y > 0:
        keyCheck()
    else:
        Fboost = vec(0,0,0)


    if lander.pos.x > 18 or lander.pos.x < -18:
        lander.vel.x = 0

    #xarray = ode.RK4(diffeq,xarray,t,h)

    dxdt = np.zeros(4)

    Fgrav = lander.mass*grav
    Fnet = Fgrav+Fboost

    dxdt[1] = lander.vel.x+Fnet.x/lander.mass*h
    dxdt[0] = lander.pos.x + dxdt[1]*h

    dxdt[3] = lander.vel.y+Fnet.y/lander.mass*h
    dxdt[2] = lander.pos.y + dxdt[3]*h

    lander.pos.x = dxdt[0]
    lander.vel.x = dxdt[1]
    lander.pos.y = dxdt[2]
    lander.vel.y = dxdt[3]

    print("Speed = ", abs(lander.vel.y)," Units/Sec")

    t = t+h

    time[inc] = t
    xpos[inc] = dxdt[0]
    xvel[inc] = dxdt[1]
    ypos[inc] = dxdt[2]
    yvel[inc] = dxdt[3]
    inc = inc + 1

#ending
flag_spot = False
flag_speed = False

#spot
if abs(lander.pos.x) < abs(spot.pos.x):
    if (abs(spot.pos.x) - abs(lander.pos.x)) < 2.5:
        print("You landed within the target")
        flag_spot = True
    else:
        boom()
        print("You did not on the target")
else:
    if (abs(lander.pos.x) - abs(spot.pos.x)) < 2.5:
        print("You landed within the target")
        flag_spot = True
    else:
        boom()
        print("You did not on the target")


#speed
if abs(lander.vel.y) > 3.0:
    boom()
    print("\nYou did not land with a speed of less than 3.0 units/sec\n")
    print("Final Speed = ", abs(lander.vel.y)," Units/Sec")
else:
    print("You landed in the target with a speed of less than 3.0 units/sec")
    print("Final Speed = ", abs(lander.vel.y)," Units/Sec")
    flag_speed = True

#final-check
if flag_spot is True and flag_speed is True:
    Bot_Wall.color = color.green
    Top_Wall.color = color.green
    Left_Wall.color = color.green
    Right_Wall.color = color.green
    print("\nCongrats! - You Win\n")
else:
    Bot_Wall.color = color.red
    Top_Wall.color = color.red
    Left_Wall.color = color.red
    Right_Wall.color = color.red

fig = plt.figure()
plt.title("Y-Velocity vs Time")
plt.plot(time,yvel, 'b-', label='y-vel')
plt.xlabel('t (s)')
plt.ylabel('y-vel (units/sec)')
plt.legend()
plt.show()


