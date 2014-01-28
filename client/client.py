# client sensor data simulation
#
# uses interactive user input to simulate RPi XloBorg Accelerometer sensor data,
# process, translate into stepper motor targets,
# and send to arduino
#
# inspired by http://pi.gate.ac.uk/pages/pibrush.html
# 
# more sources:
# http://www.rasptut.co.uk/files/raspberry-pi-xloborg1.php
# http://www.loveelectronics.co.uk/Tutorials/8/hmc5883l-tutorial-and-arduino-library

import socket
#import XLoBorg
from SimXLo import SimXLo
from multiprocessing import Process, Pipe
from multiprocessing.managers import BaseManager
import time
import os
import math
import random


# =========
# init
# =========

# set to True if we want to just test the motor without worrying about XLo simulation
stepper_test_mode = True

# how long to wait between messages, in seconds
sleepytime = .5 # 0.005 # more pro time: 200 msgs/minute

# network stufff
server = 'localhost' #os.getenv('SERVER', 'modelb')
port = 5005

# setup for the accelerometer
#XLoBorg.printFunction = XLoBorg.NoPrint
#XLoBorg.Init()

### setup accelerometer simulation ###
#XLo = SimXLo() # simple way; access only possible from one process

# use Manager from multiprocessing to handle multiple processes
class MyManager(BaseManager):
    pass

MyManager.register('XLo', SimXLo)
# start subprocess to start the manager
manager = MyManager()
manager.start()
# create proxy SimXLo
XLo = manager.XLo()

# use Pipe to open connection between user input and XLo
#sender, receiver = Pipe()

### ###

# make the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# magnetic declination correction for Berlin: 
# http://magnetic-declination.com/ || 3 deg 8' EAST
# http://www.wolframalpha.com/input/?i=%283%C2%B0+8%27%29+in+radians || 54.69 mrad
BERLIN = 54.69
declinationAngle = BERLIN/1000

# =========
# functions
# =========

def get_sim_rotate_target(conn):
    target = 1
    while target: # just hitting 'Enter' causes the function to return
        target = raw_input("Enter the desired angle to turn the SimXLo (0-360): ")
        conn.send(target)
        time.sleep(.5)


def test_rotate(XLoProxy):
    time.sleep(1)
    print '-' * 20
    print 'Setting XLo target to 180'
    XLoProxy.set_target(180)
    XLoProxy.sim_rotate()
    print '-' * 20
    time.sleep(1)
    print '\n*** Process test_rotate completed ***\n'

def test_read(XLoProxy):
    vals = 80 * [None]
    for i in range(80):
        vals[i] = XLoProxy.ReadAccelerometer()
        print vals[i]
        time.sleep(.05)
    print '\n*** Process test_read completed ***\n'

def cartesian_to_angle(mx, my):
    # get the heading in radians
    heading = math.atan2 (my,mx)
    # Correct negative values
    if (heading < 0):
            heading  = heading + (2 * math.pi)
    # convert to degrees
    heading = heading * 180/math.pi;
    return heading

# ============
# main program
# ============

target = 0

readXLo = Process(target=test_read, args=(XLo, ))
rotateXLo = Process(target=test_rotate, args=(XLo, ))

readXLo.start()
rotateXLo.start()

readXLo.join()
rotateXLo.join()

#userInput = Process(target=get_sim_rotate_target, args=(sender, ))
#userInput.start()

while True:

    if stepper_test_mode: # we just send stuff to the server to pass to the arduino
        target = raw_input("Enter the desired number of steps (1-200): ")
        sock.sendto(target, (server, port))
        time.sleep(sleepytime)
    else:
        #target = raw_input("Enter the desired angle to turn the SimXLo (0-360): ")
        if receiver.poll(): # check for data from user
            target = receiver.recv()
            XLo.set_target(target)
            XLo.sim_rotate()
        coords = XLo.ReadAccelerometer()
        print coords
        time.sleep(1)

        # do other processing here


        # set up two processes 
        # first one simulates repeatedly reading from the Xlo,
        # calculating a moving average,
        # transforming into a stepper value,
        # and sending it to the server
        # second process takes user input to 'control' the simulated XLo sensor

    #message = '%+01.4f,%+01.4f,%+01.4f' \
    #        % XLoBorg.ReadAccelerometer()
