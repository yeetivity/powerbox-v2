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
        self.compute_fatigue(p, f, t)
        
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
    
    def compute_fatigue(self, p, f, t):
        # Todo: implement RFD algorithm
        if round(np.mean(p),1) == 0.0:
            reference = f
        else:
            reference = p

        # Step 1: trim data
        # Step 1a: round data for better trimming
        reference_rounded = [self.custom_round(num, 5) for num in reference]
        # Step 1b: detect non-zero elements and determine first and last
        nonzero_indices = np.nonzero(reference_rounded)[0]
        # Step 1c: trim reference and time
        reference = reference[nonzero_indices[0]:nonzero_indices[-1]]
        t_trimmed = t[nonzero_indices[0]:nonzero_indices[-1]]

        # Step 2: Compute linear trend
        coefficients = np.polyfit(t_trimmed, reference, 1)  # Fit a first-degree polynomial
        trend = np.polyval(coefficients, t)

        # Step 3: compute decline percentage
        self.analysed['fatigability'] = round((trend[-1] * 100 / trend[0]), 2)
        
        self.analysed['timetofatigue'] = 42
    
    def custom_round(x, base=5):
        """ Custom rounding method that can round based on different bases """
        return base * round(x/base)

    def compare_data(self, current_data, lastresult, personalbests):
        """
        Compares two dictionaries of data and outputs their comparison.

        :param current_data: analyzed values from the inputted measurement
        :type current_data: dict
        :param lastresult: analyzed values from the last result of the user
        :type lastresult: dict
        :param personalbests: personal best values
        :type personalbests: tuple
        :return:    comparison: dictionary with percentual comparison
                    new_pbs: dictionary with new personal bests
        :rtype: dict
        """

        # Initialise dictionaryies
        comparison = {key: [0, 0] for key in current_data}
        new_pbs = {}

        pbs_up = {'peakforce', 'meanforce', 'best_rfd', 'power_avg', 'velocity_avg', 'distance', 'peak_acc', 'fatigability'}  # Personal bests that need to go up, to be better
        pbs_down = {'timetopeakforce', 'timetofatigue'}  # Personal bests that need to go down, to be better
        
        pb_dict = dict(zip(list(current_data.keys()), personalbests[1:]))
        
        for key, value in current_data.items():
            lr_val = lastresult.get(key, 0)  # Value of last result
            pb_val = pb_dict.get(key, 0)  # Value of personal best

            # Comparison for last result
            if lr_val != 0:
                comparison[key][0] = (value * 100) / lr_val

            # Comparison for personal best
            if pb_val!= 0:
                comparison[key][1] = (value * 100) / pb_val
                if key in pbs_up and value > pb_val:
                    new_pbs[key] = value
                elif key in pbs_down and value < pb_val:
                    new_pbs[key] = value
            else:
                new_pbs[key] = value
        
        return comparison, new_pbs

        
        
        
        