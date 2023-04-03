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
import random
class DataReader():
    def __init__(self):
        self.data = {'forces1' : deque(),
                     'forces2' : deque(),
                     'velocities' : deque(),
                     'times' : deque()}

        self.combinedforces =  deque()
        self.meanforce = np.zeros(2)
        self.peakforce = np.zeros(2)
        self.a = 0.1

    def start(self, datascreen, n_users):
        """
        Method that starts gathering data
        =INPUT=
        datascreen      reference to UI to publish data on
        n_users         the amount of users
        """
        # Init
        self.ui = datascreen
        packet_time = 0
        self.measuring = True
        velocity_old = 0

        # TODO: UNCOMMENT WHEN CONNECTED TO PI PICO
        # Setup serial readout
        port = serial.Serial('/dev/ttyACM0')
        port.flushInput()

        received_bytes = bytearray(8)

        while self.measuring:
            # TODO: UNCOMMENT WHEN CONNECTED TO PI PICO
            # Read the received bytes into the bytearray
            port.readinto(received_bytes)

            # # Extract the force and velocity values
            # force1, force2, velocity = struct.unpack_from('fff', received_bytes)
            # force1, force2, velocity = self.generate_random(n_users)
            force1 = 1
            force2 = 1
            n_lines, velocity = struct.unpack('ff', received_bytes)
            print(velocity)

            # Filter velocity
            velocity_filtered = self.a * v + (1 - self.a) * velocity_old
            velocity_old = velocity_filtered

            # # TODO: take away when connected to pi pico
            # t.sleep(0.1)

            # Update the data dictionary
            self.data['forces1'].append(force1)
            self.data['forces2'].append(force2)
            self.data['velocities'].append(velocity)
            self.data['times'].append(packet_time)
            
            # Update time
            packet_time += (1 / ApplicationSettings.FREQUENCY)

            if n_users == 1:
                self.combinedforces.append(max(force1, force2))

            # Update running average and peakforce
            if n_users == 2:
                self.meanforce[0] = np.mean(self.data['forces1'])
                self.meanforce[1] = np.mean(self.data['forces2'])
                self.peakforce[0] = np.max(self.data['forces1'])
                self.peakforce[1] = np.max(self.data['forces2'])
            elif n_users == 1:
                self.meanforce[0] = np.mean(self.combinedforces)
                self.peakforce[0] = np.mean(self.combinedforces)

            # Update time on 8 Hz
            if round(packet_time, 3) % (1 / ApplicationSettings.UPDATE_TIME_FREQUENCY) == 0:
                self.update_ui_time(packet_time)
            
            # Update vars on 4 Hz
            if round(packet_time, 3) % (1 / ApplicationSettings.UPDATE_VARS_FREQUENCY) == 0:
                if n_users == 1:
                    self.update_ui_vars_1p(self.combinedforces, velocity, self.peakforce, self.meanforce)
                else:
                    self.update_ui_vars_2p(force1, force2, velocity, self.peakforce)

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
        """ Method to stop gathering data """
        self.measuring = False

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