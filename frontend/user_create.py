import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths
from settings import ApplicationSettings as appsettings

class UserCreate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)
        
        ctk.set_appearance_mode('light')
    
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
        self.warnings = []
                
        self.populate_UI()
    
    def back(self):
        self.controller.back()
        print('back')
        return

    def finish(self):
        # Disable all warnings
        for i in self.warnings:
            i.grid_remove()
            
        # Empty the warnings list
        self.warnings = []
            
        if self.creating and self.validate_userdetails():           
            # Get user details (creating only works for 1 user)
            name, sport, gender, height = (e.get() for e in(
                self.name_vars[0], self.sport_vars[0], self.gender_vars[0], self.height_vars[0]
            ))

            # Send userdetails to database (returns userID)
            userID = self.controller.user_to_database((name, sport, gender, int(height)))

            # Send userdetails to model
            self.controller.userIDs_to_models((userID, None))

            if not self.for_measurement:
                self.controller.home()
                return
        elif self.creating and not self.validate_userdetails():
            return 
        
        # Get session details (could be for 2 users)
        sessiondetails = [None, None]  # Initialisation

        
        for i in range(self.n_users):
            if self.validate_sessiondetails(i):
                weight, pushheight = (e.get() for e in (self.weight_vars[i], self.pushheight_vars[i]))
                sessiondetails[i] = (float(weight), int(pushheight))
            elif i + 1 == self.n_users:
                # Only do this on the final loop
                return

        self.controller.session_details_to_model(sessiondetails)
        
        self.controller.goto_dataview()

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
        self.tab_view = ctk.CTkTabview(master=mid_frame,
                                  width=496,
                                  height=386,
                                  fg_color=style.CLR_BACKGROUND_ALT)
        self.tab_view.place(x=2, y=2)
        self.tab_view.grid_propagate(False)
        self.tab_view.add('User 1')
        self.fill_tabview(self.tab_view.tab('User 1'), 0)

        if self.for_measurement and self.n_users == 2:
            self.tab_view.add('User 2')
            self.fill_tabview(self.tab_view.tab('User 2'), 1)

        self.tab_view.set('User 1')
        
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
        frame_title.grid(row=0, column=0, columnspan=5, ipady=3)

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
        self.name_entry.grid(row=3, column=0, columnspan=5, padx=50, pady=(8, 4), sticky='ew')

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
        self.sportmenu.grid(row=5, column=0, columnspan=5, padx=50, pady=4, sticky='ew')

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
        self.genderbutton.grid(row=7, column=0, columnspan=5, sticky='ew', pady=4, padx=(50,50))

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
        self.height_entry.grid(row=9, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

        # height unit
        height_unit = ctk.CTkLabel(master=tab,
                                   text="cm",
                                   height=32,
                                   anchor='w',
                                   font=style.FNT_BODY)
        height_unit.grid(row=9, column=4, padx=(0,50), ipadx=6, sticky='ew')

        if self.for_measurement:
            # Row Spacer
            spacer2 = ctk.CTkLabel(master=tab,
                                text="",
                                height=28)
            spacer2.grid(row=10, column=0, columnspan=5)

            # Weight input
            self.weight_vars[i] = ctk.StringVar()
            self.weight_entry = ctk.CTkEntry(master=tab,
                                            placeholder_text="Insert current weight",
                                            textvariable=self.weight_vars[i],
                                            height=32,
                                            border_width=2,
                                            corner_radius=10,
                                            border_color=style.CLR_ACCENT,
                                            font=style.FNT_BODY)
            self.weight_entry.grid(row=12, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

            # Weight unit
            weight_unit = ctk.CTkLabel(master=tab,
                                    text="kg",
                                    height=32,
                                    anchor='w',
                                    font=style.FNT_BODY)
            weight_unit.grid(row=12, column=4, padx=(0,50), ipadx=6, sticky='ew')

            # Pushheight input #Todo: make a validation command
            self.pushheight_vars[i] = ctk.StringVar()
            self.pushheight_entry = ctk.CTkEntry(master=tab,
                                            placeholder_text="Insert pushheight",
                                            textvariable=self.pushheight_vars[i],
                                            height=32,
                                            border_width=2,
                                            corner_radius=10,
                                            border_color=style.CLR_ACCENT,
                                            font=style.FNT_BODY)
            self.pushheight_entry.grid(row=14, column=0, columnspan=4, padx=(50,4), pady=4, sticky='ew')    

            # Pushheight unit
            pushheight_unit = ctk.CTkLabel(master=tab,
                                    text="cm",
                                    height=32,
                                    anchor='w',
                                    font=style.FNT_BODY)
            pushheight_unit.grid(row=14, column=4, padx=(0,50), ipadx=6, sticky='ew')

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
                self.weight_vars[i].set("Enter weight")
                self.pushheight_vars[i].set("Enter pushheight")
                print('No last value was found')
                #Todo: see if I want to create a default value here

    def validate_userdetails(self):
        no_warnings = True
        
        if self.name_vars[0].get() == "" or len(self.name_vars[0].get().split()) == 1 or self.name_vars[0].get() == "Insert your name":
            name_warning = ctk.CTkLabel(master=self.tab_view.tab('User 1'),
                                        text="Name has to be -FirstName LastName-",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            name_warning.grid(row=2, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(name_warning)
            self.name_entry.grid_configure(pady=(0,2))
            no_warnings = False
        
        if self.sport_vars[0].get() == "Choosing...":
            sport_warning = ctk.CTkLabel(master=self.tab_view.tab('User 1'),
                                        text="Please choose a sport",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            sport_warning.grid(row=4, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(sport_warning)
            self.sportmenu.grid_configure(pady=(0,2))
            no_warnings = False
            
        if self.gender_vars[0].get() == "None":
            gender_warning = ctk.CTkLabel(master=self.tab_view.tab('User 1'),
                                        text="Please choose a gender",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            gender_warning.grid(row=6, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(gender_warning)
            self.genderbutton.grid_configure(pady=(0,2))
            no_warnings = False
        
        if (self.height_vars[0].get() == "" or not self.height_vars[0].get().isdigit()):
            height_warning = ctk.CTkLabel(master=self.tab_view.tab('User 1'),
                                        text="Please input the height as an integer",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            height_warning.grid(row=8, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(height_warning)
            self.height_entry.grid_configure(pady=(0,2))
            no_warnings = False
        elif (int(self.height_vars[0].get()) < 120 or int(self.height_vars[0].get()) > 240):
            height_warning = ctk.CTkLabel(master=self.tab_view.tab('User 1'),
                                        text="Please input a realistic height",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            height_warning.grid(row=8, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(height_warning)
            self.height_entry.grid_configure(pady=(0,2))
            no_warnings = False
        
        return no_warnings
    
    def validate_sessiondetails(self, i):
        no_warnings = True
        tabs = ('User 1', 'User 2')
        if (self.weight_vars[i].get() == "" or not self.is_float(self.weight_vars[i].get())):
            weight_warning = ctk.CTkLabel(master=self.tab_view.tab(tabs[i]),
                                        text="Please input the height as an integer",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            weight_warning.grid(row=11, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(weight_warning)
            self.weight_entry.grid_configure(pady=(0,2))
            no_warnings = False
        elif (float(self.weight_vars[i].get()) < 30 or float(self.weight_vars[i].get()) > 250):
            weight_warning = ctk.CTkLabel(master=self.tab_view.tab(tabs[i]),
                                        text="Please input a realistic weight",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            weight_warning.grid(row=11, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(weight_warning)
            self.weight_entry.grid_configure(pady=(0,2))
            no_warnings = False

        if (self.pushheight_vars[i].get() == "" or not self.is_float(self.pushheight_vars[i].get())):
            pushheight_warning = ctk.CTkLabel(master=self.tab_view.tab(tabs[i]),
                                        text="Please input the height in the form xx.xx",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            pushheight_warning.grid(row=13, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(pushheight_warning)
            self.pushheight_entry.grid_configure(pady=(0,2))
            no_warnings = False
        elif (float(self.pushheight_vars[i].get()) < 0 or float(self.pushheight_vars[i].get()) > 50):
            pushheight_warning = ctk.CTkLabel(master=self.tab_view.tab(tabs[i]),
                                        text="Please input a realistic pushheight",
                                        font=style.FNT_OVERLINE,
                                        text_color=style.CLR_RED,
                                        height=6)
            pushheight_warning.grid(row=13, column=0, columnspan=5, padx=50, pady=0, sticky='ew')
            self.warnings.append(pushheight_warning)
            self.pushheight_entry.grid_configure(pady=(0,2))
            no_warnings = False
            
        return no_warnings
    
    def is_float(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False