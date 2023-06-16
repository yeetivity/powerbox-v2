"""
Module responsible for creating a pdf report
=INPUT=
raw data, analysed data, and compared data
=OUTPUT=
saves report as pdf to /tmp

Author: Jitse van Esch
Date: 24-03-23
"""

from settings import Paths
from settings import StyleElements as s
from fpdf import FPDF

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import random

class PDFGenerator():
    def __init__(self):
        pass
    
    def create_pdf(self, model):
        """
        Transforms a model into a pdf
        =NOTE=
        Create training program feature
        """
        # Geometry
        m = 10 #margin
        self.pw = 210 - 2*m #pagewidth
        
        self.modelname = model.userdetails['name']
        self.modelgender = model.userdetails['gender']
        self.modelheight = str(model.userdetails['height'])
        self.modelsport = model.userdetails['sport']
        self.modelprogram = "Free training"  # This is a temporary placeholder
        
        self.modelweight = str(model.sessiondetails['weight'])
        self.modelpushheight = str(model.sessiondetails['pushheight'])
        self.modeldate = model.sessiondetails['date']
        
        # Results #todo: put fatigue in the graphing
        self.peakforce = str(round(model.analyseddata['peakforce'], 2)) + ' kg'
        self.meanpower = str(round(model.analyseddata['power_avg'], 2)) + ' W'
        self.fatigue = str(round(model.analyseddata['fatigability'], 2)) + ' %'       

        # Personal bests comparison
        self.pb_pfrc = 'PB: ' + str(round(model.compareddata['peakforce'][1], 1)) + ' %'
        self.pb_apwr = 'PB: ' + str(round(model.compareddata['power_avg'][1], 1)) + ' %'
        self.pb_fatigue = 'PB: ' + str(round(model.compareddata['fatigability'][1], 1)) + ' %'
        
        # Last result comparison
        self.lr_pfrc = 'LR: ' + str(round(model.compareddata['peakforce'][0], 1)) + ' %'
        self.lr_apwr = 'LR: ' + str(round(model.compareddata['power_avg'][0], 1)) + ' %'
        self.lr_fatigue = 'LR: ' + str(round(model.compareddata['fatigability'][0], 1)) + ' %'

        # Data
        self.forcedata = model.rawdata['force']
        self.powerdata = model.rawdata['power']
        self.timestamps = model.rawdata['time']

        # Generate empty pdf
        self.pdf = PDF()
        self.pdf.add_page()

        # Add custom font
        self.pdf.add_font('Ubuntu-R', '', '/home/powerbox/.fonts/ubuntu/Ubuntu-R.ttf', uni=True)
        self.pdf.add_font('Ubuntu-B', '', '/home/powerbox/.fonts/ubuntu/Ubuntu-B.ttf', uni=True)

        # Define style
        self.pdf.set_font('Ubuntu-R', '', 16)
        
        self.generate_titlebox()
        self.generate_analysis()
        self.generate_graph()

        # Output pdf
        self.pdf.output(Paths.PATH_REPORT, 'F')
        return

    def generate_titlebox(self):
        # Generate background box
        self.pdf.set_fill_color(r=249, g=218, b=96)  # yellow
        self.pdf.set_draw_color(r=249, g=218, b=96)
        self.pdf.set_xy(x=10, y=22)

        # Topmargin
        self.pdf.cell(w=self.pw, h=2, border=1, ln=1, fill=True)
        
        # First row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True)  # sidemargin
        self.pdf.cell(w=23, h=7, txt="Name:", border=1, align='L', ln=0, fill=True)  # name:
        self.pdf.cell(w=40, h=7, txt=self.modelname, border=1, align='L', ln=0, fill=True)  # modelname
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True)  # space
        self.pdf.cell(w=38, h=7, txt="Date:", border=1, align='L', ln=0, fill=True)  # date:
        self.pdf.cell(w=52, h=7, txt=self.modeldate, border=1, align='L', ln=0, fill=True)  # modeldate
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True)  # endspace

        # Second row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True)  # sidemargin
        self.pdf.cell(w=23, h=7, txt="Gender:", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt=self.modelgender, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True)  # space
        self.pdf.cell(w=38, h=7, txt="Program:", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt=self.modelprogram, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True)  # endspace

        # Third row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True)  # sidemargin
        self.pdf.cell(w=23, h=7, txt="Height:", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt=self.modelheight, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True)  # space
        self.pdf.cell(w=38, h=7, txt="", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt="", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True)  # endspace

        # Fourth row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True)  # sidemargin
        self.pdf.cell(w=23, h=7, txt="Sport: ", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt=self.modelsport, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True)  # space
        self.pdf.cell(w=38, h=7, txt="Weight :", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt=self.modelweight, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True)  # endspace

        # Fifth row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True)  # sidemargin
        self.pdf.cell(w=23, h=7, txt="", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt="", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True)  # space
        self.pdf.cell(w=38, h=7, txt="Pushheight: ", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt=self.modelpushheight, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True)  # endspace

        #bottom margin
        self.pdf.cell(w=self.pw, h=3, border=1, fill=True, ln=1)
        return

    def generate_graph(self):
        # Generating graph using matplotlib
        mm_to_inch = 0.0393701 #mm to inch conversion factor
        # Create figure
        fig1 = plt.figure(figsize=(170*mm_to_inch, 80*mm_to_inch))
        ax1 = fig1.add_subplot(1, 1, 1)
        
        # Create second figure
        fig2 = plt.figure(figsize=(170*mm_to_inch, 80*mm_to_inch))
        ax2 = fig2.add_subplot(1, 1, 1)

        #plot data
        ax1.plot(self.timestamps, self.forcedata, 'g-', label="Force [N]")
        ax2.plot(self.timestamps, self.powerdata, 'b-', label="Power [W]" )
              
        ax1.set_title('Force')
        ax1.set_ylabel('Force [N]', color='g')
        ax2.set_title('Power')
        ax2.set_ylabel('Power [W]', color='b')
        ax1.set_xlabel('Time [s]')
        ax2.set_xlabel('Time [s]')
        fig1.savefig(Paths.PATH_FORCEPLOT, transparent=True, bbox_inches='tight')
        fig2.savefig(Paths.PATH_POWERPLOT, transparent=True, bbox_inches='tight')

        # Figure 1
        self.pdf.set_fill_color(r=217, g=217, b=217)
        self.pdf.set_xy(x=10, y=100)
        self.pdf.cell(w=self.pw, h=80, txt="", border=0, ln =1, align = 'C', fill=True)
        self.pdf.image(Paths.PATH_FORCEPLOT, x=20, y=100, h=80, w=170)

        # Figure 2
        self.pdf.set_fill_color(r=217, g=217, b=217)
        self.pdf.set_xy(x=10, y=184)
        self.pdf.cell(w=self.pw, h=80, txt="", border=0, ln =1, align = 'C', fill=True)
        self.pdf.image(Paths.PATH_POWERPLOT, x=20, y=184, h=80, w=170)

        return

    def set_color(self, number):
        try:
            nr = number.split(" ")[1]
            nr = float(nr)
        except:
            self.pdf.set_text_color(255,255,255)  # White
            return

        if nr > 100:
            self.pdf.set_text_color(2, 126, 15)  # Green
        elif nr < 100 and nr >= 80:
            self.pdf.set_text_color(255, 107, 0)  # Orange
        elif nr < 80:
            self.pdf.set_text_color(203, 0, 0)  # Red
        else:
            self.pdf.set_text_color(255, 255, 255) #white

    def generate_analysis(self):
        self.pdf.set_xy(x=10, y=66)
        self.pdf.set_text_color(r=255, g=204, b=0)
        self.pdf.set_fill_color(r=0, g=77, b=250)
        self.pdf.set_draw_color(r=0, g=77, b=250)

        # Top margin
        self.pdf.cell(w=self.pw, h=1, border=0, ln =1, align= 'C', fill=True)

        # First row
        self.pdf.set_font('Ubuntu-B', '', 12)
        self.pdf.cell(w=5, h=8, ln=0, fill=True, border=0)  # sidemargin
        self.pdf.cell(w=60, h=8, txt="PEAK FORCE", ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=60, h=8, txt="MEAN POWER", ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=60, h=8, txt="FATIGABILITY", ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=5, h=8, ln=1, fill=True, border=0)  # sidemargin

        # Second row
        self.pdf.set_text_color(r=245, g=245, b=245)
        self.pdf.set_font('Ubuntu-B', '', 14)
        self.pdf.cell(w=5, h=12, ln=0, fill=True, border=0)  # sidemargin
        self.pdf.cell(w=60, h=12, txt=self.peakforce, ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=60, h=12, txt=self.meanpower, ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=60, h=12, txt=self.fatigue, ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=5, h=12, ln=1, fill=True, border=0)  # sidemargin

        # Third row
        self.pdf.set_font('Ubuntu-R', '', 12)
        self.pdf.cell(w=5, h=8, ln=0, fill=True, border=0)  # sidemargin

        self.set_color(self.lr_pfrc)
        self.pdf.cell(w=30, h=8, txt=self.lr_pfrc, ln=0, fill=True, border=0, align='C')
        
        self.set_color(self.pb_pfrc)
        self.pdf.cell(w=30, h=8, txt=self.pb_pfrc, ln=0, fill=True, border=0, align='C')
        
        self.set_color(self.lr_apwr)
        self.pdf.cell(w=30, h=8, txt=self.lr_apwr, ln=0, fill=True, border=0, align='C')

        self.set_color(self.pb_apwr)
        self.pdf.cell(w=30, h=8, txt=self.pb_apwr, ln=0, fill=True, border=0, align='C')

        self.set_color(self.lr_fatigue)
        self.pdf.cell(w=30, h=8, txt=self.lr_fatigue, ln=0, fill=True, border=0, align='C')

        self.set_color(self.pb_fatigue)
        self.pdf.cell(w=30, h=8, txt=self.pb_fatigue, ln=0, fill=True, border=0, align='C')

        self.pdf.cell(w=5, h=8, ln=1, fill=True, border=0)  # sidemargin

        # Spacer
        self.pdf.cell(w=190, h=1, txt="", ln=1, fill=True, border=0, align='L')
        return

