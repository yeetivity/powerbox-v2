import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths
from settings import ApplicationSettings as appsettings

class UserCreate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)
    
        for_measurement = controller.options['for_measurement']
        creating = controller.options['creating']
                
        self.populate_UI(for_measurement, creating)
        self.configure_UI(creating)
        return
    
    def back(self):
        print('back')
        return

    def finish(self):
        print('save')
        return

    def sportmenu_callback(self, choice):
        print(choice)
        return

    def genderbutton_callback(self, choice):
        print(choice)
        return

    def populate_UI(self, for_measurement, creating):
        # ------------------
        #   IMAGES USED
        # ------------------
        IC_BACK = ctk.CTkImage(OpenImage(paths.PATH_IC_BACK), size=(40,40))
        IC_CHECKMARK = ctk.CTkImage(OpenImage(paths.PATH_IC_CHECKMARK), size=(40,40))
        
        # ------------------
        #   NAVIGATION BAR
        # ------------------
        btn_back = ctk.CTkButton(master=self,
                                 width=40,
                                 height=51,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.back,
                                 image=IC_BACK)
        btn_back.place(x=16, y=4)

        btn_back = ctk.CTkButton(master=self,
                                 width=40,
                                 height=51,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.finish,
                                 image=IC_CHECKMARK)
        btn_back.place(x=744, y=4)

        # ------------------
        #   MIDDLE FRAME
        # ------------------
        mid_frame = ctk.CTkFrame(self, 
                              width=500,
                              height=370,
                              fg_color=style.CLR_BACKGROUND_ALT)
        mid_frame.place(x=150, y=76)
        mid_frame.grid_propagate(False)

        # Title
        if creating:
            title_txt = "Create your profile"
        else:
            title_txt = "Your profile"
        frame_title = ctk.CTkLabel(master=mid_frame,
                                   text=title_txt,
                                   font=style.FNT_H4,
                                   width=400,
                                   height=32,
                                   bg_color=style.CLR_BACKGROUND_ALT
                                  )
        frame_title.grid(row=0, column=0, columnspan=5, ipady=8)

        # Row Spacer
        spacer = ctk.CTkLabel(master=mid_frame,
                              text="",
                              height=14)
        spacer.grid(row=1, column=0, columnspan=5)

        # Name input
        self.name_entry = ctk.CTkEntry(master=mid_frame,
                                       placeholder_text="Insert your name",
                                       width=400,
                                       height=32,
                                       border_width=2,
                                       corner_radius=10,
                                       font=style.FNT_BODY,
                                       border_color=style.CLR_PRIMARY)
        self.name_entry.grid(row=2, column=0, columnspan=5, padx=50, pady=4, sticky='ew')

        # Sport input
        self.sportmenu_var = ctk.StringVar(value="Choosing...")
        self.sportmenu = ctk.CTkOptionMenu(master=mid_frame,
                                           values=appsettings.SPORTS,
                                           command=self.sportmenu_callback,
                                           width=400,
                                           height=32,
                                           corner_radius=10,
                                           variable=self.sportmenu_var,
                                           fg_color=style.CLR_PRIMARY,
                                           text_color=style.CLR_WHITE,
                                           button_color=style.CLR_SECONDARY,
                                           font=style.FNT_BODY,
                                           dropdown_font=style.FNT_BODY,
                                           dynamic_resizing=False,
                                           hover=False)
        self.sportmenu.grid(row=3, column=0, columnspan=5, padx=50, pady=4, sticky='ew')

        # Gender input
        genderbutton_var = ctk.StringVar(value="Male")
        self.genderbutton = ctk.CTkSegmentedButton(master=mid_frame,
                                              values=appsettings.GENDERS,
                                              variable=genderbutton_var,
                                              command=self.genderbutton_callback,
                                              height=32,
                                              corner_radius=10,
                                              fg_color=style.CLR_PRIMARY,
                                              unselected_color=style.CLR_PRIMARY,
                                              unselected_hover_color=style.CLR_SECONDARY,
                                              selected_color=style.CLR_ACCENT_DARKENED,
                                              selected_hover_color=style.CLR_ACCENT_DARKENED)
        self.genderbutton.grid(row=4, column=0, columnspan=5, sticky='ew', pady=4, padx=(50,50))

        # Length input
        self.length_entry = ctk.CTkEntry(master=mid_frame,
                                        placeholder_text="Insert length",
                                        height=32,
                                        border_width=2,
                                        corner_radius=10,
                                        border_color=style.CLR_PRIMARY,
                                        font=style.FNT_BODY)
        self.length_entry.grid(row=5, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

        # Length unit
        length_unit = ctk.CTkLabel(master=mid_frame,
                                   text="cm",
                                   height=32,
                                   anchor='w',
                                   font=style.FNT_BODY)
        length_unit.grid(row=5, column=4, padx=(0,50), ipadx=6, sticky='ew')

        if for_measurement:
            # Row Spacer
            spacer2 = ctk.CTkLabel(master=mid_frame,
                                text="",
                                height=28)
            spacer2.grid(row=6, column=0, columnspan=5)

            # Weight input
            self.weight_entry = ctk.CTkEntry(master=mid_frame,
                                            placeholder_text="Insert current weight",
                                            height=32,
                                            border_width=2,
                                            corner_radius=10,
                                            border_color=style.CLR_ACCENT,
                                            font=style.FNT_BODY)
            self.weight_entry.grid(row=7, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

            # Weight unit
            weight_unit = ctk.CTkLabel(master=mid_frame,
                                    text="kg",
                                    height=32,
                                    anchor='w',
                                    font=style.FNT_BODY)
            weight_unit.grid(row=7, column=4, padx=(0,50), ipadx=6, sticky='ew')

            # Pushheight input
            self.pushheight_entry = ctk.CTkEntry(master=mid_frame,
                                            placeholder_text="Insert pushheight",
                                            height=32,
                                            border_width=2,
                                            corner_radius=10,
                                            border_color=style.CLR_ACCENT,
                                            font=style.FNT_BODY)
            self.pushheight_entry.grid(row=8, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

            # Pushheight unit
            pushheight_unit = ctk.CTkLabel(master=mid_frame,
                                    text="kg",
                                    height=32,
                                    anchor='w',
                                    font=style.FNT_BODY)
            pushheight_unit.grid(row=8, column=4, padx=(0,50), ipadx=6, sticky='ew')

        return   

    def configure_UI(self, creating):
        if not creating:
            # self.controller.get_user_details()
            # todo: prefill everything
            # todo: disabled color fix
            
            # Disable inputs
            self.name_entry.configure(state='disabled')
            self.sportmenu.configure(state='disabled')
            self.genderbutton.configure(state='disabled')
            self.length_entry.configure(state='disabled')
