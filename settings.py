"""
This module contains all the settings that might change depending on the run environment

Author: Jitse van Esch
Date: 24-03-23
"""

class StyleElements():
    """ This class contains all colors and fonts for the application """
    # Colors
    CLR_PRIMARY = "#0B296D"
    CLR_SECONDARY = "#071c4b"
    CLR_ACCENT = "#FFCC00"
    CLR_ACCENT_DARKENED = "#D4AA00"

    CLR_BLACK = "#0A0A0A"
    CLR_WHITE = "#F0F0F0"

    CLR_BACKGROUND = "#2D2D2D"
    CLR_ONBACKGROUND = "#F0F0F0"
    CLR_BACKGROUND_ALT = "#B4B4B4"
    CLR_ONBACKGROUND_ALT = "#0A0A0A"

    CLR_GREY25 = "#B4B4B4"
    CLR_GREY50= "#8C8C8C"
    CLR_GREY75 = "#3C3C3C"
    
    CLR_GREEN = "#027E0F"
    CLR_RED = "#CB0000"
    CLR_ORANGE = "#FF6B00"

    # Fonts
    FNT_H1 = ("Ubuntu-L", 98)
    FNT_H2 = ("Ubuntu-L", 61)
    FNT_H3 = ("Ubuntu-R", 49)
    FNT_H4 = ("Ubuntu-R", 35)
    FNT_H5 = ("Ubuntu-R", 24)
    FNT_H6 = ("Ubuntu-R", 20)

    FNT_BUTTON = ("Ubuntu-B", 14)
    FNT_SUBTITLE = ("Ubuntu-B", 14)
    FNT_BODY = ("Ubuntu-M", 14)
    FNT_CAPTION = ("Ubuntu-L", 12)
    FNT_OVERLINE = ("Ubuntu-R", 10)
    FNT_OVERLINE_IT = ("Ubuntu-RI", 10)
    FNT_DATA = ("Ubuntu-M", 98)

class Paths():
    """ This class contains all paths for the application """

    # Save locations Todo: define all possible locations
    PATH_STORAGE = "./storage/"
    PATH_TEMP = "/tmp/"
    PATH_REPORT = PATH_TEMP + "report.pdf"
    PATH_FORCEPLOT = PATH_TEMP + "forceplot.png"
    PATH_POWERPLOT = PATH_TEMP + "powerplot.png"
    PATH_RAWDATA = PATH_STORAGE + "raw-data/"
    PATH_ANALYSEDDATA = PATH_STORAGE + "analysed-data/"
    PATH_COMPAREDDATA = PATH_TEMP + "comparisson.csv"
    PATH_DATABASE = PATH_STORAGE + "PowerBox.db"

    # Image locations
    PATH_IMAGE_FOLDER = "./frontend/images/"
    PATH_IC_BACK = PATH_IMAGE_FOLDER + "ic_back.png"
    PATH_IC_CONNECTSENSOR = PATH_IMAGE_FOLDER + "ic_connectsensor.png"
    PATH_IC_EXPORT = PATH_IMAGE_FOLDER + "ic_export.png"
    PATH_IC_FINDRESULTS = PATH_IMAGE_FOLDER + "ic_findresults.png"
    PATH_IC_FINDUSERS = PATH_IMAGE_FOLDER + "ic_finduserresults.png"
    PATH_IC_PRINT = PATH_IMAGE_FOLDER + "ic_print.png"
    PATH_IC_QUICKSTART = PATH_IMAGE_FOLDER + "ic_quickstart.png"
    PATH_IC_SAVE = PATH_IMAGE_FOLDER + "ic_save.png"
    PATH_IC_SETTINGS = PATH_IMAGE_FOLDER + "ic_settings.png"
    PATH_IC_START = PATH_IMAGE_FOLDER + "ic_start.png"
    PATH_IC_HOME = PATH_IMAGE_FOLDER + "ic_home.png"
    PATH_IC_END = PATH_IMAGE_FOLDER + "ic_end.png"
    PATH_IC_SINGLEUSER = PATH_IMAGE_FOLDER + "ic_singleathlete.png"
    PATH_IC_SINGLEUSER_GREY = PATH_IMAGE_FOLDER + "ic_singleathlete_greyed_out.png"
    PATH_IC_DOUBLEUSER = PATH_IMAGE_FOLDER + "ic_doubleathlete.png"
    PATH_IC_DOUBLEUSER_GREY = PATH_IMAGE_FOLDER + "ic_doubleathlete_greyed_out.png"
    PATH_IC_CALIBRATE = PATH_IMAGE_FOLDER + "ic_calibrate.png"
    PATH_IC_CHECKMARK = PATH_IMAGE_FOLDER + "ic_checkmark.png"
    PATH_IC_NEWUSER = PATH_IMAGE_FOLDER + "ic_newuser.png"
    PATH_IC_USESELECTED = PATH_IMAGE_FOLDER + "ic_useselected.png"
    PATH_IC_EDITUSER = PATH_IMAGE_FOLDER + "ic_edituser.png"
    PATH_IC_CREATEUSER = PATH_IMAGE_FOLDER + "ic_createuser.png"
    PATH_LOGO_PB_BIG = PATH_IMAGE_FOLDER + "Logo_Big.png"
    PATH_LOGO_PB_SMALL = PATH_IMAGE_FOLDER + "Logo_Small.png"
    PATH_LOGO_RF_SMALL = PATH_IMAGE_FOLDER + "rf_logo.png"

class ApplicationSettings():
    WINDOW_HEIGHT = 480  # pixels
    WINDOW_WIDTH = 800  # pixels

    SPORTS = ("Greco-Roman Wrestling", "Freestyle Wrestling", "Judo", "Rugby", "Other")
    GENDERS = ("Male", "Female")

    FREQUENCY = 10  # Hz
    SLEEP_TIME = 0.1 # s    1/FREQUENCY
    
    ALPHA_VELOCITY_FILTER = 0.1

    UPDATE_TIME_FREQUENCY = 2  # Hz
    UPDATE_VARS_FREQUENCY = 2  # Hz