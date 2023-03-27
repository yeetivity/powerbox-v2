import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths
from settings import ApplicationSettings as appsettings

class UserCreate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)
    
        self.controller = controller
        self.for_measurement = controller.options['for_measurement']
        self.creating = controller.options['creating']
        self.n_users = controller.options['n_users']

        self.name_vars = [None, None]
        self.sport_vars = [None, None]
        self.gender_vars = [None, None]
        self.height_vars = [None, None]
        self.weight_vars = [None, None]
        self.pushheight_vars = [None, None]
                
        self.populate_UI()
        return
    
    def back(self):
        self.controller.back()
        print('back')
        return

    def finish(self):
        if self.creating:
            # This can only have one user
            # Get the userdetails from tab 1
            name, sport, gender, height = (e.get() for e in (
            self.name_entries[0], self.sport_vars[0], self.gender_vars[0], self.height_entries[0]))

            # Send userdetails to database
            userID = self.controller.user_to_database((name, sport, gender, height))

            # Get sessiondetails
            if self.for_measurement:
                weight, push_height = (e.get() for e in (self.weight_entries[0], self.pushheight_entries[0]))

                # Send userdetails to models
                self.controller.userIDs_to_models((userID, None))
                
                # Send sessiondetails to models          
                self.controller.sessiondetails_to_models(([weight, push_height], None))
                self.controller.start_measurement()
                return
            else:
                self.controller.home()
                return

        elif self.for_measurement and not self.creating:
            # This can have two users
            sessiondetails = [None, None]
            for i in range(self.n_users):
                weight, push_height = (e.get() for e in (self.weight_entries[i], self.pushheight_entries[i]))
                sessiondetails[i] = [weight, push_height]

            self.controller.sessiondetails_to_models(sessiondetails)
            return   

    def populate_UI(self):
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
                              height=390,
                              fg_color=style.CLR_BACKGROUND_ALT)
        mid_frame.place(x=150, y=76)

        # Create tab view
        tab_view = ctk.CTkTabview(master=mid_frame,
                                  width=496,
                                  height=386,
                                  fg_color=style.CLR_BACKGROUND_ALT)
        tab_view.place(x=2, y=2)
        tab_view.grid_propagate(False)
        tab_view.add('User 1')
        self.fill_tabview(tab_view.tab('User 1'), 0)

        if self.for_measurement and self.n_users == 2:
            tab_view.add('User 2')
            self.fill_tabview(tab_view.tab('User 2'), 1)

        tab_view.set('User 1')
        
        return   

    def fill_tabview(self, tab, i):
        # Title
        if self.creating:
            title_txt = "Create your profile"
        else:
            title_txt = "Your profile"
        frame_title = ctk.CTkLabel(master=tab,
                                   text=title_txt,
                                   font=style.FNT_H5,
                                   width=400,
                                   height=32,
                                   bg_color=style.CLR_BACKGROUND_ALT
                                  )
        frame_title.grid(row=0, column=0, columnspan=5, ipady=8)

        # Row Spacer
        spacer = ctk.CTkLabel(master=tab,
                              text="",
                              height=4)
        spacer.grid(row=1, column=0, columnspan=5)

        # Name input
        self.name_vars[i] = ctk.StringVar()
        self.name_entry = ctk.CTkEntry(master=tab,
                                       placeholder_text="Insert your name",
                                       textvariable=self.name_vars[i],
                                       width=400,
                                       height=32,
                                       border_width=2,
                                       corner_radius=10,
                                       font=style.FNT_BODY,
                                       border_color=style.CLR_PRIMARY)
        self.name_entry.grid(row=2, column=0, columnspan=5, padx=50, pady=4, sticky='ew')

        # Sport input
        self.sport_vars[i] = ctk.StringVar(value="Choosing...")
        self.sportmenu = ctk.CTkOptionMenu(master=tab,
                                           values=appsettings.SPORTS,
                                           width=400,
                                           height=32,
                                           corner_radius=10,
                                           variable=self.sport_vars[i],
                                           fg_color=style.CLR_PRIMARY,
                                           text_color=style.CLR_WHITE,
                                           button_color=style.CLR_SECONDARY,
                                           font=style.FNT_BODY,
                                           dropdown_font=style.FNT_BODY,
                                           dynamic_resizing=False,
                                           hover=False)
        self.sportmenu.grid(row=3, column=0, columnspan=5, padx=50, pady=4, sticky='ew')

        # Gender input
        self.gender_vars[i] = ctk.StringVar(value="None")
        self.genderbutton = ctk.CTkSegmentedButton(master=tab,
                                              values=appsettings.GENDERS,
                                              variable=self.gender_vars[i],
                                              height=32,
                                              corner_radius=10,
                                              fg_color=style.CLR_PRIMARY,
                                              unselected_color=style.CLR_PRIMARY,
                                              unselected_hover_color=style.CLR_SECONDARY,
                                              selected_color=style.CLR_ACCENT_DARKENED,
                                              selected_hover_color=style.CLR_ACCENT_DARKENED)
        self.genderbutton.grid(row=4, column=0, columnspan=5, sticky='ew', pady=4, padx=(50,50))

        # height input
        self.height_vars[i] = ctk.StringVar()
        self.height_entry = ctk.CTkEntry(master=tab,
                                        placeholder_text="Insert height",
                                        textvariable= self.height_vars[i],
                                        height=32,
                                        border_width=2,
                                        corner_radius=10,
                                        border_color=style.CLR_PRIMARY,
                                        font=style.FNT_BODY)
        self.height_entry.grid(row=5, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

        # height unit
        height_unit = ctk.CTkLabel(master=tab,
                                   text="cm",
                                   height=32,
                                   anchor='w',
                                   font=style.FNT_BODY)
        height_unit.grid(row=5, column=4, padx=(0,50), ipadx=6, sticky='ew')

        if self.for_measurement:
            # Row Spacer
            spacer2 = ctk.CTkLabel(master=tab,
                                text="",
                                height=28)
            spacer2.grid(row=6, column=0, columnspan=5)

            # Weight input
            self.weight_vars[i] = ctk.StringVar()
            weight_entry = ctk.CTkEntry(master=tab,
                                            placeholder_text="Insert current weight",
                                            textvariable=self.weight_vars[i],
                                            height=32,
                                            border_width=2,
                                            corner_radius=10,
                                            border_color=style.CLR_ACCENT,
                                            font=style.FNT_BODY)
            weight_entry.grid(row=7, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

            # Weight unit
            weight_unit = ctk.CTkLabel(master=tab,
                                    text="kg",
                                    height=32,
                                    anchor='w',
                                    font=style.FNT_BODY)
            weight_unit.grid(row=7, column=4, padx=(0,50), ipadx=6, sticky='ew')

            # Pushheight input #Todo: make a validation command
            self.pushheight_vars[i] = ctk.StringVar()
            pushheight_entry = ctk.CTkEntry(master=tab,
                                            placeholder_text="Insert pushheight",
                                            textvariable=self.pushheight_vars[i],
                                            height=32,
                                            border_width=2,
                                            corner_radius=10,
                                            border_color=style.CLR_ACCENT,
                                            font=style.FNT_BODY)
            pushheight_entry.grid(row=8, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

            # Pushheight unit
            pushheight_unit = ctk.CTkLabel(master=tab,
                                    text="cm",
                                    height=32,
                                    anchor='w',
                                    font=style.FNT_BODY)
            pushheight_unit.grid(row=8, column=4, padx=(0,50), ipadx=6, sticky='ew')

    def configure_UI(self, userdetails, last_sessiondetails=None):
        #Todo: get model information and fill it in.
        for i in range(len(userdetails)):
            # Sport choice
            self.sportmenu.configure(state='disabled')
            self.sport_vars[i].set(userdetails[i]['sport'])
            
            # Gender choice
            self.genderbutton.configure(state='disabled')
            self.gender_vars[i].set(value=userdetails[i]['gender'])
            
            # Name
            self.name_entry.configure(state='disabled')
            self.name_vars[i].set(value=userdetails[i]['name'])
        
            # Height
            self.height_entry.configure(state='disabled')
            self.height_vars[i].set(value=userdetails[i]['height'])
            
            if last_sessiondetails is not None and last_sessiondetails[i] is not None:
                self.weight_vars[i].set(last_sessiondetails[i][0])
                self.pushheight_vars[i].set(last_sessiondetails[i][0])
            else:
                #Todo: findout why placeholder doesn't work
                self.weight_vars[i].set("Enter weight")
                self.pushheight_vars[i].set("Enter pushheight")
                print('No last value was found')
                #Todo: see if I want to create a default value here
