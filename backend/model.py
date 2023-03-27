"""
Module responsible for saving sessiondata
Only communicates with controller

Author: Jitse van Esch
Date: 24-03-23
"""
from settings import Paths
from collections import namedtuple

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
                               'pushheight': None}
        
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
            'weight': sessiondetails[1],
            'pushheight': sessiondetails[2]
        }
        
    def get_userdetails(self):
        return self.userdetails