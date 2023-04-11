#script that is used for calibrating the force sensors

import serial
import struct
import csv
import matplotlib.pyplot as plt
import matplotlib
import time as t

matplotlib.use('Agg') #use a non-interactive backend

# Set up serial readout
ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()

# Initialise lists
force = []

start_time = t.time()


while True:
    ser_bytes = ser.read(12)
    # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    v, f1, f2 = struct.unpack('fff', ser_bytes)

    force.append(f1)

    if t.time() - start_time > 10:
        break
    
print('n packets: ', len(force))

