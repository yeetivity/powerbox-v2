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
force1 = []
force1_unfiltered = []
force2 = []
force2_unfiltered = []
time = []

# Initialise filter data
velocity_old = 0
force1_old = 0
force2_old = 0
a_velocity = 0.1
a_force = 0.8

# Calibration data
null_point_correction_1 = 4.67418
a1 = -3.20061411300997e-05
b1 = -5.3303520315288 + null_point_correction_1

null_point_correction_2 = 0
a2 = -3.4567490506012004e-05
b2 = -1.52071926256712 + null_point_correction_2

def save():
    measurement_nr = input("Which measurementname?")

    csvfilename = './storage/test-data/velocity-tests/' + measurement_nr + '.csv'
    figfilename = './storage/test-data/velocity-tests/' + measurement_nr + '.png'

    # Write to csv
    with open(csvfilename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['velocity', 'velocity_unfiltered', 'force1', 'force1_unfiltered', 'force2', 'force2_unfiltered', 'time'])
        writer.writerows(zip(velocity, velocity_unfiltered, force1, force1_unfiltered, force2, force2_unfiltered, time))
    
    # Create figure
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

    # Plot velocity
    ax1.plot(time, velocity, 'r-', label='Velocity')
    ax1.plot(time, velocity_unfiltered, 'b--', label='Unfiltered Velocity')
    ax1.set_title("Velocity Test")
    ax1.set_ylabel("Velocity [m/s]")
    ax1.set_xlabel("Time [s]")
    ax1.legend()

    # Plot force 1
    ax2.plot(time, force1, 'r-', label='Force')
    ax2.plot(time, force1_unfiltered, 'b--', label='Unfiltered Force')
    ax2.set_title("Force 1")
    ax2.set_ylabel("Force [kg]")
    ax2.set_xlabel("Time [s]")
    ax2.legend()

    # Plot force 2
    ax3.plot(time, force2, 'r-', label='Force')
    ax3.plot(time, force2_unfiltered, 'b--', label='Unfiltered Force')
    ax3.set_title("Force 2")
    ax3.set_ylabel("Force [kg]")
    ax3.set_xlabel("Time [s]")
    ax3.legend()

    # Save the figure
    fig.savefig(figfilename)

start_time = t.time()
sensor_time = 0

try:
    while True:
        ser_bytes = ser.read(12)
        # decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        v, f1, f2 = struct.unpack('fff', ser_bytes)

        f1 = a1*f1 + b1
        f2 = a2*f2 + b2

        velocity_unfiltered.append(v)
        velocity_filtered = a_velocity * v + (1 - a_velocity) * velocity_old
        velocity_old = velocity_filtered
        velocity.append(velocity_filtered)

        force1_unfiltered.append(f1)
        force1_filtered = a_force * f1 + (1 - a_force) * force1_old
        force1_old = force1_filtered
        force1.append(force1_filtered)

        force2_unfiltered.append(f2)
        force2_filtered = a_force * f2 + (1 - a_force) * force2_old
        force2_old = force2_filtered
        force2.append(force2_filtered)

        time.append(sensor_time)
        sensor_time += 1/60
        
        print('information: ', v, f1, f2)

except KeyboardInterrupt:
    print('I am quitting')
    save()
    pass

print('number of samples:', len(force1))