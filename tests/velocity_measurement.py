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
velocity = []
velocity_unfiltered = []
lines_moved = []
time = []

# Initialise filter data
velocity_old = 0
a = 0.1

def save():
    global velocity
    global velocity_unfiltered
    global lines_moved
    global time

    measurement_nr = input("Which measurementnr?")

    csvfilename = './storage/test-data/velocity-tests/' + measurement_nr + '.csv'
    figfilename = './storage/test-data/velocity-tests/' + measurement_nr + '.png'

    #Write to csv
    with open(csvfilename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['velocity', 'velocity_unfiltered', 'lines_moved', 'time'])
        writer.writerows(zip(velocity, velocity_unfiltered, lines_moved, time))
    
    #Plot to figure and save
    fig, ax = plt.subplots()
    ax.plot(time, velocity, 'r-', label='Velocity')
    # ax.plot(time, lines_moved, 'b--', label='Lines moved')
    ax.set_title("Velocity Test")
    ax.set_ylabel("Velocity [m/s]")
    ax.set_xlabel("Time [s]")
    ax.legend()
    fig.savefig(figfilename)

start_time = t.time()
sensor_time = 0

try:
    while True:
        ser_bytes = ser.read(8)
        # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        n_lines, v = struct.unpack('ff', ser_bytes)

        velocity_filtered = a * v + (1 - a) * velocity_old
        velocity_old = velocity_filtered

        velocity_unfiltered.append(v)
        time.append(sensor_time)
        velocity.append(velocity_filtered)
        lines_moved.append(n_lines)
        sensor_time += 1/10
        
        print('information: ', v, n_lines)

except KeyboardInterrupt:
    print('I am quitting')
    save()
    pass