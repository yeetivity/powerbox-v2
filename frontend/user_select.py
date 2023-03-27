import tkinter as tk
import customtkinter as ctk

from CTkMessagebox import CTkMessagebox

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths
from settings import ApplicationSettings as appsettings

class UserSelect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)
        
        self.controller = controller

        self.for_measurement = controller.options['for_measurement']
        # If we are selecting for a measurement, n_users applies, otherwise it is 1
        self.n_users = controller.options['n_users'] if self.for_measurement else 1
        
        self.userIDs = {}
        self.users = None
        
        self.populate_UI()

        self.request_userlist('placeholder')
        return
    
    def back(self):
        self.controller.back()
        return

    def finish(self):        
        selected_ids = [None, None]
        # Check if a user is selected
        try:
            selected_items = self.userlist.curselection()
            for i in range(len(selected_items)):
                selected_ids[i] = self.userIDs[self.userlist.get(selected_items[i])] 
        except:
            # No user selected, display error message and return
            self.listbox_info_txt.configure(text_color=style.CLR_RED,
                                        text="Please select the right number of users")
            return
        
        if self.for_measurement:
            # Check if we selected the right amount of users
            if self.n_users == 2 and selected_ids[1] == None:
                self.listbox_info_txt.configure(text_color=style.CLR_RED,
                                        text="Please select the right number of users")
                return
            
            self.controller.userIDs_to_models(selected_ids)
            
            # Go to session details screen
            self.controller.goto_usercreate()
            return
        else:
            self.controller.goto_userview(selected_ids[0])

    def newuser(self):
        if self.n_users == 2:
            msg = CTkMessagebox(title="Warning", 
                                message="You've selected dual athlete mode, please create the athletes in the homescreen before starting",
                                icon="warning",
                                option_1="Go Home",
                                option_2="Select athletes instead")
            if msg.get() == "Go Home":
                self.controller.home()
            return
        self.controller.options['creating'] = True
        self.controller.goto_usercreate()
        print('creating new user...')

    def request_userlist(self, choice):
        gender_filter = self.genderbutton_var.get() if self.genderbutton_var.get() != "None" else None
        sport_filter = self.sportmenu_var.get() if self.sportmenu_var.get() != "Choosing..." else None

        users = self.controller.get_users(filter1=gender_filter, filter2=sport_filter)

        self.update_userlist(users)
        return

    def update_userlist(self, users):
        # Clear current userlist
        self.userlist.delete(0, tk.END)

        if not users:
            # No users found
            self.listbox_info_txt.configure(text_color=style.CLR_GREY75,
                                         text="NO USERS FOUND")
            print('No users found')
            return

        # Users found
        self.listbox_info_txt.configure(text_color=style.CLR_BACKGROUND_ALT)

        # Sort users by last name
        self.users = sorted(users, key=lambda x: x[2])

        # Add usernames to listbox and userIDs to dictionary
        for user in self.users:
            fullname = f" {user[1]} {user[2]}"
            self.userlist.insert(tk.END, fullname)
            self.userIDs[fullname] = user[0]

        print('Users inserted into userlist')
        return

    def populate_UI(self):
        # ------------------
        #   IMAGES USED
        # ------------------
        IC_BACK = ctk.CTkImage(OpenImage(paths.PATH_IC_BACK), size=(40,40))
        IC_USESELECTED = ctk.CTkImage(OpenImage(paths.PATH_IC_USESELECTED), size=(84,51))
        IC_NEWUSER = ctk.CTkImage(OpenImage(paths.PATH_IC_NEWUSER), size=(60,51))

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

        if self.for_measurement:
            btn_newuser = ctk.CTkButton(master=self,
                                    width=60,
                                    height=51,
                                    text="",
                                    bg_color=style.CLR_BACKGROUND,
                                    fg_color=style.CLR_BACKGROUND,
                                    command=self.newuser,
                                    image=IC_NEWUSER)
            btn_newuser.place(x=622, y=4)

        btn_checkmark = ctk.CTkButton(master=self,
                                 width=84,
                                 height=51,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.finish,
                                 image=IC_USESELECTED)
        btn_checkmark.place(x=700, y=4)

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
        if self.n_users == 1:
            title_txt = "Find your athlete"
        else:
            title_txt = "Find your athletes"
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

        # filter_title
        filter_title = ctk.CTkLabel(master=mid_frame,
                                   text="FILTERS",
                                   font=style.FNT_OVERLINE,
                                   width=400,
                                   height=16,
                                   anchor='w',
                                   bg_color=style.CLR_BACKGROUND_ALT
                                  )
        filter_title.grid(row=2, column=0, columnspan=5, padx=50, sticky='ew')

        # Sport input
        self.sportmenu_var = ctk.StringVar(value="Choosing...")
        self.sportmenu = ctk.CTkOptionMenu(master=mid_frame,
                                           values=appsettings.SPORTS,
                                           command=self.request_userlist,
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
        self.genderbutton_var = ctk.StringVar(value="None")
        self.genderbutton = ctk.CTkSegmentedButton(master=mid_frame,
                                                   values=appsettings.GENDERS,
                                                   variable=self.genderbutton_var,
                                                   command=self.request_userlist,
                                                   height=32,
                                                   corner_radius=10,
                                                   fg_color=style.CLR_PRIMARY,
                                                   unselected_color=style.CLR_PRIMARY,
                                                   unselected_hover_color=style.CLR_SECONDARY,
                                                   selected_color=style.CLR_ACCENT_DARKENED,
                                                   selected_hover_color=style.CLR_ACCENT_DARKENED)
        self.genderbutton.grid(row=4, column=0, columnspan=5, sticky='ew', pady=4, padx=(50,50))
        
        # Row Spacer
        spacer = ctk.CTkLabel(master=mid_frame,
                              text="",
                              height=14)
        spacer.grid(row=5, column=0, columnspan=5)
        
        # Select athlete title
        athlete_title = ctk.CTkLabel(master=mid_frame,
                                   text="SELECT ATHLETE",
                                   font=style.FNT_OVERLINE,
                                   height=16,
                                   anchor='w',
                                   bg_color=style.CLR_BACKGROUND_ALT
                                  )
        athlete_title.grid(row=6, column=0, columnspan=2, padx=(50,0), sticky='ew')

        # No item selected_title
        self.listbox_info_txt = ctk.CTkLabel(master=mid_frame,
                                   text="NO ATHLETES FOUND",
                                   font=style.FNT_OVERLINE,
                                   height=16,
                                   anchor='w',
                                   bg_color=style.CLR_BACKGROUND_ALT,
                                   text_color=style.CLR_BACKGROUND_ALT)
        self.listbox_info_txt.grid(row=6, column=2, columnspan=3, sticky='ew')


        # Scrollbar listbox
        scrollbar = tk.Scrollbar(mid_frame, bg=style.CLR_BACKGROUND, width=20)
        scrollbar.grid(row=7, column=4, sticky='ns', padx=(0,50))

        # Listbox user names
        self.selected_item = tk.Variable()
        self.userlist = tk.Listbox(master=mid_frame,
                                   bg=style.CLR_GREY50,
                                   font=style.FNT_CAPTION,
                                   selectmode="single",
                                   yscrollcommand=scrollbar.set,
                                   fg=style.CLR_PRIMARY,
                                   highlightcolor=style.CLR_PRIMARY,
                                   highlightthickness=1,
                                   height=7,
                                   listvariable=self.selected_item)
        self.userlist.grid(row=7, column=0, columnspan=4, padx=(50,0), pady=4, sticky='ew')

        for i in range(5):
            mid_frame.grid_columnconfigure(i, weight=1)
        
        if self.n_users != 1:
            self.userlist.configure(selectmode='multiple')

        return   