class PDF(FPDF):
    def __init__(self):
        """
        Custom class to overwrite header and footer methods
        """
        super().__init__()

    def header(self):
        #Add logos
        self.image(Paths.PATH_LOGO_PB_SMALL, x=122, y=7)
        self.image(Paths.PATH_LOGO_RF_SMALL, x=16, y=5, w=70)
        self.set_draw_color(255, 255, 255)
        #Add custom font
        self.add_font('Ubuntu-L', '', '/home/powerbox/.fonts/ubuntu/Ubuntu-L.ttf', uni=True)
        #Add headerbox
        self.set_font('Ubuntu-L', '', 7)
        self.cell(w=0, h=7, txt='', border=0, ln=1, align='C', fill=False)

    def footer(self):
        #Add custom font
        self.add_font('Ubuntu-L', '', '/home/powerbox/.fonts/ubuntu/Ubuntu-L.ttf', uni=True)
        #Add footerbox
        self.set_text_color(r=10, g=10, b=10)
        self.set_draw_color(255, 255, 255)
        self.set_y(-15)
        self.set_font('Ubuntu-L', '', 7)
        self.cell(w=0, h=7, txt='Report made by PowerBox v2.0    LR = Last Result, PB = Personal Best', border=0, ln=0, align='C', fill=False)