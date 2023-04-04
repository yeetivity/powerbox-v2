"""
Module responsible for analysing a data dictionary with force, velocity and time
It can also compare an existing analysis to other analyses (e.g. personal bests or another result)
Can return analysed data dictionary or comparison dictionary

=NOTE=
Should run in a thread

Author: Jitse van Esch
Date: 28-03-23
"""
import numpy as np
import scipy
import math

class DataAnalyser():
    def __init__(self):
        pass
    
    def analyse_model(self, model):
        """
        Analyses raw data and outputs processed data
        =INPUT=
        model
        """
        # Create empty analysed data
        self.analysed = {}
        
        # Convert lists to numpy arrays
        f = np.array(model.rawdata['force'])
        v = np.array(model.rawdata['velocity'])
        p = np.array(model.rawdata['power'])
        t = np.array(model.rawdata['time'])
        
        # Do analysis
        self.analyse_force(f, t)
        self.analysed['power_avg'] = np.average(p)
        self.analyse_velocity(v, t)
        self.compute_fatigue()
        
        # Write to model
        model.analyseddata = self.analysed
        
    def analyse_force(self, f, t):
        self.analysed['peakforce'] = np.max(f)
        self.analysed['meanforce'] = np.average(f)
        
        # Time to peak force
        self.analysed['timetopeakforce'] = t[f.argmax()] - t[0]  # Todo: Replace for peak and valley detection
        
        # Compute RFDs
        self.analysed['best_rfd'] = 0 # Todo: replace for RFD algorithm
        
    def analyse_velocity(self, v, t):
        self.analysed['velocity_avg'] = np.average(v)
        self.analysed['distance'] = sum(np.multiply(v, t))
        
        # Differentiation to get acceleration
        a = np.diff(v) / np.diff(t)
        self.analysed['peak_acc'] = np.max(a)
    
    def compute_fatigue(self):
        # Todo: create algorithm for this
        # Compute based on RFD
        rfd_fatigue = 0
        
        # Compute based on power
        pwr_fatigue = 0
        
        # Combine
        fatigue = 0
        
        self.analysed['fatigability'] = fatigue
        self.analysed['timetofatigue'] = 10000
        
    def compare_data(self, current_data, lastresult, personalbests):
        """
        Compares two dictionaries of data and outputs their comparison
        =INPUT=
        current_data        dictionary with analysed values from requested measurement
        lastresult          dictionary with analysed values from last result
        personalbests       tuple with personal bests
        
        =OUTPUT=
        comparison          dictionary with percentual comparison
        new_pbs             dictionary with new personal bests
        
        =NOTE=
        Create a new pb dictionary
        """
        
        comparison = {}
        
        pbs = list(personalbests)[1:]  # Transform to a list and remove the first key
        keys = list(current_data)
        
        for key in keys:
            lr_val = lastresult.get(key)
            pb_val = pbs[keys.index(key)]
            if lr_val is not None and pb_val is not None:
                try:
                    lr_compared = (current_data[key] * 100) / lr_val
                except ZeroDivisionError:
                    lr_compared = 0
                try:
                    #todo: fix for divide by zero that doesnt give zerodivisionerror
                    pb_compared = (current_data[key] * 100) / pb_val
                except ZeroDivisionError:
                    pb_compared = 0
                    
                comparison[key] = [lr_compared if not math.isnan(lr_compared) else 0,
                                   pb_compared if not math.isnan(pb_compared) else 0]
        
        return comparison

        
        
        
        