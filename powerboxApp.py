"""
This file is the main controller of the powerBox-v2 application
All frontend is built with Gtk4, a gnome linux GUI framework

Date last checked: 24-03-23
Author: Jitse van Esch
"""
# Framework imports
import tkinter as tk
import customtkinter as ctk

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
        self.md = Model()

        self.fstack = []  # Stack of loaded frames
        self.options = {'n_users': 2, 'start_mode': 1, 
                        'for_measurement':True, 'creating':False}  # run options for the application

        
        # Container for loading frames
        self.container = tk.Frame(self) #Todo: See if this needs to be ctk
        self.container.pack(side='top', fill='both', expand=True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Load home
        self.home()
        return

    def home(self):
        """ Method that loads home frame and clears the session data """

        # Destroy all frames in stack
        for f in self.fstack:
            f.destroy()

        # Clear stack
        self.fstack.clear()

        # Reinitialize model
        self.model = Model()

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