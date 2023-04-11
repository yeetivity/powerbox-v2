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
        
        # Initialise calibration factors
        self.calibration_factor1 = 0
        self.calibration_factor2 = 0

        # Filter variables
        self.alpha = ApplicationSettings.ALPHA_VELOCITY_FILTER

        # Calibration variables
        self.A1 = -3.20061411300997e-05
        self.A2 = -3.4567490506012004e-05
        self.B1 = -5.3303520315288 + 4.67418
        self.B2 = -1.52071926256712 

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

        # Setup serial readout
        port = serial.Serial('/dev/ttyACM0')
        port.flushInput()

        received_bytes = bytearray(12)

        while not self.stop_flag.is_set():
            # Read the received bytes into the bytearray
            port.readinto(received_bytes)

            # Extract the force and velocity values
            velocity, self.force1, self.force2 = struct.unpack_from('fff', received_bytes)
            
            # Calibrate
            self.force1 = self.A1 * self.force1 + self.B1 - self.calibration_factor1
            self.force2 = self.A2 * self.force2 + self.B2 - self.calibration_factor2

            # Filter velocity
            velocity_filtered = self.alpha * velocity + (1 - self.alpha) * velocity_old
            velocity_old = velocity_filtered

            # Update the data dictionary
            self.data['forces1'].append(self.force1)
            self.data['forces2'].append(self.force2)
            self.data['velocities'].append(velocity)
            self.data['times'].append(packet_time)
            
            # Update time
            packet_time += (1 / ApplicationSettings.FREQUENCY)

            if self.n_users == 1:
                self.combinedforces.append(max(self.force1, self.force2))

            # Update average and peakforce
            if self.n_users == 2:
                self.meanforce[0] = np.mean(self.data['forces1'])
                self.meanforce[1] = np.mean(self.data['forces2'])
                self.peakforce[0] = np.max(self.data['forces1'])
                self.peakforce[1] = np.max(self.data['forces2'])
            elif self.n_users == 1:
                self.meanforce[0] = np.mean(self.combinedforces)
                self.peakforce[0] = np.mean(self.combinedforces)

            # Update time on 1 Hz
            if round(packet_time, 3) % (1 / ApplicationSettings.UPDATE_TIME_FREQUENCY) == 0:
                self.update_ui_time(packet_time)
            
            # Update vars on 2 Hz
            if round(packet_time, 3) % (1 / ApplicationSettings.UPDATE_VARS_FREQUENCY) == 0:
                if self.n_users == 1:
                    self.update_ui_vars_1p(self.combinedforces, velocity, self.peakforce, self.meanforce)
                else:
                    self.update_ui_vars_2p(self.force1, self.force2, velocity, self.peakforce)
                    
            # t.sleep(ApplicationSettings.SLEEP_TIME)

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
            powers = [force * 9.81 * abs(velocity) for force, velocity in zip(self.combinedforces, self.velocities)]
            return ((self.combinedforces, self.data['velocities'], powers, self.data['times']),)
        else:
            powers1 = [force * 9.81 * abs(velocity) for force, velocity in zip(self.data['forces1'], self.velocities)]
            powers2 = [force * 9.81 * abs(velocity) for force, velocity in zip(self.data['forces2'], self.velocities)]
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
    
    def calibrate(self):
        self.calibration_factor1 = self.force1
        self.calibration_factor2 = self.force2