# Framework imports
import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from CTkMessagebox import CTkMessagebox

# Frontend information
from settings import StyleElements as style
from settings import Paths as paths

class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)

        self.controller = controller
        self.populate_UI()
        return

    def connect_sensor(self):
        print('yow')
        return
    
    def switch_usernr(self):
        print('usernr switched')
        if self.controller.options['n_users'] == 1:
            self.btn_switch_usernr.configure(image=self.IC_DOUBLEUSER)
            self.controller.options['n_users'] = 2
        else:
            self.btn_switch_usernr.configure(image=self.IC_SINGLEUSER)
            self.controller.options['n_users'] = 1
        return
    
    def goto_userresults(self):
        print('goto userresults')
        return

    def quickstart(self):
        print('quickstart')
        return
    
    def start(self):
        print('start')
        return

    def populate_UI(self):
        """ Class method to place all widgets """
        # ------------------
        #   IMAGES USED
        # ------------------
        IC_CONNECTSENSOR = ctk.CTkImage(OpenImage(paths.PATH_IC_CONNECTSENSOR), size=(55,72))
        self.IC_SINGLEUSER = ctk.CTkImage(OpenImage(paths.PATH_IC_SINGLEUSER), size=(50,72))
        self.IC_DOUBLEUSER = ctk.CTkImage(OpenImage(paths.PATH_IC_DOUBLEUSER), size=(50,72))
        IC_QUICKSTART = ctk.CTkImage(OpenImage(paths.PATH_IC_QUICKSTART), size=(180,186))
        IC_START = ctk.CTkImage(OpenImage(paths.PATH_IC_START), size=(150,186))
        IC_FINDUSERS = ctk.CTkImage(OpenImage(paths.PATH_IC_FINDUSERS), size=(83,72))
        LOGO_PB_SMALL = ctk.CTkImage(light_image=OpenImage(paths.PATH_LOGO_PB_SMALL),
                                     dark_image=OpenImage(paths.PATH_LOGO_PB_SMALL),
                                     size=(222,24))

        # ------------------
        #   NAVIGATION BAR
        # ------------------
        btn_connectsensor = ctk.CTkButton(master=self,
                                          width=55,
                                          height=72,
                                          text="",
                                          bg_color=style.CLR_BACKGROUND,
                                          fg_color=style.CLR_BACKGROUND,
                                          command=self.connect_sensor,
                                          image=IC_CONNECTSENSOR)
        btn_connectsensor.place(x=16, y=18)
        
        self.btn_switch_usernr = ctk.CTkButton(master=self,
                                          width=50,
                                          height=72,
                                          text="",
                                          bg_color=style.CLR_BACKGROUND,
                                          fg_color=style.CLR_BACKGROUND,
                                          command=self.switch_usernr,
                                          image=self.IC_SINGLEUSER)
        self.btn_switch_usernr.place(x=86, y=18)
        
        btn_user_results = ctk.CTkButton(master=self,
                                          width=83,
                                          height=72,
                                          text="",
                                          bg_color=style.CLR_BACKGROUND,
                                          fg_color=style.CLR_BACKGROUND,
                                          command=self.goto_userresults,
                                          image=IC_FINDUSERS)
        btn_user_results.place(x=692, y=18)
        
        # ------------------
        #   START BUTTONS
        # ------------------       
        btn_quickstart = ctk.CTkButton(master=self,
                                          width=180,
                                          height=186,
                                          text="",
                                          bg_color=style.CLR_BACKGROUND,
                                          fg_color=style.CLR_BACKGROUND,
                                          hover=False,
                                          command=self.quickstart,
                                          image=IC_QUICKSTART)
        btn_quickstart.place(x=181, y=167)
        
        btn_start = ctk.CTkButton(master=self,
                                          width=150,
                                          height=186,
                                          text="",
                                          bg_color=style.CLR_BACKGROUND,
                                          fg_color=style.CLR_BACKGROUND,
                                          hover=False,
                                          command=self.start,
                                          image=IC_START)
        btn_start.place(x=460, y=167)
        
        # ------------------
        #   LOGO
        # ------------------  
        img_logo = ctk.CTkLabel(master=self,
                                text="",
                                width=222,
                                height=24,
                                image=LOGO_PB_SMALL,
                                bg_color=style.CLR_BACKGROUND)
        img_logo.place(x=16, y=440)