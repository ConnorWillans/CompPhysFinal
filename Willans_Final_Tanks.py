#Connor Willans
#Final Project
#Tank  Game

from vpython import *
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import ode
import time

#keyCheck For Aiming / adjusting power / spin / firing
def keyCheck(kcCurPos):
    global ammoPWR  #power on ball/power meter
    global ammoSPN  #spin on ball
    global ammoCNT  #number of shots
    k = keysdown()
    if 'left' in k and kcCurPos > 1:
        aimCannon(kcCurPos-1)
        time.sleep(0.3) #added so user doesn't move more than they meant to
        return kcCurPos-1
    elif 'right' in k and kcCurPos < 9:
        aimCannon(kcCurPos+1)
        time.sleep(0.3) #ignore input for 0.3 seconds
        return kcCurPos+1
    elif ' ' in k:
        if ammoCNT > 0:
            fireTank(kcCurPos)
        ammoCNT = ammoCNT - 1
        return kcCurPos
    elif 'up' in k and ammoPWR < 4:
        powerMeter(ammoPWR+1)
        ammoPWR = ammoPWR + 1
        time.sleep(0.3)
        return kcCurPos
    elif 'down' in k and ammoPWR > 1:
        powerMeter(ammoPWR-1)
        ammoPWR = ammoPWR - 1
        time.sleep(0.3)
        return kcCurPos
    elif '1' in k:
        #backspin
        ammoSPN = 1
        spinMenu()
        time.sleep(0.3)
        return kcCurPos
    elif '2' in k:
        #default/no spin
        ammoSPN = 2
        spinMenu()
        time.sleep(0.3)
        return kcCurPos
    elif '3' in k:
        #topspin
        ammoSPN = 3
        spinMenu()
        time.sleep(0.3)
        return kcCurPos
    else:
        return kcCurPos


def aimCannon(aimCurPos):
    global ammoAGL
    #check for which angle the user has it set to and display correct one
    if aimCurPos == 1:
        ammoAGL = vec(-5,0.5,0)
        tk_pt2.size=vec(0.0001,0.0001,0.0001)
        tk_pt1.size=vec(.25,2,0.1)
    elif aimCurPos == 2:
        ammoAGL = vec(-3,1.4,0)
        tk_pt1.size=vec(0.0001,0.0001,0.0001)
        tk_pt3.size=vec(0.0001,0.0001,0.0001)
        tk_pt2.size=vec(.25,2,0.1)
    elif aimCurPos == 3:
        ammoAGL = vec(-3,1.8,0)
        tk_pt2.size=vec(0.0001,0.0001,0.0001)
        tk_pt4.size=vec(0.0001,0.0001,0.0001)
        tk_pt3.size=vec(.25,2,0.1)
    elif aimCurPos == 4:
        ammoAGL = vec(-2,3,0)
        tk_pt3.size=vec(0.0001,0.0001,0.0001)
        tk_pt5.size=vec(0.0001,0.0001,0.0001)
        tk_pt4.size=vec(.25,2,0.1)
    elif aimCurPos == 5:
        ammoAGL = vec(0.000001,4,0)
        tk_pt4.size=vec(0.0001,0.0001,0.0001)
        tk_pt6.size=vec(0.0001,0.0001,0.0001)
        tk_pt5.size=vec(.25,2,0.1)
    elif aimCurPos == 6:
        ammoAGL = vec(2,3,0)
        tk_pt5.size=vec(0.0001,0.0001,0.0001)
        tk_pt7.size=vec(0.0001,0.0001,0.0001)
        tk_pt6.size=vec(.25,2,0.1)
    elif aimCurPos == 7:
        ammoAGL = vec(3,1.8,0)
        tk_pt6.size=vec(0.0001,0.0001,0.0001)
        tk_pt8.size=vec(0.0001,0.0001,0.0001)
        tk_pt7.size=vec(.25,2,0.1)
    elif aimCurPos == 8:
        ammoAGL = vec(3,1.4,0)
        tk_pt7.size=vec(0.0001,0.0001,0.0001)
        tk_pt9.size=vec(0.0001,0.0001,0.0001)
        tk_pt8.size=vec(.25,2,0.1)
    elif aimCurPos == 9:
        ammoAGL = vec(5,0.5,0)
        tk_pt8.size=vec(0.0001,0.0001,0.0001)
        tk_pt9.size=vec(.25,2,0.1)

def powerMeter(powerLVL):
    #check which level power the user inputed and display it
    if powerLVL == 1:
        power1.size = vec(10,5,0.1)
        power2.size = vec(10,5,0)
    elif powerLVL == 2:
        power2.size = vec(10,5,0.1)
        power3.size = vec(10,5,0)
    elif powerLVL == 3:
        power3.size = vec(10,5,0.1)
        power4.size = vec(10,5,0)
    elif powerLVL == 4:
        power4.size = vec(10,5,0.1)

