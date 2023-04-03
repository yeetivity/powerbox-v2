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
        
        # Convert lists to numpy arrays
        f = np.array(model.rawdata['force'])
        v = np.array(model.rawdata['velocity'])
        p = np.array(model.rawdata['power'])
        t = np.array(model.rawdata['time'])
        
        # Do analysis
        
    def compare_data(self, current_data, lastresult, personalbests):
        """
        Compares two dictionaries of data and outputs their comparison
        =INPUT=
        current_data        dictionary with analysed values from requested measurement
        lastresult          dictionary with analysed values from last result
        personalbests       tuple with personal bests
        
        =OUTPUT=
        comparison  dictionary with percentual comparison
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
                    pb_compared = (current_data[key] * 100) / pb_val
                except ZeroDivisionError:
                    pb_compared = 0
                    
                comparison[key] = [lr_compared if not math.isnan(lr_compared) else 0,
                                   pb_compared if not math.isnan(pb_compared) else 0]
        
        return comparison

        
        
        
        