import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from CTkMessagebox import CTkMessagebox

from settings import StyleElements as style
from settings import Paths as paths
from settings import ApplicationSettings as appsettings

class UserView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)
        
        ctk.set_appearance_mode('light')
        
        self.resultIDs = {}
        self.controller = controller
        
        self.populate_UI()
        return
    
    def back(self):
        self.controller.back()
        return

    def edit(self):
        print('connecting sensor feature not functional yet')
        msg = CTkMessagebox(title="Feature not found", 
                            message="This functionality is still under construction",
                            icon='warning',
                            option_1='OK')
        return
   
    def item_selected(self, event):
        # Get selected index
        selected_index = self.resultlist.curselection()
        # Get corresponding resultID
        resultID = self.resultIDs[self.resultlist.get(selected_index)]
        # Open selected result
        self.controller.goto_result(resultID)
        return

    def update_resultlist(self, results):
        # Clear current userlist
        self.resultlist.delete(0, tk.END)

        # Add results to listbox
        for result in results:
            info = f" {result[4]}"
            self.resultlist.insert(tk.END, info)
            self.resultIDs[info] = result[0]

        print('Users inserted into userlist')
        return

    def populate_UI(self):
        # ------------------
        #   IMAGES USED
        # ------------------
        IC_BACK = ctk.CTkImage(OpenImage(paths.PATH_IC_BACK), size=(40,40))
        IC_EDITUSER = ctk.CTkImage(OpenImage(paths.PATH_IC_EDITUSER), size=(60,51))

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

        btn_checkmark = ctk.CTkButton(master=self,
                                 width=60,
                                 height=51,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.edit,
                                 image=IC_EDITUSER)
        btn_checkmark.place(x=700, y=4)

        # ----------------------
        #   ATHLETE INFORMATION
        # ----------------------
        block_title1 = ctk.CTkLabel(master=self,
                                    text="ATHLETE INFORMATION",
                                    font=style.FNT_OVERLINE,
                                    fg_color=style.CLR_BACKGROUND,
                                    text_color=style.CLR_WHITE)
        block_title1.place(x=150, y=50, anchor='sw')
        
        block1 = ctk.CTkFrame(master=self,
                              width=500,
                              height=115,
                              fg_color=style.CLR_PRIMARY)
        block1.place(x=150, y=50, anchor='nw')
        block1.grid_propagate(False)
               
        name_desc = ctk.CTkLabel(master=block1,
                                 text="Name: ",
                                 font=style.FNT_CAPTION,
                                 text_color=style.CLR_GREY25,
                                 fg_color=style.CLR_PRIMARY,
                                 anchor='w')
        name_desc.grid(row=0, column=0, padx=(16,0), pady=(2,0), sticky='ew')
        
        self.name_var = ctk.StringVar()
        name = ctk.CTkLabel(master=block1,
                                 textvariable=self.name_var,
                                 font=style.FNT_BODY,
                                 anchor='w',
                                 fg_color=style.CLR_PRIMARY,
                                 text_color=style.CLR_WHITE)
        name.grid(row=0, column=1, padx=(0,16), pady=(2,0), sticky='ew')
        
        gender_desc = ctk.CTkLabel(master=block1,
                                 text="Gender: ",
                                 font=style.FNT_CAPTION,
                                 fg_color=style.CLR_PRIMARY,
                                 text_color=style.CLR_GREY25,
                                 anchor='w')
        gender_desc.grid(row=1, column=0, padx=(16,0), sticky='ew')
        
        self.gender_var = ctk.StringVar()
        gender = ctk.CTkLabel(master=block1,
                                 textvariable=self.gender_var,
                                 font=style.FNT_BODY,
                                 anchor='w',
                                 fg_color=style.CLR_PRIMARY,
                                 text_color=style.CLR_WHITE)
        gender.grid(row=1, column=1, padx=(0,16), sticky='ew')
        
        height_desc = ctk.CTkLabel(master=block1,
                                 text="Height: ",
                                 font=style.FNT_CAPTION,
                                 fg_color=style.CLR_PRIMARY,
                                 text_color=style.CLR_GREY25,
                                 anchor='w')
        height_desc.grid(row=2, column=0, padx=(16,0), sticky='ew')
        
        self.height_var = ctk.StringVar()
        height = ctk.CTkLabel(master=block1,
                                 textvariable=self.height_var,
                                 font=style.FNT_BODY,
                                 anchor='w',
                                 fg_color=style.CLR_PRIMARY,
                                 text_color=style.CLR_WHITE)
        height.grid(row=2, column=1, padx=(0,16), sticky='ew')
        
        sport_desc = ctk.CTkLabel(master=block1,
                                 text="Sport: ",
                                 font=style.FNT_CAPTION,
                                 fg_color=style.CLR_PRIMARY,
                                 text_color=style.CLR_GREY25,
                                 anchor='w')
        sport_desc.grid(row=3, column=0, padx=(16,0), sticky='ew')
        
        self.sport_var = ctk.StringVar()
        sport = ctk.CTkLabel(master=block1,
                                 textvariable=self.sport_var,
                                 font=style.FNT_BODY,
                                 anchor='w',
                                 fg_color=style.CLR_PRIMARY,
                                 text_color=style.CLR_WHITE)
        sport.grid(row=3, column=1, padx=(0,16), sticky='ew')
        
        block1.grid_columnconfigure(0, weight=1)
        block1.grid_columnconfigure(1, weight=4)
        
        # ----------------------
        #   PB INFORMATION
        # ----------------------
        block_title2 = ctk.CTkLabel(master=self,
                                    text="PERSONAL BESTS",
                                    font=style.FNT_OVERLINE,
                                    fg_color=style.CLR_BACKGROUND,
                                    text_color=style.CLR_WHITE)
        block_title2.place(x=150, y=165+32, anchor='sw')
        
        block2 = ctk.CTkFrame(master=self,
                              width=500,
                              height=80,
                              fg_color=style.CLR_ACCENT_DARKENED)
        block2.place(x=150, y=165+32, anchor='nw')
        block2.grid_propagate(False)
        
        pf_desc = ctk.CTkLabel(master=block2,
                                 text="Peak Force:",
                                 font=style.FNT_H6,
                                 text_color=style.CLR_PRIMARY,
                                 fg_color=style.CLR_ACCENT_DARKENED)
        pf_desc.grid(row=0, column=0, padx=(16,0), pady=(2,0), sticky='ew')
        
        self.pf_var = ctk.StringVar()
        pf = ctk.CTkLabel(master=block2,
                                 textvariable=self.pf_var,
                                 font=style.FNT_H5,
                                 fg_color=style.CLR_ACCENT_DARKENED,
                                 text_color=style.CLR_WHITE)
        pf.grid(row=1, column=0, padx=(16,0), pady=(2,0), sticky='ew')
        
        mf_desc = ctk.CTkLabel(master=block2,
                                 text="Mean Force:",
                                 font=style.FNT_H6,
                                 text_color=style.CLR_PRIMARY,
                                 fg_color=style.CLR_ACCENT_DARKENED)
        mf_desc.grid(row=0, column=1, padx=(4,0), pady=(2,0), sticky='ew')
        
        self.mf_var = ctk.StringVar()
        mf = ctk.CTkLabel(master=block2,
                                 textvariable=self.mf_var,
                                 font=style.FNT_H5,
                                 fg_color=style.CLR_ACCENT_DARKENED,
                                 text_color=style.CLR_WHITE)
        mf.grid(row=1, column=1, padx=(4,0), pady=(2,0), sticky='ew')
        
        fat_desc = ctk.CTkLabel(master=block2,
                                 text="Fatigue:",
                                 font=style.FNT_H6,
                                 text_color=style.CLR_PRIMARY,
                                 fg_color=style.CLR_ACCENT_DARKENED)
        fat_desc.grid(row=0, column=2, padx=(4,16), pady=(2,0), sticky='ew')
        
        self.fat_var = ctk.StringVar()
        fat = ctk.CTkLabel(master=block2,
                                 textvariable=self.fat_var,
                                 font=style.FNT_H5,
                                 fg_color=style.CLR_ACCENT_DARKENED,
                                 text_color=style.CLR_WHITE)
        fat.grid(row=1, column=2, padx=(4,16), pady=(2,0), sticky='ew')
        
        block2.grid_columnconfigure(0, weight=1)
        block2.grid_columnconfigure(1, weight=1)
        block2.grid_columnconfigure(2, weight=1)
        
        # ----------------------
        #   RESULTS
        # ----------------------
        block_title3 = ctk.CTkLabel(master=self,
                                    text="RESULTS",
                                    font=style.FNT_OVERLINE,
                                    fg_color=style.CLR_BACKGROUND,
                                    text_color=style.CLR_WHITE)
        block_title3.place(x=150, y=245+64, anchor='sw')

        # No item selected_title
        self.listbox_info_txt = ctk.CTkLabel(master=self,
                                   text="NO RESULTS FOUND",
                                   font=style.FNT_OVERLINE,
                                   fg_color=style.CLR_BACKGROUND,
                                   text_color=style.CLR_BACKGROUND)
        self.listbox_info_txt.place(x=250, y=245+64, anchor='sw')

        self.selected_item = tk.Variable()
        scrollbar = tk.Scrollbar(self, bg=style.CLR_BACKGROUND, width=20)
        scrollbar.place(x=654, y=245+64, height=142, anchor='nw')

        self.resultlist = tk.Listbox(self, bg= style.CLR_GREY50, font=style.FNT_BODY, height=15, 
                                selectmode='single', yscrollcommand= scrollbar.set,
                                fg=style.CLR_BLACK, listvariable=self.selected_item)
        self.resultlist.place(x=150, y=245+64, width=500, height=142, anchor='nw')
        self.resultlist.bind('<<ListboxSelect>>', self.item_selected)
        scrollbar.config(command = self.resultlist.yview)
        
        return   

    def display_user(self, userInfo):
        self.name_var.set(userInfo[0][1] + " " + userInfo[0][2])
        self.sport_var.set(userInfo[0][3])
        self.gender_var.set(userInfo[0][4])
        self.height_var.set(str(userInfo[0][5]))
        
        if len(userInfo[2]) == 0:
            # No results, so no personal bests either
            self.pf_var.set(" - ")
            self.mf_var.set(" - ")
            self.fat_var.set(" - ")
            self.listbox_info_txt.configure(text_color=style.CLR_RED)
        else:
            self.pf_var.set(str(round(userInfo[1][1], 2)) + " kg")
            self.mf_var.set(str(round(userInfo[1][2], 2)) + " kg")
            self.fat_var.set(str(round(userInfo[1][9], 2)) + " %")
            self.update_resultlist(userInfo[2])
        
         