def spinMenu():
    #check which spin and display properly
    if ammoSPN == 1:
        #back
        topspin.color = vec(0.7,0.7,0.7)
        backspin.color = color.green
        nospin.color = vec(0.7,0.7,0.7)
    if ammoSPN == 2:
        #none
        backspin.color = vec(0.7,0.7,0.7)
        nospin.color = color.green
        topspin.color = vec(0.7,0.7,0.7)
    if ammoSPN ==3:
        #top
        backspin.color = vec(0.7,0.7,0.7)
        topspin.color = color.green
        nospin.color = vec(0.7,0.7,0.7)

def deriv(d, t):
        #calcs for RK4 ODE solver
        x = d[0]
        y = d[1]
        z = d[2]
        vx = d[3]
        vy = d[4]
        vz = d[5]

        #backspin - more y less x
        if ammoSPN == 1:
            w = vec(0.01,0.01,1)
        #no spin
        if ammoSPN == 2:
            w = vec(1,1,1)
        #topspin - more x less y
        if ammoSPN == 3:
            w = vec(-0.1,0.1,1)

        vel = vec(vx,vy,vz)
        S = r*mag(w)/mag(vel)
        C_L = 0.62*S**0.7

        Fmagnus = 0.5 * C_L*p*A*r/S*cross(w,vel)

        b = 10
        vrel = vel - ammoWIND
        Fair = -b*mag(vrel)*vrel

        #final calcs
        Fgrav = m*grav
        Fnet = Fgrav + Fmagnus + Fair

        derivatives = np.zeros(len(d))
        derivatives[0] = vx
        derivatives[1] = vy
        derivatives[2] = vz
        derivatives[3] = Fnet.x/m
        derivatives[4] = Fnet.y/m
        derivatives[5] = Fnet.z/m

        return derivatives


