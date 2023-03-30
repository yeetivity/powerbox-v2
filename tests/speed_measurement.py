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
velocity = []
lines_moved = []
time = []

def save():
    global velocity
    global lines_moved
    global time

    measurement_nr = input("Which measurementnr?")

    csvfilename = './storage/test-data/velocity-tests/' + measurement_nr + '.csv'
    figfilename = './storage/test-data/velocity-tests/' + measurement_nr + '.png'

    #Write to csv
    with open(csvfilename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['velocity', 'lines_moved', 'time'])
        writer.writerows(zip(velocity, lines_moved, time))
    
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
        time.append(sensor_time)
        velocity.append(v)
        lines_moved.append(n_lines)
        sensor_time += 1/10
        
        print('information: ', v, n_lines)

except KeyboardInterrupt:
    print('I am quitting')
    save()
    pass