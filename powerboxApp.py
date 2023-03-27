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
import copy

# Frontend imports
import frontend.home
import frontend.result_view
import frontend.data_view
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

        # Reinitialize model
        self.models = [Model(), None]

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
        
        # Add the user to the screen
        self.fstack[-1].display_user(userinfo)
        print('goto_userview')

    def goto_result(self, resultID):
        # Fetch results for resultID and store them to temp storage
        # Todo: do something
        # Show resultview
        self.show(frontend.result_view.ResultView)
        print('goto_results')

    def start_measurement(self):
        # Todo: start the data_reader thread
        self.show(frontend.data_view.DataView)
        print('goto_dataview')

    def get_users(self, filter1=None, filter2=None):
        return self.db.get_users(filter1, filter2)
    
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

    def sessiondetails_to_models(self, sessiondetails):
        # Save sessiondetails to models
        print('sessiondetails sent to database and model')
            
            
        
    
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