def fireTank(fireCurPos):
    global ammoY
    global timeY
    global callPLT
    ammoLand = vec(0,0,0)
    flag_fire = 0
    if flag_fire == 0:
        #creating the shot each time the tank is fired
        ammo = sphere(pos=vec(tk_pt5.pos.x,tk_pt5.pos.y,0.1), size=vec(1,1,0.1), vel=ammoAGL*(ammoPWR*3.2), color=color.white)
        ammo.vel.z = 0.01

        fireT = 0
        fireDT = 0.01
    flag_fire += 1
    data = np.array([ammo.pos.x, ammo.pos.y, ammo.pos.z, ammo.vel.x, ammo.vel.y, ammo.vel.z])

    while fireT < 15:
        global ammoVEC
        global timeVEC
        rate(100)

        data = ode.RK4(deriv, data, fireT, fireDT)
        ammo.pos = vec(data[0], data[1], data[2])
        ammo.vel = vec(data[3], data[4], data[5])

        #record data for graph on level 1
        if ammoCNT == 3 and currentLevel == 1:
            ammoVEC = np.append(ammoVEC, ammo.vel.y)
            timeVEC = np.append(timeVEC, fireT)
        ammoY = ammo.vel.y
        timeY = fireT

        flag_hit = False


        #flip if reached the wall
        if ammo.pos.x < -30:
            ammo.pos.x = 29.5
        if ammo.pos.x > 30:
            ammo.pos.x = -29.5

        #collision detection-------------------------------------------
        if(currentLevel == 1):
            #land---
            if ammo.pos.y <= 19.9:
                break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
        if(currentLevel == 2):
            #land---
            if ammo.pos.y <= 19.9 and ammo.pos.x <= 10:
                break
            if ammo.pos.x >= 10 and ammo.pos.x <= 20:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= 20 and ammo.pos.x <= 30:
                if ammo.pos.y <= 40:
                    break
            if ammo.pos.x >= 9.8 and ammo.pos.x <= 10.2:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= 19.8 and ammo.pos.x <= 20.2:
                if ammo.pos.y <= 40:
                    break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break

        if(currentLevel == 3):
            #land---
            #left flat
            if ammo.pos.y <= 16 and ammo.pos.x <= -10:
                break
            #peak
            if ammo.pos.x <= -4.8 and ammo.pos.x >= -5.2:
                if ammo.pos.y <= 30:
                    break
            #mountain
            if ammo.pos.x >= -10 and ammo.pos.x <= -9.375:
                if ammo.pos.y <= 17.75:
                    break
            if ammo.pos.x >= -9.375 and ammo.pos.x <= -8.75:
                if ammo.pos.y <= 19.5:
                    break
            if ammo.pos.x >= -8.75 and ammo.pos.x <= -8.125:
                if ammo.pos.y <= 21.25:
                    break
            if ammo.pos.x >= -8.125 and ammo.pos.x <= -7.5:
                if ammo.pos.y <= 23:
                    break
            if ammo.pos.x >= -7.5 and ammo.pos.x <= -6.875:
                if ammo.pos.y <= 24.75:
                    break
            if ammo.pos.x >= -6.875 and ammo.pos.x <= -6.25:
                if ammo.pos.y <= 26.5:
                    break
            if ammo.pos.x >= -6.25 and ammo.pos.x <= -5.625:
                if ammo.pos.y <= 28.25:
                    break
            if ammo.pos.x >= -5.625 and ammo.pos.x <= -5:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= -5 and ammo.pos.x <= -3.875:
                if ammo.pos.y <= 26.85:
                    break
            if ammo.pos.x >= -3.875 and ammo.pos.x <= -2.75:
                if ammo.pos.y <= 23.7:
                    break
            if ammo.pos.x >= -2.75 and ammo.pos.x <= -1.625:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= -1.625 and ammo.pos.x <= -0.5:
                if ammo.pos.y <= 17.4:
                    break
            if ammo.pos.x >= -0.5 and ammo.pos.x <= 0.625:
                if ammo.pos.y <= 14.25:
                    break
            if ammo.pos.x >= 0.625 and ammo.pos.x <= 1.75:
                if ammo.pos.y <= 11.1:
                    break
            if ammo.pos.x >= 1.75 and ammo.pos.x <= 2.875:
                if ammo.pos.y <= 7.95:
                    break
            if ammo.pos.x >= 2.875 and ammo.pos.x <= 4:
                if ammo.pos.y <= 4.8:
                    break
            #pit
            if ammo.pos.x >= 4 and ammo.pos.x <= 13.8:
                if ammo.pos.y <= 4.8:
                    break
            #hill
            if ammo.pos.x >= 13.8 and ammo.pos.x <= 14.55:
                if ammo.pos.y <= 6.025:
                    break
            if ammo.pos.x >= 14.55 and ammo.pos.x <= 15.3:
                if ammo.pos.y <= 7.45:
                    break
            if ammo.pos.x >= 15.3 and ammo.pos.x <= 16.8:
                if ammo.pos.y <= 8.875:
                    break
            #right flat
            if ammo.pos.y <= 10.5 and ammo.pos.x >= 16.8:
                break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break

        if (currentLevel==4):
            #land---
            if ammo.pos.x <= -10 and ammo.pos.y <= 40:
                break
            if ammo.pos.x > -10 and ammo.pos.y <= 3:
                break
            if ammo.pos.x >= -9.9 and ammo.pos.x <= -10.1:
                if ammo.pos.y < 40:
                    break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break

        if (currentLevel==5):
            #land---
            if ammo.pos.y <= 19.9:
                break
            if ammo.pos.x >= 1 and ammo.pos.x <= -1:
                if ammo.pos.y <= 40:
                    break
            if ammo.pos.x >= 0.9 and ammo.pos.x <= 1.1:
                if ammo.pos.y <= 40:
                    break
            if ammo.pos.x >= -0.9 and ammo.pos.x <= -1.1:
                if ammo.pos.y <= 40:
                    break
            if ammo.pos.x >= 3 and ammo.pos.x <= 5:
                if ammo.pos.y <= 35:
                    break
            if ammo.pos.x >= 4.9 and ammo.pos.x <= 5.1:
                if ammo.pos.y <= 35:
                    break
            if ammo.pos.x >= 2.9 and ammo.pos.x <= 3.1:
                if ammo.pos.y <= 35:
                    break
            if ammo.pos.x >= 7 and ammo.pos.x <= 9:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= 6.9 and ammo.pos.x <= 7.1:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= 8.9 and ammo.pos.x <= 9.1:
                if ammo.pos.y <= 30:
                    break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break

        if (currentLevel==6):
            #land---
            if ammo.pos.y <= 5:
                break
            if ammo.pos.x <= -20 and ammo.pos.x >= -30:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= 20 and ammo.pos.x <= 30:
                if ammo.pos.y <= 30:
                    break
            if ammo.pos.x >= -1 and ammo.pos.x <= 1:
                if ammo.pos.y <= 43.5:
                    break
            if ammo.pos.x >= -1 and ammo.pos.x <= 1:
                if ammo.pos.y >= 50:
                    break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break

        if (currentLevel==7):
            #land---
            if ammo.pos.x >= 20 and ammo.pos.y <= 40:
                break
            if ammo.pos.x <= 20 and ammo.pos.x >= -15:
                if ammo.pos.y <= 3:
                    break
            if ammo.pos.x >= -15 and ammo.pos.x <= -20:
                if ammo.pos.y <= 10:
                    break
            if ammo.pos.x >= -20 and ammo.pos.x <= -25:
                if ammo.pos.y <= 20:
                    break
            if ammo.pos.x <= -25 and ammo.pos.y <= 30:
                break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break

        if (currentLevel==8):
            #land---
            if ammo.pos.y <= 8:
                break
            if ammo.pos.x >= 14 and ammo.pos.y <= 20:
                break
            if ammo.pos.x >= 26 and ammo.pos.y <= 33:
                break
            if ammo.pos.x >= 14:
                if ammo.pos.y >= 30 and ammo.pos.y <= 34:
                    break
            if ammo.pos.y >= 38 and ammo.pos.x >= 13:
                break
            #target---
            if ammo.pos.y <= target.pos.y+1.5:
                if ammo.pos.x >= target.pos.x-1.5 and ammo.pos.x <= target.pos.x+1.5:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x-1.6 and ammo.pos.x <= target.pos.x-1.4:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break
            if ammo.pos.y <= target.pos.y+1.5 and ammo.pos.y >= target.pos.y-1.5:
                if ammo.pos.x >= target.pos.x+1.4 and ammo.pos.x <= target.pos.x+1.6:
                    flag_hit = True
                    print("\nCongrats - You Win!\n")
                    callPLT = 1
                    break

        fireT = fireT + fireDT
    ammoLand = ammo.pos
    ammo.size = vec(0.0001,0.0001,0.0001)
    boom(ammoLand)
    #checks if the target was hit
    if flag_hit == True:
        target.size=vec(0.0001,0.0001,0.0001)
        time.sleep(1.0)
        loadLevel(currentLevel+1)
    else:
        if ammoCNT == 1:
            print("\nYou lost - refresh to try again\n")
            callPLT = 0

