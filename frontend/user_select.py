import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths
from settings import ApplicationSettings as appsettings

class UserSelect(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)
        
        n_users = controller.options['n_users']
        
        self.populate_UI(n_users)
        return
    
    def back(self):
        print('back')
        return

    def finish(self):
        # check if a user is selected
        print('save')
        return

    def newuser(self):
        print('newuser')
        return

    def sportmenu_callback(self, choice):
        print(choice)
        return

    def genderbutton_callback(self, choice):
        print(choice)
        return

    def populate_UI(self, n_users):
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
        if n_users == 1:
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
        
        # Row Spacer
        spacer = ctk.CTkLabel(master=mid_frame,
                              text="",
                              height=14)
        spacer.grid(row=5, column=0, columnspan=5)
        
        # Select athlete title
        athlete_title = ctk.CTkLabel(master=mid_frame,
                                   text="SELECT ATHLETE",
                                   font=style.FNT_OVERLINE,
                                   width=400,
                                   height=16,
                                   anchor='w',
                                   bg_color=style.CLR_BACKGROUND_ALT
                                  )
        athlete_title.grid(row=6, column=0, columnspan=5, padx=50, sticky='ew')

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
        
        if n_users != 1:
            self.userlist.configure(selectmode='multiple')

        return   
