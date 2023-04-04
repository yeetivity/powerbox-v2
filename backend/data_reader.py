"""
Module responsible from reading data from the usb serial port and unpack it
Sends out regular data updates to the UI
Runs on its own thread

Author: Jitse van Esch
Date: 24-03-23
"""
import serial, struct
import time as t
import numpy as np
from collections import deque
from settings import ApplicationSettings
import random, threading
class DataReader(threading.Thread):
    def __init__(self, stop_flag, data_screen, n_users):
        threading.Thread.__init__(self)
        
        # Set a stop flag
        self.stop_flag = stop_flag
        
        # Initialize storage variables
        self.data = {'forces1' : deque(),
                     'forces2' : deque(),
                     'velocities' : deque(),
                     'times' : deque()}
        self.combinedforces =  deque()
        self.meanforce = np.zeros(2)
        self.peakforce = np.zeros(2)
        
        # Initialise UI pointer
        self.ui = data_screen
        
        # Initialise number of users
        self.n_users = n_users

        # Filter variables
        self.a = ApplicationSettings.ALPHA_VELOCITY_FILTER

    def run(self):
        """
        Method that starts gathering data
        =INPUT=
        datascreen      reference to UI to publish data on
        n_users         the amount of users
        """
        # Init
        packet_time = 0
        velocity_old = 0

        # Calibration data
        null_point_correction_1 = 4.67418
        a1 = -3.20061411300997e-05
        b1 = -5.3303520315288 + null_point_correction_1

        null_point_correction_2 = 0
        a2 = -3.4567490506012004e-05
        b2 = -1.52071926256712 + null_point_correction_2

        # TODO: UNCOMMENT WHEN CONNECTED TO PI PICO
        # Setup serial readout
        port = serial.Serial('/dev/ttyACM0')
        port.flushInput()

        received_bytes = bytearray(12)

        while not self.stop_flag.is_set():
            # TODO: UNCOMMENT WHEN CONNECTED TO PI PICO
            # Read the received bytes into the bytearray
            port.readinto(received_bytes)

            # Extract the force and velocity values
            velocity, force1, force2 = struct.unpack_from('fff', received_bytes)
            # force1, force2, velocity = self.generate_random(self.n_users)
            # force1 = 1
            # force2 = 1
            # n_lines, velocity = struct.unpack('ff', received_bytes)
            # print(velocity)

            # Filter velocity
            velocity_filtered = self.a * velocity + (1 - self.a) * velocity_old
            velocity_old = velocity_filtered

            # Transform force
            f1 = a1*force1 + b1
            f2 = a2*force2 + b2

            # Update the data dictionary
            self.data['forces1'].append(f1)
            self.data['forces2'].append(f2)
            self.data['velocities'].append(velocity)
            self.data['times'].append(packet_time)

            print(f1, f2, velocity)
            
            # Update time
            packet_time += (1 / ApplicationSettings.FREQUENCY)

            if self.n_users == 1:
                self.combinedforces.append(max(f1, f2))

            # Update running average and peakforce
            if self.n_users == 2:
                self.meanforce[0] = np.mean(self.data['forces1'])
                self.meanforce[1] = np.mean(self.data['forces2'])
                self.peakforce[0] = np.max(self.data['forces1'])
                self.peakforce[1] = np.max(self.data['forces2'])
            elif self.n_users == 1:
                self.meanforce[0] = np.mean(self.combinedforces)
                self.peakforce[0] = np.max(self.combinedforces)

            # Update time on 8 Hz
            if round(packet_time, 3) % (1 / ApplicationSettings.UPDATE_TIME_FREQUENCY) == 0:
                self.update_ui_time(packet_time)
            
            # Update vars on 4 Hz
            if round(packet_time, 3) % (1 / ApplicationSettings.UPDATE_VARS_FREQUENCY) == 0:
                if self.n_users == 1:
                    self.update_ui_vars_1p(self.combinedforces, velocity, self.peakforce, self.meanforce)
                else:
                    self.update_ui_vars_2p(f1, f2, velocity, self.peakforce)
                    
            t.sleep(ApplicationSettings.SLEEP_TIME)

    def update_ui_time(self, packet_time):
        self.ui.display_time(packet_time)

    def update_ui_vars_1p(self, force, velocity, peakforce, meanforce):
        """ Method to output data for 1 user to the screen """
        power = velocity * force[-1]

        self.ui.display_data_1p((force, power, meanforce[0], peakforce[0]))

    def update_ui_vars_2p(self, force1, force2, velocity, peakforces):
        """ Method to output data for 2 users to the screen """
        self.ui.display_data_2p((force1, force2, velocity, peakforces[0], peakforces[1]))

    def stop(self):
        self.stop_flag.set()
        
    def get_data(self, n_users):
        """ Method to receive data saved in the class """
        if n_users == 1:
            powers = np.multiply(self.combinedforces, self.data['velocities'])
            return ((self.combinedforces, self.data['velocities'], powers, self.data['times']),)
        else:
            powers1 = np.multiply(self.data['forces1'], self.data['velocities'])
            powers2 = np.multiply(self.data['forces2'], self.data['velocities'])
            return ((self.data['forces1'], self.data['velocities'], powers1, self.data['times']),
                    (self.data['forces2'], self.data['velocities'], powers2, self.data['times']))

    def generate_random(self, n_users):
        if n_users == 1:
            if random.random() < 0.5:
                force1 = random.random() * 10
                force2 = 0
                velocity = random.random() * 10
            else:
                force2 = random.random() * 10
                force1 = 0
                velocity = -1 * random.random() * 10
        else:
            force1 = random.random() * 10
            force2 = random.random() * 10
            velocity = random.random() * 10

        return force1, force2, velocity