def boom(boomPos):
    boomSize = 0.1
    boomInc = 0.5
    boom = sphere(pos=boomPos, size=vec(boomSize,boomSize,boomSize), color=vec(1,0.5,0))
    tboom = 0
    while tboom < 10:
        rate(100)
        boom.size =vec(boomSize+boomInc*tboom,boomSize+boomInc*tboom,boomSize+boomInc*tboom)
        tboom = tboom + 1
    while tboom > 0:
        rate(100)
        boom.size =vec(boomSize-boomInc*tboom,boomSize-boomInc*tboom,boomSize-boomInc*tboom)
        tboom = tboom - 1
    boom.size=vec(0.001,0.001,0.001)

def updatePos():
    #function to move all the tank barrels
    tk_pt1.pos = vec(tank.pos.x-0.8,tank.pos.y+1.5,-0.1)
    tk_pt2.pos = vec(tank.pos.x-0.8,tank.pos.y+1.6,-0.1)
    tk_pt3.pos = vec(tank.pos.x-0.8,tank.pos.y+1.8,-0.1)
    tk_pt4.pos = vec(tank.pos.x-0.4,tank.pos.y+1.9,-0.1)
    tk_pt5.pos = vec(tank.pos.x,tank.pos.y+1.8,-0.1)
    tk_pt6.pos = vec(tank.pos.x+0.5,tank.pos.y+1.9,-0.1)
    tk_pt7.pos = vec(tank.pos.x+0.7,tank.pos.y+1.8,-0.1)
    tk_pt8.pos = vec(tank.pos.x+0.7,tank.pos.y+1.6,-0.1)
    tk_pt9.pos = vec(tank.pos.x+0.7,tank.pos.y+1.5,-0.1)

def titleKeyCheck(select):
    #key check for title screen
    c = keysdown()
    if 'up' in c and select == 1:
        titleCRS.pos.y = 27
        time.sleep(0.3)
        return select-1
    elif 'down' in c and select == 0:
        titleCRS.pos.y = 21.5
        time.sleep(0.3)
        return select+1
    elif ' ' in c and select == 0:
        #start game
        select = 2
        time.sleep(0.3)
        return select
    elif ' ' in c and select == 1:
        #how to play
        select = 3
        titleTxt.pos.z = -0.3
        titleCRS.pos.z = -0.3
        helpTxt.pos.z = 0.3
        time.sleep(0.3)
        return select
    elif ' ' in c and select == 3:
        #back to title screen
        helpTxt.pos.z = -0.3
        titleTxt.pos.z = 0.3
        titleCRS.pos.z = 0.3
        select = 1
        time.sleep(0.3)
        return select
    else:
        return select


