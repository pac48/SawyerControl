import vrep
import numpy as np
import time
import establishConnection
import terminateConnection


def main():
    clientID = establishConnection.connect()
    handles = []
    for i in range(1,7):
        returnCode, handle = vrep.simxGetObjectHandle(clientID, "Sawyer_joint"+str(i), vrep.simx_opmode_blocking)
        handles.append(handle)
    for i in range(0, 6):
        returnCode = vrep.simxSetJointForce(clientID, handles[i],0, vrep.simx_opmode_oneshot)
    returnCode,T = vrep.simxGetJointForce(clientID, handles[1], vrep.simx_opmode_streaming)
    time.sleep(.02)
    returnCode,T = vrep.simxGetJointForce(clientID, handles[1], vrep.simx_opmode_buffer)
    print(T)
    b,T =vrep.simxGetJointPosition(clientID,handles[1], vrep.simx_opmode_streaming)
    time.sleep(.02)
    b, T = vrep.simxGetJointPosition(clientID, handles[1], vrep.simx_opmode_buffer)
    returnCode = vrep.simxSetJointTargetPosition(clientID, handles[1], T-1, vrep.simx_opmode_oneshot)
    print(T)
    terminateConnection.terminate(clientID)


if __name__ == '__main__':
    main()
