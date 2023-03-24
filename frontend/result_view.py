import tkinter as tk
from tkinter.simpledialog import askstring
from tkPDFViewer import tkPDFViewer as tkpdf

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths

class ResultView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)

        self.controller = controller
        self.populate_UI()
        return

    def export(self):
        email = askstring(prompt="At what emailadress would you like to receive your results?", 
                          title="Please input your emailadress")
        ctk.set_appearance_mode('dark')
        if email is not None:
            wait_txt = ctk.CTkLabel(master=self,
                                    text="Processing your report...",
                                    text_color=style.CLR_ACCENT,
                                    font=style.FNT_OVERLINE_IT,
                                    anchor='n')
            wait_txt.place(x=400, y=23, anchor='n')
            
            wait_bar = ctk.CTkProgressBar(master=self,
                                            width=400,
                                            height=11,
                                            border_color=style.CLR_PRIMARY,
                                            fg_color=style.CLR_BACKGROUND,
                                            progress_color=style.CLR_ACCENT,
                                            orientation='horizontal',
                                            indeterminate_speed=0,
                                            determinate_speed=0.5)
            wait_bar.place(x=200, y=43)
            wait_bar.start()
        else:
            CTkMessagebox(title="Email sent", 
                          message="Your email is succesfully sent, and should arrive shortly",
                          icon='check', option_1='OK')
        return 
    
    def email_sent(self):
        print('email sent')
        return  
    
    def home(self):
        print('home')
        return
    
    def populate_UI(self):
        # ------------------
        #   IMAGES USED
        # ------------------
        IC_HOME = ctk.CTkImage(OpenImage(paths.PATH_IC_HOME), size=(40,54))
        IC_EXPORT = ctk.CTkImage(OpenImage(paths.PATH_IC_EXPORT), size=(50,61))

        # ------------------
        #   NAVIGATION BAR
        # ------------------
        btn_home = ctk.CTkButton(master=self,
                                 width=50,
                                 height=61,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.home,
                                 image=IC_HOME,
                                 anchor='sw')
        btn_home.place(x=42, y=4, anchor='nw')
               
        btn_export = ctk.CTkButton(master=self,
                                 width=50,
                                 height=61,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.export,
                                 image=IC_EXPORT,
                                 anchor='e')
        btn_export.place(x=716+42, y=4, anchor='ne')
                                      

        # ------------------
        #   PDF
        # ------------------
        v1 = tkpdf.ShowPdf()
        pdf_view = v1.pdf_view(self, width=716, height=480-97, pdf_location=paths.PATH_REPORT)
        pdf_view.place(x=42, y=77, width=716, height=480-97, anchor='nw')
        return