def loadLevel(levelNum):
    #load whichever level is specified
    global currentLevel
    currentLevel = levelNum

    if levelNum == 0:
        #title screen
        tank.pos = vec(-18,2,-0.1)
        target.pos = vec(18,2.5,-0.1)
        updatePos()


    if levelNum == 1:
        #update position of tank and target
        tank.pos = vec(-20,21.1,-0.1)
        target.pos = vec(24.5,21.6,-0.1)

        #call function to move tank barrels
        updatePos()

        #land declaration
        land1.pos = vec(0,10,-0.1)
        land1.size = vec(60,20,0.1)
    if levelNum == 2:
        target.size = vec(3, 3, 0.1)
        tank.pos = vec(-20,21.1,-0.1)
        target.pos = vec(15,31.6,0)

        updatePos()

        land1.pos = vec(0,10,-0.1)
        land1.size = vec(60,20,0.1)
        land3.pos = vec(25,20,-0.1)
        land3.size = vec(10,40,0.1)
        land5.pos = vec(15,15,-0.1)
        land5.size = vec(10,30,0.1)

    if levelNum == 3:
        target.size = vec(2.98357, 3, 0.13)
        tank.pos = vec(-20,16.6,-0.1)
        target.pos = vec(23,11.6,-0.13)

        updatePos()

        land1.pos = vec(-19.5,8,-0.1)
        land1.size = vec(20,15,0.1)
        land2.pos = vec(-5,0.5,-0.1)
        land2.size = vec(30,20,0.1)
        land2.rotate(angle=1.57, axis=vec(0,0,1))
        land3.pos = vec(12,2,-0.1)
        land3.size = vec(20,5,0.1)
        land4.pos = vec(17,0.5,-0.1)
        land4.size = vec(10,10,0.1)
        land4.rotate(angle=1.57, axis=vec(0,0,1))
        land5.pos = vec(23.7,4.9,-0.1)
        land5.size = vec(13.5,11,0.1)

    if levelNum == 4:
        #unload objects not needed in current level
        land3.pos = vec(0,0,-0.3)
        land3.size = vec(0.1,0.1,0.1)
        land5.pos = vec(0,0,-0.3)
        land5.size = vec(0.1,0.1,0.1)

        target.size = vec(2.98357, 3, 0.13)
        tank.pos = vec(-18,41.2,-0.1)
        target.pos = vec(8.5,6.8,-0.1)

        updatePos()

        land1.pos = vec(-19.5,20,-0.1)
        land1.size = vec(20,40,0.1)
        land2.pos = vec(-9.5,0.4,-0.1)
        land2.size = vec(5,5,0.1)
        land4.pos = vec(-5,0.4,-0.1)
        land4.size = vec(5,5,0.1)
        land6.pos = vec(-0.5,0.4,-0.1)
        land6.size = vec(5,5,0.1)
        land6.rotate(angle=1.57, axis=vec(0,0,1))
        land7.pos = vec(4.0,0.4,-0.1)
        land7.size = vec(5,5,0.1)
        land7.rotate(angle=1.57, axis=vec(0,0,1))
        land8.pos = vec(8.5,0.4,-0.1)
        land8.size = vec(5,5,0.1)
        land8.rotate(angle=1.57, axis=vec(0,0,1))
        land9.pos = vec(13.0,0.4,-0.1)
        land9.size = vec(5,5,0.1)
        land9.rotate(angle=1.57, axis=vec(0,0,1))
        land10.pos = vec(17.5,0.4,-0.1)
        land10.size = vec(5,5,0.1)
        land10.rotate(angle=1.57, axis=vec(0,0,1))
        land11.pos = vec(22.0,0.4,-0.1)
        land11.size = vec(5,5,0.1)
        land11.rotate(angle=1.57, axis=vec(0,0,1))
        land12.pos = vec(26.5,0.4,-0.1)
        land12.size = vec(5,5,0.1)
        land12.rotate(angle=1.57, axis=vec(0,0,1))

    if levelNum == 5:
        land2.pos = vec(0,0,-0.3)
        land2.size = vec(0.1,0.1,0.1)
        land4.pos = vec(0,0,-0.3)
        land4.size = vec(0.1,0.1,0.1)
        land6.pos = vec(0,0,-0.3)
        land6.size = vec(0.1,0.1,0.1)
        land7.pos = vec(0,0,-0.3)
        land7.size = vec(0.1,0.1,0.1)
        land8.pos = vec(0,0,-0.3)
        land8.size = vec(0.1,0.1,0.1)
        land9.pos = vec(0,0,-0.3)
        land9.size = vec(0.1,0.1,0.1)
        land10.pos = vec(0,0,-0.3)
        land10.size = vec(0.1,0.1,0.1)
        land11.pos = vec(0,0,-0.3)
        land11.size = vec(0.1,0.1,0.1)
        land12.pos = vec(0,0,-0.3)
        land12.size = vec(0.1,0.1,0.1)

        target.size = vec(3, 3, 0.1)
        tank.pos = vec(24,21.1,-0.1)
        target.pos = vec(-4,21.6,-0.1)

        updatePos()

        land1.pos = vec(0,10,-0.1)
        land1.size = vec(60,20,0.1)
        land3.pos = vec(0,20,-0.1)
        land3.size = vec(2,40,0.1)
        land13.pos = vec(4,20,-0.1)
        land13.size = vec(2,30,0.1)
        land14.pos = vec(8,20,-0.1)
        land14.size = vec(2,20,0.1)

    if levelNum == 6:
        target.size = vec(3, 3, 0.1)
        tank.pos = vec(-25,31.1,-0.1)
        target.pos = vec(25,31.6,-0.1)

        updatePos()

        land1.pos = vec(0,2.5,-0.1)
        land1.size = vec(60,5,0.1)
        land3.pos = vec(-25,15,-0.1)
        land3.size = vec(10,30,0.1)
        land5.pos = vec(25,15,-0.1)
        land5.size = vec(10,30,0.1)
        land13.pos = vec(0,51,-0.1)
        land13.size = vec(2,8,0.1)
        land14.pos = vec(0,24,-0.1)
        land14.size = vec(2,39,0.1)

    if levelNum == 7:
        land14.pos = vec(0,0,-0.3)
        land14.size = vec(0.1,0.1,0.1)

        target.size = vec(3, 3, 0.1)
        tank.pos = vec(24,41.1,-0.1)
        target.pos = vec(-17.2,11.6,-0.1)

        updatePos()

        land1.pos = vec(25,20,-0.1)
        land1.size = vec(10,40,0.1)
        land2.pos = vec(-16,0.4,-0.1)
        land2.size = vec(5,5,0.1)
        land4.pos = vec(15.5,0.4,-0.1)
        land4.size = vec(5,5,0.1)
        land6.pos = vec(11,0.4,-0.1)
        land6.size = vec(5,5,0.1)
        land7.pos = vec(6.5,0.4,-0.1)
        land7.size = vec(5,5,0.1)
        land8.pos = vec(2,0.4,-0.1)
        land8.size = vec(5,5,0.1)
        land9.pos = vec(-2.5,0.4,-0.1)
        land9.size = vec(5,5,0.1)
        land10.pos = vec(-7,0.4,-0.1)
        land10.size = vec(5,5,0.1)
        land11.pos = vec(-11.5,0.4,-0.1)
        land11.size = vec(5,5,0.1)
        land3.pos = vec(-20,5,-0.1)
        land3.size = vec(10,10,0.1)
        land5.pos = vec(-25,10,-0.1)
        land5.size = vec(10,20,0.1)
        land13.pos = vec(-27.5,20,-0.1)
        land13.size = vec(5,20,0.1)

    if levelNum == 8:
        land4.pos = vec(0,0,-0.3)
        land4.size = vec(0.1,0.1,0.1)
        land9.pos = vec(0,0,-0.3)
        land9.size = vec(0.1,0.1,0.1)
        land10.pos = vec(0,0,-0.3)
        land10.size = vec(0.1,0.1,0.1)
        land11.pos = vec(0,0,-0.3)
        land11.size = vec(0.1,0.1,0.1)

        target.size = vec(3, 3, 0.1)
        tank.pos = vec(-20,9.1,-0.1)
        target.pos = vec(22,21.6,-0.1)

        updatePos()

        land1.pos = vec(0,4,-0.1)
        land1.size = vec(60,8,0.1)
        land3.pos = vec(22,12,-0.1)
        land3.size = vec(16,16,0.1)
        land5.pos = vec(28,24,-0.1)
        land5.size = vec(4,8,0.1)
        land13.pos = vec(22,32,-0.1)
        land13.size = vec(16,8,0.1)
        land2.pos = vec(15.5,20,-0.1)
        land2.size = vec(3,3,0.1)
        land15.pos = vec(15.5,28,-0.1)
        land15.size = vec(3,3,0.1)
        land15.rotate(angle=-1.57, axis=vec(0,0,1))
        land6.pos = vec(18,36,-0.1)
        land6.size = vec(5,5,0.1)
        land7.pos = vec(22.5,36,-0.1)
        land7.size = vec(5,5,0.1)
        land8.pos = vec(27,36,-0.1)
        land8.size = vec(5,5,0.1)

    if levelNum == 9:
        #ending: unload all land and place tank and target at bottom
        land1.pos = vec(0,0,-0.3)
        land1.size = vec(0.1,0.1,0.1)
        land2.pos = vec(0,0,-0.3)
        land2.size = vec(0.1,0.1,0.1)
        land3.pos = vec(0,0,-0.3)
        land3.size = vec(0.1,0.1,0.1)
        land5.pos = vec(0,0,-0.3)
        land5.size = vec(0.1,0.1,0.1)
        land6.pos = vec(0,0,-0.3)
        land6.size = vec(0.1,0.1,0.1)
        land7.pos = vec(0,0,-0.3)
        land7.size = vec(0.1,0.1,0.1)
        land8.pos = vec(0,0,-0.3)
        land8.size = vec(0.1,0.1,0.1)
        land13.pos = vec(0,0,-0.3)
        land13.size = vec(0.1,0.1,0.1)
        land15.pos = vec(0,0,-0.3)
        land15.size = vec(0.1,0.1,0.1)

        target.size = vec(3, 3, 0.1)
        tank.pos = vec(-10,1.8,-0.1)
        target.pos = vec(10,2,-0.1)

        updatePos()

        print("\nYou Completed all 8 levels. Congrats!\n")

