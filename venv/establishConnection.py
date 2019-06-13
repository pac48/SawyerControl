# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import vrep


def connect():
    vrep.simxFinish(-1) # just in case, close all opened connections
    clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

    if clientID!=-1:
        print('Connected to remote API server')
        return clientID
    else:
        print ('Failed connecting to remote API server')
        return 0

