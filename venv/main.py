import vrep
import numpy as np
import time
import establishConnection
import terminateConnection

def main():
    pos = np.zeros(7)
    vel = np.zeros(7)
    tor = np.zeros(7)
    clientID = establishConnection.connect()
    handles = {}
    for i in range(1, 8):
        returnCode, handle = vrep.simxGetObjectHandle(clientID, "Sawyer_joint" + str(i), vrep.simx_opmode_blocking)
        handles[i] = handle
        returnCode, T = vrep.simxGetJointForce(clientID, handle, vrep.simx_opmode_streaming)
        returnCode, T = vrep.simxGetJointPosition(clientID, handle, vrep.simx_opmode_streaming)
        # returnCode, T = vrep.simxGetJointVelocity(clientID, handle, vrep.simx_opmode_streaming)
        returnCode, T = vrep.simxGetObjectFloatParameter(clientID,handle, 2012, vrep.simx_opmode_streaming)
    time.sleep(.2)
    getForce = lambda j:  getForceHelper(clientID, handles[j], vrep.simx_opmode_streaming)
    getVel = lambda j: getVelHelper(clientID, handles[j], vrep.simx_opmode_streaming)
    getPos = lambda j: getPosHelper(clientID, handles[j], vrep.simx_opmode_streaming)
    setForce = lambda j, f: vrep.simxSetJointForce(clientID, handles[j], f, vrep.simx_opmode_oneshot)
    setVel = lambda j, v: vrep.simxSetJointTargetVelocity(clientID, handles[j], v, vrep.simx_opmode_oneshot)
    setPos = lambda j, p: vrep.simxSetJointTargetPosition(clientID, handles[j], p, vrep.simx_opmode_oneshot)
    setTorque = lambda j, T: torqueHelper(j,T,getPos,setPos,setForce)

    for t in range(0,1000):
        for j in range(1, 8):
            v = getVel(j)
            P = getPos(j)
            #if (j==6):
            #        P=-P
            #        print(P)
            setTorque(j,-(P)*300-v*5)

        #setTorque(2, 50)
        time.sleep(.01)
    #returnCode,T = vrep.simxGetJointForce(clientID, handles[1], vrep.simx_opmode_streaming)

    #returnCode,T = vrep.simxGetJointForce(clientID, handles[1], vrep.simx_opmode_buffer)
    #print(T)
    #b,T =vrep.simxGetJointPosition(clientID,handles[1], vrep.simx_opmode_streaming)
    #time.sleep(.2)
    #b, T = vrep.simxGetJointPosition(clientID, handles[1], vrep.simx_opmode_buffer)
    #returnCode = vrep.simxSetJointTargetPosition(clientID, handles[1], T-1, vrep.simx_opmode_oneshot)
    #print(T)
    for j in range(1, 8):
        setTorque(j, 0)
    terminateConnection.terminate(clientID)


def torqueHelper(j,T,getPos,setPos,setForce):
    P = getPos(j)
    if T>20:
        T=20
    returnCode =setPos(j,P+T/1000)
    returnCode =setForce(j,np.abs(T))
    #returnCode = setForce(j, 1000)


def getForceHelper(clientID, handle, option):
    returnCode,F = vrep.simxGetJointForce(clientID, handle, option)
    return F


def getVelHelper(clientID, handle, option):
    returnCode,V = vrep.simxGetObjectFloatParameter(clientID, handle, 2012, option)
    return V


def getPosHelper(clientID, handle, option):
    returnCode,P = vrep.simxGetJointPosition(clientID, handle, option)
    return P

if __name__ == '__main__':
    main()