def loading(state):
    #place black screen in front so assets can load behind
    if state == 0:
        loadingScreen.size = vec(0.1,0.1,0.1)
        loadingScreen.pos = vec(0,20,-0.3)
    if state == 1:
        loadingScreen.size = vec(59,54,0.1)
        loadingScreen.pos = vec(0,27.5,0.4)

#scene---------------------------------------------------
scene1 = canvas(center = vector(0,27.5,0), title="- Connor Willans: Tanks Game -")
#walls
Bot_Wall = box(pos=vec(0, 0, 0.3), size=vec(60.5,1,0.1), shininess = 0, color=color.green)
Top_Wall = box(pos=vec(0, 55, 0.3), size=vec(60.5,1,0.1), shininess = 0, color=color.green)
Left_Wall = box(pos=vec(-30, 27.5, 0.3), size=vec(1,55.5,0.1), shininess = 0, color=color.green)
Right_Wall = box(pos=vec(30, 27.5, 0.3), size=vec(1,55.5,0.1), shininess = 0, color=color.green)
#bg
background = box(pos=vec(0,27.5,-0.2), size=vec(60,55,0.1), shininess = 0, color=color.blue)
backgroundBLK = box(pos=vec(0,65,0.2), size=vec(60,20,0.15), shininess = 0, color=color.black)

