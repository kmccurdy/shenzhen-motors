# client sensor data simulation
#
# uses interactive user input to read RPi XloBorg Accelerometer sensor data,
# process, translate into stepper motor targets,
# and send to arduino
#
# inspired by http://pi.gate.ac.uk/pages/pibrush.html
# 
# more sources:
# http://www.rasptut.co.uk/files/raspberry-pi-xloborg1.php
# http://www.loveelectronics.co.uk/Tutorials/8/hmc5883l-tutorial-and-arduino-library

import socket
import XLoBorg
import time
import os
import math
import random


# =========
# init
# =========

# object to handle accelerometer readings
class XLoReader:
    def __init__(self):       
        self.full_step = 200 # number of steps per full rotation for our stepper motor
        self.aX = [] # placeholders for moving average arrays
        self.aY = []
        self.MAlength = 20 # length for moving average arrays
        self.offset = 0 # for baseline angle correction
        self.steps = 0 # hold target stepper value
    # using cylindrical coordinates with x and y, ignoring z
    # http://electron9.phys.utk.edu/vectors/3dcoordinates.htm
    # use arrays to get moving average
    def get_angle(self):
        x = math.fsum(self.aX)/self.MAlength
        y = math.fsum(self.aY)/self.MAlength
        # r = math.sqrt(x*x + y*y) # in case we need r for checking or whatever, here it is
        f = math.atan2(y, x)
        return f
    # convert angle in radians to step count
    # optional offset parameter to correct for baseline angle
    def get_steps(self, f):
        self.steps = (f / (2 * math.pi)) * self.full_step + self.offset
        self.steps = math.floor(self.steps)
    # add new accelerometer values to array, or initialize array if necessary
    def read(self, x, y):
        if self.aX:
            self.aX.insert(0, x)
            self.aX.pop()
        else:
            self.aX = [x] * self.MAlength 
        if self.aY:
            self.aY.insert(0, y)
            self.aY.pop()
        else:
            self.aY = [y] * self.MAlength 
    # main function - convert XloBorg accelerometer measurements to step count for rotation
    def rotate(self, x, y):
        self.read(x, y)
        f = self.get_angle()
        self.get_steps(f)
        return self.steps

reader = XLoReader()

# set to True if we want to just test the motor without worrying about XLo simulation
stepper_test_mode = False

# how long to wait between messages, in seconds
sleepytime = 0.005 

# network stufff
server =  '192.168.178.65' # my macbook #'192.168.178.177' # the arduino #'localhost' #os.getenv('SERVER', 'modelb')
port = 5005 #8888

# setup for the accelerometer
XLoBorg.printFunction = XLoBorg.NoPrint
XLoBorg.Init()

# make the socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# magnetic declination correction for Berlin: 
# http://magnetic-declination.com/ || 3 deg 8' EAST
# http://www.wolframalpha.com/input/?i=%283%C2%B0+8%27%29+in+radians || 54.69 mrad
BERLIN = 54.69
declinationAngle = BERLIN/1000


# ============
# main program
# ============


while True:

    if stepper_test_mode: # we just send stuff to the server to pass to the arduino
        target = raw_input("Enter the desired number of steps (1-200): ")
        sock.sendto(target, (server, port))
        time.sleep(sleepytime)
    else:
        X, Y, Z = XLoBorg.ReadAccelerometer()
        steps = reader.rotate(X, Y)
        message = str(steps)
        sock.sendto(message, (server, port))
        time.sleep(sleepytime)
