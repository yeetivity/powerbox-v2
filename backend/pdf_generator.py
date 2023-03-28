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
        self.peakforce = str(round(model.analyseddata['peakforce'], 2)) + ' N'
        self.meanpower = str(round(model.analyseddata['power_avg'], 2)) + ' W'
        self.impulse = str(round(model.analyseddata['best_rfd'], 2)) + ' N/s'       

        # Personal bests comparison
        self.pb_pfrc = str(round(model.compareddata['peakforce'][1], 1)) + ' %'
        self.pb_apwr = str(round(model.compareddata['power_avg'][1], 1)) + ' %'
        self.pb_impu = str(round(model.compareddata['best_rfd'][1], 1)) + ' %'
        
        # Last result comparison
        self.rfd_pfrc = str(round(model.compareddata['peakforce'][0], 1)) + ' %'
        self.rfd_apwr = str(round(model.compareddata['power_avg'][0], 1)) + ' %'
        self.rfd_impu = str(round(model.compareddata['best_rfd'][0], 1)) + ' %'

        # Data
        self.forcedata = model.rawdata['force']
        self.powerdata = model.rawdata['power']
        self.timestamps = model.rawdata['time']

        # Generate empty pdf
        self.pdf = PDF()
        self.pdf.add_page()

        # Add custom font
        self.pdf.add_font('Ubuntu-R', '', '/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', uni=True)
        self.pdf.add_font('Ubuntu-B', '', '/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', uni=True)

        # Define style
        self.pdf.set_font('Ubuntu-R', '', 16)
        
        self.generate_titlebox()
        self.generate_graph()
        self.generate_analysis()

        # Output pdf
        self.pdf.output(Paths.PATH_REPORT, 'F')
        return


    def generate_titlebox(self):
        #place cells
        self.pdf.set_fill_color(r=249, g=218, b=96) #yellow
        self.pdf.set_draw_color(r=249, g=218, b=96)
        self.pdf.set_xy(x=10, y=22)

        #topmargin
        self.pdf.cell(w=self.pw, h=2, border=1, ln=1, fill=True)
        
        #first row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True) #sidemargin
        self.pdf.cell(w=23, h=7, txt="Name:", border=1, align='L', ln=0, fill=True) #name:
        self.pdf.cell(w=40, h=7, txt=self.modelname, border=1, align='L', ln=0, fill=True) #modelname
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True) #space
        self.pdf.cell(w=38, h=7, txt="Date:", border=1, align='L', ln=0, fill=True) #date:
        self.pdf.cell(w=52, h=7, txt=self.modeldate, border=1, align='L', ln=0, fill=True) #modeldate
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True) #endspace

        #second row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True) #sidemargin
        self.pdf.cell(w=23, h=7, txt="Gender:", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt=self.modelgender, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True) #space
        self.pdf.cell(w=38, h=7, txt="Program:", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt=self.modelprogram, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True) #endspace

        #third row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True) #sidemargin
        self.pdf.cell(w=23, h=7, txt="Height:", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt=self.modelheight, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True) #space
        self.pdf.cell(w=38, h=7, txt="", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt="", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True) #endspace

        #fourth row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True) #sidemargin
        self.pdf.cell(w=23, h=7, txt="Sport: ", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt=self.modelsport, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True) #space
        self.pdf.cell(w=38, h=7, txt="Weight :", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt=self.modelweight, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True) #endspace

        #fifth row
        self.pdf.cell(w=4, h=7, txt=" ", border=1, ln =0, align = 'C', fill=True) #sidemargin
        self.pdf.cell(w=23, h=7, txt="", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=40, h=7, txt="", border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=7, h=7, txt='', border=1, align='L', ln=0, fill=True) #space
        self.pdf.cell(w=38, h=7, txt="Pushheight: ", border=1, align='L', ln=0, fill=True) 
        self.pdf.cell(w=52, h=7, txt=self.modelpushheight, border=1, align='L', ln=0, fill=True)
        self.pdf.cell(w=26, h=7, txt=" ", border=1, align='L', ln=1, fill=True) #endspace

        #bottom margin
        self.pdf.cell(w=self.pw, h=3, border=1, fill=True, ln=1)
        return


    def generate_graph(self):
        #Todo: generate graph
        self.pdf.set_fill_color(r=217, g=217, b=217)
        self.pdf.set_xy(x=10, y=72)
        self.pdf.cell(w=self.pw, h=105, txt="", border=0, ln =1, align = 'C', fill=True)

        # Generating graph using matplotlib
        mm_to_inch = 0.0393701 #mm to inch conversion factor
        # Create figure
        fig1 = plt.figure(figsize=(75*mm_to_inch, 85*mm_to_inch))
        ax1 = fig1.add_subplot(1, 1, 1)
        
        # Create second figure
        fig2 = plt.figure(figsize=(75*mm_to_inch, 85*mm_to_inch))
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

        #Placing the graph [sizes in mm]
        self.pdf.image(Paths.PATH_FORCEPLOT, x=20, y=82, h=85, w=75)
        self.pdf.image(Paths.PATH_POWERPLOT, x=105, y=82, h=85, w=75)

        return


    def set_color(self, number, inverse=False):
        try:
            nr = number.split(" ")[0]
            nr = float(nr)
        except:
            self.pdf.set_text_color(255,255,255) #white
            return

        if inverse:
            nr = -nr #invert the number (in case lower is better)

        if nr > 100:
            self.pdf.set_text_color(2, 126, 15) #green
        elif nr < 100:
            self.pdf.set_text_color(203, 0, 0) #red
        else:
            self.pdf.set_text_color(255, 255, 255) #white

    def generate_analysis(self):
        self.pdf.set_xy(x=10, y=181)
        self.pdf.set_text_color(r=255, g=255, b=255)
        self.pdf.set_fill_color(r=11, g=41, b=79)
        self.pdf.set_draw_color(r=11, g=41, b=79)

        #top margin
        self.pdf.cell(w=self.pw, h=2, border=0, ln =1, align= 'C', fill=True)

        #first row
        self.pdf.set_font('Ubuntu-B', '', 14)
        self.pdf.cell(w=4, h=15, ln=0, fill=True, border=0) #sidemargin
        self.pdf.cell(w=62, h=15, ln=0, fill=True, border=0, align='L')
        self.pdf.cell(w=38, h=15, txt="RESULT", ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=38, h=15, txt="%PB", ln=0, fill=True, border=0, align='C')
        self.pdf.cell(w=48, h=15, txt="%LAST RESULT", ln=1, fill=True, border=0, align='C')
                
        #spacer
        self.pdf.cell(w=190, h=5, txt="", ln=1, fill=True, border=0, align='L')

        #second row
        self.pdf.set_font('Ubuntu-B', '', 14)
        self.pdf.cell(w=4, h=15, ln=0, fill=True, border=0) #sidemargin
        self.pdf.cell(w=62, h=15, txt="Peak force:", ln=0, fill=True, border=0, align='L')
        self.pdf.set_text_color(r=255, g=204, b=0)
        self.pdf.set_font('Ubuntu-R', '', 16)
        self.pdf.cell(w=38, h=15, txt=self.peakforce, ln=0, fill=True, border=0, align='C')
        self.set_color(self.pb_pfrc)
        self.pdf.cell(w=38, h=15, txt=self.pb_pfrc, ln=0, fill=True, border=0, align='C')
        self.set_color(self.rfd_pfrc)
        self.pdf.cell(w=48, h=15, txt=self.rfd_pfrc, ln=1, fill=True, border=0, align='C')
        self.pdf.set_text_color(r=255, g=255, b=255)

        #spacer
        self.pdf.cell(w=190, h=5, txt="", ln=1, fill=True, border=0, align='L')

        #third row
        self.pdf.set_font('Ubuntu-B', '', 14)
        self.pdf.cell(w=4, h=15, ln=0, fill=True, border=0) #sidemargin
        self.pdf.cell(w=62, h=15, txt="Power:", ln=0, fill=True, border=0, align='L')
        self.pdf.set_text_color(r=255, g=204, b=0)
        self.pdf.set_font('Ubuntu-R', '', 16)
        self.pdf.cell(w=38, h=15, txt=self.meanpower, ln=0, fill=True, border=0, align='C')
        self.set_color(self.pb_apwr)
        self.pdf.cell(w=38, h=15, txt=self.pb_apwr, ln=0, fill=True, border=0, align='C')
        self.set_color(self.rfd_apwr)
        self.pdf.cell(w=48, h=15, txt=self.pb_apwr, ln=1, fill=True, border=0, align='C')
        self.pdf.set_text_color(r=255, g=255, b=255)

        #spacer
        self.pdf.cell(w=190, h=5, txt="", ln=1, fill=True, border=0, align='L')

        #fourth row
        self.pdf.set_font('Ubuntu-B', '', 14)
        self.pdf.cell(w=4, h=15, ln=0, fill=True, border=0) #sidemargin
        self.pdf.cell(w=62, h=15, txt="Impulse index:", ln=0, fill=True, border=0, align='L')
        self.pdf.set_text_color(r=255, g=204, b=0)
        self.pdf.set_font('Ubuntu-R', '', 16)
        self.pdf.cell(w=38, h=15, txt=self.impulse, ln=0, fill=True, border=0, align='C')
        self.set_color(self.pb_impu)
        self.pdf.cell(w=38, h=15, txt=self.pb_impu, ln=0, fill=True, border=0, align='C')
        self.set_color(self.rfd_impu)
        self.pdf.cell(w=48, h=15, txt=self.rfd_impu, ln=1, fill=True, border=0, align='C')
        self.pdf.set_text_color(r=255, g=255, b=255)

        #spacer
        self.pdf.cell(w=190, h=2, txt="", ln=1, fill=True, border=0, align='L')
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
        self.image(Paths.PATH_LOGO_RF_SMALL, x=16, y=7, w=70)
        self.set_draw_color(255, 255, 255)
        #Add custom font
        self.add_font('Ubuntu-L', '', '/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf', uni=True)
        #Add headerbox
        self.set_font('Ubuntu-L', '', 7)
        self.cell(w=0, h=7, txt='', border=0, ln=1, align='C', fill=False)

    def footer(self):
        #Add custom font
        self.add_font('Ubuntu-L', '', '/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf', uni=True)
        #Add footerbox
        self.set_text_color(r=0, g=0, b=0)
        self.set_draw_color(255, 255, 255)
        self.set_y(-15)
        self.set_font('Ubuntu-L', '', 7)
        self.cell(w=0, h=7, txt='Working version of the report', border=0, ln=0, align='C', fill=False)