# 
# python interface to arduino serial port
#
# listens for UDP input 
#
# once we get the ethernet shield, 
# the server will be handled on the arduino -
# this is just a simulation for testing
#
# inspired by http://pi.gate.ac.uk/pages/pibrush.html

import serial  
import time  
import socket
import select
import os

# ==============
# initialization
# ==============

# port to listen on
port = 5005

# setup networking
sock = socket.socket(socket.AF_INET,
        socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", port))
sock.setblocking(0)
 
# connect to arduino  
"""
locations=['/dev/tty.usbmodem411', '/dev/tty.usbmodem641', '/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3', 
'/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3']    
    
for device in locations:    
    try:    
        print "Trying...",device  
        arduino = serial.Serial(device, 9600)   
        print 'Located device!'
        time.sleep(1)
        print arduino.readline()
        print arduino.readline()
        break  
    except:    
        print "Failed to connect on",device     
"""
  
# ============
# main program
# ============

running = 1

while running:

    result = select.select([sock], [], [], 0)
    if len(result[0]) > 0:
        # read in data
        data = str(result[0][0].recvfrom(1024)[0]) + '\n'
        print "Received:", data
        """
        try:    
            print 'writing to Arduino'
            arduino.write(data)    
            print 'wrote to Arduino'
            #time.sleep(.5)  
            lines_to_read = 0
            while lines_to_read < 6:
                print arduino.readline()
                lines_to_read += 1
                time.sleep(1) 
        except:    
            print "Failed to send!"   

        """
        
