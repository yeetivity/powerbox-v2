import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths
from settings import ApplicationSettings as appsettings

class UserView(tk.Frame):
    def __init__(self, parent, controller, pbs=None, results=None):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)
                
        #Todo: replace placeholders
        self.name = "John Doe"
        self.gender = "Male"
        self.height = "167.0 cm"
        self.sport = "Greco-Roman wrestling"
        
        self.peakforce = "42 N"
        self.meanforce = "42 N"
        self.fatigue = "42 %"
        
        self.populate_UI()
        return
    
    def back(self):
        print('back')
        return

    def edit(self):
        print('edit')
        return
   
    def item_selected(self, event):
        # get selected index
        selected_index = self.resultlist.curselection()
        # get item
        selected_item = self.resultlist.get(selected_index)
        
        # Todo: send to controller
        print('selected a result')
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
        
        name = ctk.CTkLabel(master=block1,
                                 text=self.name,
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
        
        gender = ctk.CTkLabel(master=block1,
                                 text=self.gender,
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
        
        height = ctk.CTkLabel(master=block1,
                                 text=self.height,
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
        
        sport = ctk.CTkLabel(master=block1,
                                 text=self.sport,
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
        
        pf = ctk.CTkLabel(master=block2,
                                 text=self.peakforce,
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
        
        mf = ctk.CTkLabel(master=block2,
                                 text=self.meanforce,
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
        
        fat = ctk.CTkLabel(master=block2,
                                 text=self.fatigue,
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
        block_title2 = ctk.CTkLabel(master=self,
                                    text="RESULTS",
                                    font=style.FNT_OVERLINE,
                                    fg_color=style.CLR_BACKGROUND,
                                    text_color=style.CLR_WHITE)
        block_title2.place(x=150, y=245+64, anchor='sw')

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
