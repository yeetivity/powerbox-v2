"""
This file is the main controller of the powerBox-v2 application
All frontend is built with Gtk4, a gnome linux GUI framework

Date last checked: 24-03-23
Author: Jitse van Esch
"""
# Framework imports
import tkinter as tk
import customtkinter as ctk

# Functionality imports
from collections.abc import MutableMapping
from collections import deque
import copy
import threading as t
import time
import csv
import numpy as np

# Frontend imports
import frontend.home
import frontend.result_view
from frontend.result_view import ResultView
import frontend.data_view
from frontend.data_view import DataView
import frontend.user_view
import frontend.user_create
import frontend.user_select

# Backend imports
from backend.database import Database
from backend.model import Model
from backend.data_analyser import DataAnalyser
from backend.data_reader import DataReader
from backend.email_generator import EmailGenerator 
from backend.pdf_generator import PDFGenerator

# Settings imports
from settings import ApplicationSettings
from settings import Paths

class powerboxApplication(ctk.CTk):
    # Root window
    def __init__(self):
        super().__init__()

        # Initialisations      
        self.db = Database(Paths.PATH_DATABASE)
        self.email_generator = EmailGenerator()
        self.analyser = DataAnalyser()
        self.pdf_generator = PDFGenerator()

        self.fstack = []  # Stack of loaded frames
        self.options = OptionDict({'n_users': 1, 
                        'start_mode': 1, 
                        'for_measurement':True, 
                        'creating':False})  # run options for the application
        self.options.register_callback('n_users', self.n_users_callback)
        
        # Container for loading frames
        self.container = tk.Frame(self) #Todo: See if this needs to be ctk
        self.container.pack(side='top', fill='both', expand=True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Load home
        self.home()
        return

    def n_users_callback(self, key, value):
        if key != 'n_users':
            return
        if value == 1 and self.models[1] != None:
            # Single user mode, but the second model still exists
            del self.models[1]
        elif value == 2 and self.models[1] == None:
            # Double user mode, but second model doesn't exist
            self.models[1] = copy.copy(self.models[0])
        return
            
    def home(self):
        """ Method that loads home frame and clears the session data """

        # Destroy all frames in stack
        for f in self.fstack:
            f.destroy()

        # Clear stack
        self.fstack.clear()

        # Reinitialize
        self.models = [Model(), None]
        self.options['for_measurement'] = True
        self.options['creating'] = False

        # Show home
        self.show(frontend.home.Home)
        return
    
    def show(self, frame):
        """
        Method that loads frame and moves it to the top of the stack
        
        =INPUT=
        frame   tk.Frame inherited class
        """

        # Create frame instance in the container, and pass the controller
        f = frame(self.container, self)

        # Add frame to the stack
        self.fstack.append(f)

        # Display frame
        f.grid(row=0, column=0, sticky='nsew')  # Sticky: makes frame stick to all sides
        f.tkraise()
        return

    def back(self):
        """ Method to go back to the previous frame """
        # Display previous frame
        f = self.fstack[-2]
        f.tkraise()

        # Destroy old frame
        self.fstack[-1].destroy()

        # Take frame out of the stack
        self.fstack.pop()
        return

    def goto_userselect(self):
        # Show the userselect screen
        self.show(frontend.user_select.UserSelect)
        # Show the users
        self.fstack[-1].update_userlist(self.get_users())
        print('goto_userselect')
        
    def goto_usercreate(self):
        self.show(frontend.user_create.UserCreate)
        
        if self.options['for_measurement'] and not self.options['creating']:
            userdetails = []
            for i in range(self.options['n_users']):
                userdetails.append(self.models[i].get_userdetails())
            # Get userdetails from model
            self.fstack[-1].configure_UI(userdetails)
        # Fill out userdetails
        print('goto_usercreate')

    def goto_userview(self, userID):
        self.show(frontend.user_view.UserView)
        
        # Get all the user information
        userdetails = self.db.get_userdetails(userID)
        personalbests = self.db.get_userpbs(userID)
        userresults = self.db.get_userresults(userID)
        
        userinfo = (userdetails, personalbests, userresults)
        
        # Write the user details to the model
        self.models[0].set_userdetails(userdetails)
        
        # Add the user to the screen
        self.fstack[-1].display_user(userinfo)
        print('goto_userview')

    def goto_result(self, resultID=None):
        # NOTE: This class can only take one result
        
        if not self.options['for_measurement']:
            # Get session details from db and send them to model
            self.db_sessiondetails_to_models(self.get_result(resultID=resultID))
            self.models[0].load_data_from_csv()
            analysis_thread = t.Thread(target=self.start_comparison, args=(self.models[0],))
            analysis_thread.start()
        
        self.show(frontend.result_view.ResultView)
        print('goto_results')

    def goto_dataview(self):
        self.show(frontend.data_view.DataView)

        if isinstance(self.fstack[-1], DataView):
            # Start data reader thread; give it a pointer to the dataview
            stop_flag = t.Event()
            self.measuring_thread = DataReader(stop_flag, self.fstack[-1], self.options['n_users'])
            self.measuring_thread.start()
        
            print('measurement thread started...')

    def stop_measurement(self):
        self.stop_measurement_thread() # Stops the thread
        
        if self.options['start_mode'] == 1:
            # If default start mode, save data to model
            data = self.measuring_thread.get_data(self.options['n_users'])
            # Create a box for the analysis threads
            self.analyser_threads = [None, None]
            for i in range(self.options['n_users']):
                self.models[i].set_rawdata(data[i])
                self.analyser_threads[i] = t.Thread(target=self.start_analysis, args=(self.models[i],))
                self.analyser_threads[i].start()
            
            if self.options['n_users'] == 2:
                self.fstack[-1].display_msg()
                self.home()
                return
            else:
                self.goto_result()
        else:
            # Quickstart mode, don't save or analyse data
            self.home()
    
    def stop_measurement_thread(self):
        if self.measuring_thread != None:
            self.measuring_thread.stop()
            self.measuring_thread.join()
            print('Thread closed')
    
    def get_users(self, filter1=None, filter2=None):
        return self.db.get_users(filter1, filter2)
    
    def get_result(self, resultID):
        return self.db.get_result(resultID)

    def userIDs_to_models(self, userIDs):
        # Get the user from the db and write to the model
        for i  in range(self.options['n_users']):
            user = self.db.get_userdetails(userIDs[i])
            self.models[i].set_userdetails(user)
        return
    
    def user_to_database(self, userdetails):
        userID = self.db.add_user(userdetails)
        print(f'database confirmed that {userID} is added')
        return userID

    def db_sessiondetails_to_models(self, sessiondetails):
        #This is specifically for one user
        self.models[0].set_sessiondetails(sessiondetails)

    def session_details_to_model(self, sessiondetails):
        # This can be for two users
        for i in range(self.options['n_users']):
            self.models[i].set_sessiondetails(sessiondetails[i])
  
    def start_analysis(self, model):
        self.analyser.analyse_model(model)
        self.start_comparison(model)
        self.save_model(model)
    
    def start_comparison(self, model):
        # Note: runs in thread
        # Get last analysed data #Todo: this might not be the last data, but the current data...
        last_result_info = self.db.get_lastresult(model.userdetails['userID'])
        analysedpath = Paths.PATH_ANALYSEDDATA + str(last_result_info[0]) + '.csv'
        with open(analysedpath) as f1:
            file1 = list(csv.DictReader(f1))
            last_result = {k: float(col[k]) for k in file1[0].keys() for col in file1}
        
        # Get personal bests
        pbs = self.db.get_userpbs(model.userdetails['userID'])
        
        # Create comparison
        comparison, new_pbs = self.analyser.compare_data(model.analyseddata, last_result, pbs)
        
        # Write to model
        model.compareddata = comparison

        # Update database
        self.update_db_pbs(new_pbs, model.userdetails['userID'])

        # Create pdf
        self.pdf_generator.create_pdf(model)
        
        # Update resultview (first check if we are seeing resultview)
        if isinstance(self.fstack[-1], ResultView):
            self.fstack[-1].update_pdf()
        else:
            print("Analysis done before the resultview was triggered")
            
    def send_email(self, receiver):
        username, date, resultID = self.models[0].get_details_for_email()

        email_thread = t.Thread(target=self.compose_email, args=(receiver, username, date, resultID))
        email_thread.start()
        return

    def compose_email(self, receiver, name, date, ID):
        # Generate and send email
        sent = self.email_generator.send_email(receiver_adress=receiver, username=name, date=date, resultID=ID)
        # Update UI if sucessful
        if sent and isinstance(self.fstack[-1], ResultView):
            # If the last frame is still the resultview; show that email is sent
            self.fstack[-1].email_sent()
        elif isinstance(self.fstack[-1], ResultView):
            self.fstack[-1].email_error()
    
    def save_model(self, model):
        # Get the modeldata
        usrID, modeldata = model.get_model_data()
        
        # Save resultentry to database -> returns ID to which it is saved
        resultID = self.db.add_resultentry(usrID, modeldata[0])
        model.set_resultID(resultID)
        
        # Define locations to save data to
        path_rawresult = Paths.PATH_RAWDATA + str(resultID) + '.csv'
        path_analysedresult = Paths.PATH_ANALYSEDDATA + str(resultID) + '.csv'
        
        # Write to csv
        self.write_to_csv(modeldata[1], path_rawresult)
        self.write_to_csv(modeldata[2], path_analysedresult)
        
    def write_to_csv(self, dictionary, path):
        """ Method to save a dictionary to a csv """
               
        with open(path, 'w', newline='') as outfile:         
            writer = csv.writer(outfile)
            writer.writerow(dictionary.keys())

            if isinstance(next(iter(dictionary.values())), (list, deque)):
                # Iterate over the rows and write them to the CSV file
                for row in zip(*dictionary.values()):
                    writer.writerow(row)
            else:
                writer.writerow(dictionary.values())

        print("Successfully written to CSV")

    def update_db_pbs(self, new_pbs, usrID):
        """
        Loops through the dictionary of new_pbs and updates the database accordingly

        :param new_pbs: new personal bests
        :type new_pbs: dict
        """

        for key, value in new_pbs.items():
            self.db.update_pb(usrID, key, value)

    def update_calibration_factor(self):
        self.measuring_thread.calibrate()
class OptionDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)
        self._callbacks = {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        if key in self._callbacks:
            for callback in self._callbacks[key]:
                callback(key, value)

    def __delitem__(self, key):
        del self._data[key]
        if key in self._callbacks:
            del self._callbacks[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def register_callback(self, key, callback):
        if key not in self._callbacks:
            self._callbacks[key] = []
        self._callbacks[key].append(callback)

def main():
    app = powerboxApplication()

    # Window settings
    placement_x = (app.winfo_screenwidth() // 2) - (ApplicationSettings.WINDOW_WIDTH // 2)
    placement_y = (app.winfo_screenheight() // 2) - (ApplicationSettings.WINDOW_HEIGHT // 2)
    app.geometry('{}x{}+{}+{}'.format(ApplicationSettings.WINDOW_WIDTH, ApplicationSettings.WINDOW_HEIGHT, placement_x, placement_y))
    app.resizable(0,0) #Don't allow resizing

    app.title("POWERBOX")

    app.mainloop()

if __name__ == "__main__":
    main()