loadingScreen = box(pos=vec(0,27.5,0.4), size=vec(59,54,0.1), shininess = 0, color=color.black)

#tanks
tank_main = box(pos=vec(-20,16.6,-0.1), size=vec(3.5,1.5,0.1), color=color.green)
tk_wh1 = sphere(pos=vec(-21,15.9,-0.1), size=vec(1,1,0.1), color=color.green)
tk_wh2 = sphere(pos=vec(-20,15.9,-0.1), size=vec(1,1,0.1), color=color.green)
tk_wh3 = sphere(pos=vec(-19,15.9,-0.1), size=vec(1,1,0.1), color=color.green)
tk_top = box(pos=vec(-20,17.6,-0.1), size=vec(2,0.5,0.1), color=color.green)
#combine into one object to move around. MINUS top barrel
tank = compound([tank_main,tk_wh1, tk_wh2, tk_wh3, tk_top])

tankPos = vec(0,24.6,0)

#setting up all tank angles------------------------------------------------------------------------------
tk_pt1 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt1.pos=vec(-20.8+tankPos.x,18+tankPos.y,-0.1)
tk_pt1.rotate(angle=1.40, axis=vec(0,0,1))
tk_pt2 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt2.pos=vec(-20.8+tankPos.x,18.1+tankPos.y,-0.1)
tk_pt2.rotate(angle=1.20, axis=vec(0,0,1))
tk_pt3 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt3.pos=vec(-20.8+tankPos.x,18.3+tankPos.y,-0.1)
tk_pt3.rotate(angle=1, axis=vec(0,0,1))
tk_pt4 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt4.pos=vec(-20.4+tankPos.x,18.5+tankPos.y,-0.1)
tk_pt4.rotate(angle=0.60, axis=vec(0,0,1))
tk_pt5 = box(pos=vec(-20+tankPos.x,18.3+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
#already in position
tk_pt6 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt6.pos=vec(-19.5+tankPos.x,18.5+tankPos.y,-0.1)
tk_pt6.rotate(angle=0.60, axis=vec(0,0,-1))
tk_pt7 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt7.pos=vec(-19.3+tankPos.x,18.3+tankPos.y,-0.1)
tk_pt7.rotate(angle=1, axis=vec(0,0,-1))
tk_pt8 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt8.pos=vec(-19.3+tankPos.x,18.1+tankPos.y,-0.1)
tk_pt8.rotate(angle=1.20, axis=vec(0,0,-1))
tk_pt9 = box(pos=vec(-20+tankPos.x,18+tankPos.y,-0.1), size=vec(0.0001,0.0001,0.0001), color=color.green)
tk_pt9.pos=vec(-19.3+tankPos.x,18+tankPos.y,-0.1)
tk_pt9.rotate(angle=1.40, axis=vec(0,0,-1))
#--------------------------------------------------------------------------------------------------------

#target
target1 = sphere(pos=vec(24.5,11.8,-0.13), size=vec(3,3,0.1), color=color.white)
target2 = sphere(pos=vec(24.5,11.8,-0.12), size=vec(2.5,2.5,0.1), color=color.red)
target3 = sphere(pos=vec(24.5,11.8,-0.11), size=vec(2,2,0.1), color=color.white)
target4 = sphere(pos=vec(24.5,11.8,-0.1), size=vec(1.2,1.2,0.1), color=color.red)
target = compound([target1,target2,target3,target4])

#title screen
tanksTxt = text(text='TANKS', pos=vec(-17.5, 35, 0.3), height=9, depth=0, shininess=0, color=vec(0.95,0.95,0.95))
startTxt = text(text='Start', pos=vec(-10, 25, 0.3), height=4, depth=0, shininess=0, color=vec(0.95,0.95,0.95))
howTxt = text(text='How to Play', pos=vec(-10, 20, 0.3), height=3.5, depth=0, shininess=0, color=vec(0.95,0.95,0.95))
nameTxt = text(text='By: Connor Willans', pos=vec(-13, 2, 0.3), height=2.5, depth=0, shininess=0, color=vec(0.95,0.95,0.95))
titleTxt = compound([tanksTxt, startTxt, howTxt, nameTxt])

titleCRS = box(pos=vec(-13.5,27,0.3), size=vec(2.5,0.8,0.1), shininess = 0, color=vec(1,1,0.5))

demoTxt = text(text='How to Play\n[<][>] - Adjust Aim\n[^][v] - Change Power\n[1][2][3] - Select Spin\n[___] - Fire', pos=vec(-45, 40, -0.3), height=3.5, depth=0, shininess=0, color=vec(0.95,0.95,0.95))
backTxt = text(text='Back [___]', pos=vec(-7.5, 2, -0.3), height=2.5, depth=0, shininess=0, color=vec(0.95,0.95,0.95))
helpTxt = compound([demoTxt,backTxt])

#title screen
loadLevel(0)
select = 0
loading(0)
while True == True:
    rate(100)
    select = titleKeyCheck(select)
    if select == 2:
        titleTxt.height = 0.1
        titleTxt.pos = vec(0,20,-0.3)
        titleCRS.size = vec(0.1,0.1,0.1)
        titleCRS.pos = vec(0,20,-0.3)
        break
loading(1)

#power levels
power1 = box(pos=vec(-16.5, -4, 0), size=vec(10,5,0.1), shininess = 0, color=color.green)
power2 = box(pos=vec(-5.5, -4, 0), size=vec(10,5,0.1), shininess = 0, color=color.yellow)
power3 = box(pos=vec(5.5, -4, 0), size=vec(10,5,0.1), shininess = 0, color=color.orange)
power4 = box(pos=vec(16.5, -4, 0), size=vec(10,5,0), shininess = 0, color=color.red)

#spin menu
backspin = text(text='1 - Backspin', pos=vec(-28, 58, 0.3), height=2.2, depth=0, shininess=0, color=vec(1,1,1))
nospin = text(text='2 - No Spin', pos=vec(-7, 58, 0.3), height=2.2, depth=0, shininess=0, color=vec(1,1,1))
topspin = text(text='3 - Topspin', pos=vec(13, 58, 0.3), height=2.2, depth=0, shininess=0, color=vec(1,1,1))

ammoPos=vec(0,0,0)

#land declaration
land1 = box(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land2 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land3 = box(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land4 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land5 = box(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land6 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land7 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land8 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land9 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land10 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land11 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land12 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land13 = box(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land14 = box(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)
land15 = pyramid(pos=vec(0,0,-0.3), size=vec(0.1,0.1,0.1), shininess = 0, color=color.red)

#wind
global ammoWIND
windRand = 1
wind1 = text(text='Wind: 3m/s  >>>', pos=vec(-28, 51, 0.3), height=2.5, depth=0, shininess=0, color=color.white)
ammoWIND = vec(1,0,0)

#ammo / 3 shots
ammoCNT = 3
ammoN1 = sphere(pos=vec(27,52,0.1), size=vec(1.5,1.5,0.1), color=color.white)
ammoN2 = sphere(pos=vec(24,52,0.1), size=vec(1.5,1.5,0.1), color=color.white)
ammoN3 = sphere(pos=vec(21,52,0.1), size=vec(1.5,1.5,0.1), color=color.white)

#data arrays
global ammoVEC
ammoVEC = np.zeros(1000)
global timeVEC
timeVEC = np.zeros(1000)

global p
p = 0.0138              #air density
global r
r = 1                   #radius
global A
A = pi*r**2             #area
global w
w = vec(1,1,1)          #spin
global m
m = 200                 #mass
global grav
grav = vec(0,-3.711,0)  #gravity


ammoVEC = np.append(ammoVEC, 0)
timeVEC = np.append(timeVEC, 0)

#setting default values
curPos = 5
ammoPWR = 3
ammoSPN = 2
callPLT = 0
ammoY = 0
powerMeter(3)
spinMenu()
aimCannon(curPos)     #important line to call function once to set up all cannon positions
t = 0
dt = 0.001

currentLevel = 1

loadLevel(1)
loading(0)
while True == True:
    callPLT = 0
    while t < 30:
        rate(100)
        curPos = keyCheck(curPos)

        if currentLevel == 9:
            time.sleep(3.0)
            break
        if ammoCNT == 2:
            ammoN3.pos.z = -0.3
        if ammoCNT == 1:
            ammoN2.pos.z = -0.3
        if ammoCNT == 0:
            ammoN1.pos.z = -0.3
            break
        if callPLT == 1:
            break
        t = t + dt
    #if player does not hit the target in 3 shots - end loop
    if callPLT == 0:
        break
    ammoCNT = 3
    ammoN1.pos.z = 0.1
    ammoN2.pos.z = 0.1
    ammoN3.pos.z = 0.1

fig = plt.figure()
plt.title("Y-Velocity vs Time")
plt.plot(timeVEC,ammoVEC, 'b-', label='shot 1')
plt.xlabel('t (s)')
plt.ylabel('y-vel (m/s^2)')
plt.legend()
plt.show()
