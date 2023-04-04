#script that is used for calibrating the force sensors

import serial
import struct
import csv
import matplotlib.pyplot as plt
import matplotlib
import time as t

matplotlib.use('Agg') #use a non-interactive backend

#Set up serial readout
ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()

#initialize lists
force = []
rawforce = []
time = []

# Calibration data (works for sensor 1 on gain 64)
null_point_correction = 4.67418
a = -3.20061411300997e-05
b = -5.3303520315288 + null_point_correction

# a = -28836.5873622319067
# b = -207265.90178130945

def save():
    global force
    global time

    measurement_nr = input("Which measurementnr?")

    csvfilename = './storage/testdata/isometric_tests/' + measurement_nr + '.csv'
    figfilename = './storage/testdata/isometric_tests/' + measurement_nr + '.png'

    #Write to csv
    with open(csvfilename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['force', 'time', 'rawforce'])
        writer.writerows(zip(force, time, rawforce))
    
    #Plot to figure and save
    fig, ax = plt.subplots()
    ax.plot(time, force, 'r-')
    ax.set_title("Isometric Test")
    ax.set_ylabel("Force [kg]")
    ax.set_xlabel("Time [s]")
    fig.savefig(figfilename)

start_time = t.time()
sensor_time = 0

try:
    while True:
        ser_bytes = ser.read(4)
        # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        decoded = struct.unpack('f', ser_bytes)
        measured_force = float(decoded[0])
        f = a * measured_force + b
        force.append(f)
        rawforce.append(measured_force)
        time.append(sensor_time)
        sensor_time += 1/80
        print(decoded[0], f)

except KeyboardInterrupt:
    print('I am quitting')
    save()
    pass