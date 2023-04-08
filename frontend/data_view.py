import tkinter as tk
import customtkinter as ctk

from PIL.Image import open as OpenImage

from settings import StyleElements as style
from settings import Paths as paths

from CTkMessagebox import CTkMessagebox

class DataView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=style.CLR_BACKGROUND)

        self.controller = controller
        
        if self.controller.options['n_users'] == 1:
            self.populate_UI_1user()
        else:
            self.populate_UI_2users()
        return
    
    def back(self):
        self.controller.stop_measurement_thread()
        self.controller.back()
        return
    
    def end(self):
        self.controller.stop_measurement()
        return
    
    def recalibrate(self):
        print('recalibrate')
        self.controller.update_calibration_factor()
        return
    
    def populate_navigation_bar(self):
        # ------------------
        #   IMAGES USED
        # ------------------
        IC_BACK = ctk.CTkImage(OpenImage(paths.PATH_IC_BACK), size=(40,40))
        IC_CALIBRATE = ctk.CTkImage(OpenImage(paths.PATH_IC_CALIBRATE), size=(64,51))
        IC_END = ctk.CTkImage(OpenImage(paths.PATH_IC_END), size=(40,51))

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
        
        btn_recalibrate = ctk.CTkButton(master=self,
                                 width=64,
                                 height=51,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.recalibrate,
                                 image=IC_CALIBRATE)
        btn_recalibrate.place(x=646, y=4)
        
        btn_end = ctk.CTkButton(master=self,
                                 width=40,
                                 height=51,
                                 text="",
                                 bg_color=style.CLR_BACKGROUND,
                                 fg_color=style.CLR_BACKGROUND,
                                 command=self.end,
                                 image=IC_END)
        btn_end.place(x=726, y=4)
        return
        
    def populate_UI_1user(self):
        # Navigation bar
        self.populate_navigation_bar()
        
        # Frame Top Left
        tl_frame = tk.Frame(self, width=368, height=130, bg= style.CLR_PRIMARY,
                            highlightthickness=1, highlightcolor=style.CLR_ONBACKGROUND)
        tl_frame.place(anchor='nw', x=24, y=64)

        time_txt = tk.Label(tl_frame, text="TIME", font= style.FNT_CAPTION,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height = 16)
        time_txt.place(anchor='ne', x=364, y=0, height=16)
        
        self.time_var = tk.DoubleVar()
        time_data = tk.Label(tl_frame, textvariable=self.time_var, font= style.FNT_DATA,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height=106)
        time_data.place(anchor='ne', x=364, y=20, height=106)

        # Frame Top Right
        tr_frame = tk.Frame(self, width=368, height=130, bg= style.CLR_PRIMARY,
                            highlightthickness=1, highlightcolor=style.CLR_ONBACKGROUND)
        tr_frame.place(anchor='nw', x=384+24, y=0+64)

        pf_txt = tk.Label(tr_frame, text="PEAK FORCE", font= style.FNT_CAPTION,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height = 16)
        pf_txt.place(anchor='ne', x=364, y=0, height=16)
        
        self.pf_var = tk.DoubleVar()
        pf_data = tk.Label(tr_frame, textvariable=self.pf_var, font= style.FNT_DATA,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height=106)
        pf_data.place(anchor='ne', x=364, y=20, height=106)

        # Frame Mid Right
        mr_frame = tk.Frame(self, width=368, height=130, bg= style.CLR_PRIMARY,
                            highlightthickness=1, highlightcolor= style.CLR_ONBACKGROUND)
        mr_frame.place(anchor='nw', x=384+24, y=138+64)

        watt_txt = tk.Label(mr_frame, text="POWER", font= style.FNT_CAPTION,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height = 16)
        watt_txt.place(anchor='ne', x=364, y=0, height=16)
        
        self.power_var = tk.DoubleVar()
        watt_data = tk.Label(mr_frame, textvariable=self.power_var, font= style.FNT_DATA,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height=106)
        watt_data.place(anchor='ne', x=364, y=20, height=106)
        

        # Frame Mid Left
        ml_frame = tk.Frame(self, width=368, height=130, bg= style.CLR_PRIMARY,
                            highlightthickness=1, highlightcolor= style.CLR_ONBACKGROUND)
        ml_frame.place(anchor='nw', x=0+24, y=138+64)

        mf_txt = tk.Label(ml_frame, text="MEAN FORCE", font= style.FNT_CAPTION,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height = 16)
        mf_txt.place(anchor='ne', x=364, y=0, height=16)
        
        self.mf_var = tk.DoubleVar()
        mf_data = tk.Label(ml_frame, textvariable=self.mf_var, font= style.FNT_DATA,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height=106)
        mf_data.place(anchor='ne', x=364, y=20, height=106)

        # Frame Bottom
        b_frame = tk.Frame(self, width=750, height= 138, bg=style.CLR_SECONDARY,
                                highlightthickness=1, highlightcolor= style.CLR_ONBACKGROUND)
        b_frame.place(anchor='nw', x=0+24 , y=276+64)

        mf_txt = tk.Label(b_frame, text="FORCE", font= style.FNT_CAPTION,
                            bg= style.CLR_PRIMARY, fg= style.CLR_ONBACKGROUND, height = 16)
        mf_txt.place(anchor='ne', x=746, y=0, height=16)
        return
           
    def populate_UI_2users(self):
        # Navigation bar
        self.populate_navigation_bar()
        
        # Frame Top Left
        clr_tl = style.CLR_GREY75
        tl_frame = tk.Frame(self, width=368, height=130, bg=clr_tl,
                            highlightthickness=0, highlightcolor=style.CLR_BLACK)
        tl_frame.place(anchor='nw', x=24, y=64)
       
        time_txt = tk.Label(tl_frame, text="TIME", font= style.FNT_CAPTION,
                            bg=clr_tl, fg= style.CLR_ONBACKGROUND, height = 16)
        time_txt.place(anchor='nw', x=4, y=0, height=16)
        
        self.time_var = tk.DoubleVar()
        time_data = tk.Label(tl_frame, textvariable=self.time_var, font= style.FNT_DATA,
                            bg=clr_tl, fg= style.CLR_ONBACKGROUND, height=106)
        time_data.place(anchor='nw', x=4, y=20, height=106)

        # Frame Top Right
        clr_tr = style.CLR_GREY75
        tr_frame = tk.Frame(self, width=368, height=130, bg=clr_tr,
                            highlightthickness=0, highlightcolor=style.CLR_BLACK)
        tr_frame.place(anchor='nw', x=384+24, y=0+64)

        velocity_txt = tk.Label(tr_frame, text="VELOCITY", font= style.FNT_CAPTION,
                            bg=clr_tr, fg= style.CLR_ONBACKGROUND, height = 16)
        velocity_txt.place(anchor='ne', x=364, y=0, height=16)
        
        self.velocity_var = tk.DoubleVar()
        velocity_data = tk.Label(tr_frame, textvariable=self.velocity_var, font= style.FNT_DATA,
                            bg=clr_tr, fg= style.CLR_ONBACKGROUND, height=106)
        velocity_data.place(anchor='ne', x=364, y=20, height=106)

        # Frame Mid Right
        clr_user2 = style.CLR_PRIMARY
        mr_frame = tk.Frame(self, width=368, height=130, bg=clr_user2,
                            highlightthickness=1, highlightcolor= style.CLR_ONBACKGROUND)
        mr_frame.place(anchor='nw', x=384+24, y=138+64)

        force2_txt = tk.Label(mr_frame, text="FORCE 2", font= style.FNT_CAPTION,
                            bg=clr_user2, fg= style.CLR_ONBACKGROUND, height = 16)
        force2_txt.place(anchor='ne', x=364, y=0, height=16)
        
        self.force2_var = tk.DoubleVar()
        force2_data = tk.Label(mr_frame, textvariable=self.force2_var, font= style.FNT_DATA,
                            bg=clr_user2, fg= style.CLR_ONBACKGROUND, height=106)
        force2_data.place(anchor='ne', x=364, y=20, height=106)

        # Frame Mid Left
        clr_user1 = style.CLR_SECONDARY
        ml_frame = tk.Frame(self, width=368, height=130, bg=clr_user1,
                            highlightthickness=1, highlightcolor= style.CLR_ONBACKGROUND)
        ml_frame.place(anchor='nw', x=0+24, y=138+64)

        force1_txt = tk.Label(ml_frame, text="FORCE 1", font= style.FNT_CAPTION,
                            bg=clr_user1, fg= style.CLR_ONBACKGROUND, height = 16)
        force1_txt.place(anchor='nw', x=4, y=0, height=16)
        
        self.force1_var = tk.DoubleVar()
        force1_data = tk.Label(ml_frame, textvariable=self.force1_var, font= style.FNT_DATA,
                            bg=clr_user1, fg= style.CLR_ONBACKGROUND, height=106)
        force1_data.place(anchor='nw', x=4, y=20, height=106)

        # Frame Bottom Left      
        bl_frame = tk.Frame(self, width=368, height=138, bg=clr_user1,
                            highlightthickness=1, highlightcolor=style.CLR_ONBACKGROUND)
        bl_frame.place(anchor='nw', x=0+24, y=276+64)

        pf1_txt = tk.Label(bl_frame, text="PEAKFORCE 1", font= style.FNT_CAPTION,
                            bg=clr_user1, fg= style.CLR_ONBACKGROUND, height = 16)
        pf1_txt.place(anchor='nw', x=4, y=0, height=16)
        
        self.pf1_var = tk.DoubleVar()
        pf1_data = tk.Label(bl_frame, textvariable=self.pf1_var, font= style.FNT_DATA,
                            bg=clr_user1, fg= style.CLR_ONBACKGROUND, height=106)
        pf1_data.place(anchor='nw', x=4, y=20, height=106)
        
        # Frame Bottom Right      
        br_frame = tk.Frame(self, width=368, height=138, bg=clr_user2,
                            highlightthickness=1, highlightcolor= style.CLR_ONBACKGROUND)
        br_frame.place(anchor='nw', x=384+24, y=276+64)

        pf2_txt = tk.Label(br_frame, text="PEAKFORCE 2", font= style.FNT_CAPTION,
                            bg=clr_user2, fg= style.CLR_ONBACKGROUND, height = 16)
        pf2_txt.place(anchor='ne', x=364, y=0, height=16)
        
        self.pf2_var = tk.DoubleVar()
        pf2_data = tk.Label(br_frame, textvariable=self.pf2_var, font= style.FNT_DATA,
                            bg=clr_user2, fg= style.CLR_ONBACKGROUND, height=106)
        pf2_data.place(anchor='ne', x=364, y=20, height=106)
        return

    def display_time(self, time):
        self.time_var.set(round(time,1))

    def display_data_1p(self, data):
        self.force = data[0]
        self.power_var.set(round(data[1], 0))
        self.mf_var.set(round(data[2], 0))
        self.pf_var.set(round(data[3], 0))

    def display_data_2p(self, data):
        self.force1_var.set(round(data[0], 0))
        self.force2_var.set(round(data[1], 0))
        self.velocity_var.set(round(data[2], 2))
        self.pf1_var.set(round(data[3], 0))
        self.pf2_var.set(round(data[4], 0))
        
    def display_msg(self):
        # Display messagebox
        ctk.set_appearance_mode('dark')
        CTkMessagebox(title="Data is being processed", 
                          message="Your data is being processed, and can be found in the user profiles once its done",
                          icon='check', option_1='OK')