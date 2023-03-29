"""
Module responsible for saving sessiondata
Only communicates with controller

Author: Jitse van Esch
Date: 24-03-23
"""
from settings import Paths
from collections import namedtuple
import csv

class Model():
    def __init__(self):
        # Initialise saving dictionarys
        self.userdetails = {'userID': None,
                            'name': None,
                            'height': None,
                            'gender': None,
                            'sport': None}
        self.sessiondetails = {'resultID': None,
                               'weight': None,
                               'pushheight': None,
                               'date': None}
        
        self.rawdata = {'force': [],
                        'velocity': [],
                        'power': [],
                        'time': []}
        
        self.analyseddata = {'peakforce': None,
                            'meanforce': None,
                            'timetopeakforce': None,
                            'best_rfd': None,
                            'power_avg': None,
                            'velocity_avg': None,
                            'distance': None,
                            'peak_acc': None,
                            'fatigability': None,
                            'timetofatigue': None}
        
        self.compareddata = self.analyseddata.copy()
        
    def set_userdetails(self, user):
        """ Method that takes a user from the database and saves it to the model """
        self.userdetails = {
        'userID': user[0],
        'name': f'{user[1]} {user[2]}',
        'height': user[5],
        'gender': user[4],
        'sport': user[3]
        }
    
    def set_sessiondetails(self, sessiondetails):
        self.sessiondetails = {
            'resultID': sessiondetails[0],
            'weight': sessiondetails[2],
            'pushheight': sessiondetails[3],
            'date' : sessiondetails[4]
        }
        
    def get_userdetails(self):
        return self.userdetails
    
    def set_rawdata(self, rawdata):
        self.rawdata = rawdata

    def get_details_for_email(self):
        return self.userdetails['name'], self.sessiondetails['date'], self.sessiondetails['resultID']
    
    def load_data_from_csv(self):
        """ Method to get data from storage """
        # Initialize paths
        rawpath = Paths.PATH_RAWDATA + str(self.sessiondetails['resultID']) + '.csv'
        analysedpath = Paths.PATH_ANALYSEDDATA + str(self.sessiondetails['resultID']) + '.csv'

        # Load the data from the files
        with open(rawpath) as f1, open(analysedpath) as f2:
            file1 = list(csv.DictReader(f1))
            file2 = list(csv.DictReader(f2))
            
            self.rawdata = {k: [float(col[k]) for col in file1] for k in file1[0].keys()}
            self.analyseddata = {k: float(col[k]) for k in file2[0].keys() for col in file2}