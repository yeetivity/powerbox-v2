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
        #Todo: create email functionality 
        receiver = askstring(prompt="At what emailadress would you like to receive your results?", 
                          title="Please input your emailadress")
        if receiver is not None:
            self.wait_txt = ctk.CTkLabel(master=self,
                                    text="Processing your report...",
                                    text_color=style.CLR_ACCENT,
                                    font=style.FNT_OVERLINE_IT,
                                    anchor='n')
            self.wait_txt.place(x=400, y=23, anchor='n')
            
            self.wait_bar = ctk.CTkProgressBar(master=self,
                                            width=400,
                                            height=11,
                                            border_color=style.CLR_PRIMARY,
                                            fg_color=style.CLR_BACKGROUND,
                                            progress_color=style.CLR_ACCENT,
                                            orientation='horizontal',
                                            indeterminate_speed=0,
                                            determinate_speed=0.5)
            self.wait_bar.place(x=200, y=43)
            self.wait_bar.start()
            
            self.controller.send_email(receiver)
        else:
            print('No emailadress was inputted')
    
    def email_sent(self):
        # Update UI
        self.wait_txt.configure(text="Email sent")
        self.wait_bar.stop()
        self.wait_bar.place_forget()

        # Display messagebox
        ctk.set_appearance_mode('dark')
        CTkMessagebox(title="Email sent", 
                          message="Your email is succesfully sent, and should arrive shortly",
                          icon='check', option_1='OK')
        return  
    
    def email_error(self):
        # Update UI
        self.wait_txt.configure(text="Something went wrong")
        self.wait_bar.stop()

    def home(self):
        self.controller.home()
        return
    
    def update_pdf(self):
        # Stop the waitbar
        self.pdfwait_bar.stop()
        self.pdfwait_bar.place_forget()
        
        # Take away message
        self.pdfwait_txt.place_forget()
        
        # Display pdf        
        v1 = tkpdf.ShowPdf()
        pdf_view = v1.pdf_view(self, width=716, height=480-97, pdf_location=paths.PATH_REPORT)
        pdf_view.place(x=42, y=77, width=716, height=480-97, anchor='nw')

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
        self.pdfwait_txt = ctk.CTkLabel(master=self,
                                    text="Processing your data...",
                                    text_color=style.CLR_ACCENT,
                                    font=style.FNT_OVERLINE_IT,
                                    anchor='n')
        self.pdfwait_txt.place(x=400, y=77, anchor='n')
        
        self.pdfwait_bar = ctk.CTkProgressBar(master=self,
                                        width=600,
                                        height=11,
                                        border_color=style.CLR_PRIMARY,
                                        fg_color=style.CLR_BACKGROUND,
                                        progress_color=style.CLR_ACCENT,
                                        orientation='horizontal',
                                        indeterminate_speed=0,
                                        determinate_speed=0.5)
        self.pdfwait_bar.place(x=100, y=100)
        self.pdfwait_bar.start()
        return