# PowerBox version 2

This is a multiclass application built using object-oriented programming principles. The application consists of frontend classes that generate the frontend using the customtkinter framework. "powerboxApp.py" is used as a controller, and handles the communication between the frontend and backend classes. 

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contact](#contact)

## Features
- Quick measurement: athletes get the data from three sensors without saving any data
- Normal measurement: athletes perform a measurements and save the data to their profiles
- Reviewing results: athletes can review old and saved results, which are compared to their current personal bests and last results

## Getting started
### Prerequisites
- You will need the following libraries:
    - contourpy (==1.0.7)
    - CTkMessagebox (==1.5)
    - customtkinter (==5.1.2)**
    - cycler (==0.11.0)
    - darkdetect (==0.8.0)
    - fonttools (==4.39.2)
    - fpdf (==1.7.2)**
    - future (==0.18.3)
    - iso8601 (==1.1.0)
    - kiwisolver (==1.4.4)
    - matplotlib (==3.7.1)
    - numpy (==1.24.2)
    - packaging (==23.0)
    - Pillow (==9.4.0)
    - PyMuPDF (==1.21.1)
    - pyparsing (==3.0.9)
    - pyserial (==3.5)
    - python-dateutil (==2.8.2)
    - PyYAML (==6.0)
    - scipy (==1.10.1)
    - six (==1.16.0)
    - tkPDFViewer (==0.1) **

    ** Depending on which version you use these packages might still contain bugs

### Installation
    1. Clone the repository
    2. Navigate to the project directory
    3. Install the required dependencies

### Usage
    1. Make sure you have a running microprocessor gathering data
        - This microprocessor has to be plugged into a USB port that supports Serial data transfer
    2. Run the application
        - python powerboxApp.py
    3. Interact with the application

### Disclaimer
The application is a bespoke application built for the PowerBox system, built by J.J. van Esch. 

# Architecture
- frontend: this folder holds the classes for the generating the using
- backend: this folder holds the classes for handling the backend operations, such as generating the pdf report, holding the session data, analysing data, gathering data, and generating emails. 
- pipico_code: this folder holds code that can run on the microprocessor
- powerboxApp.py: controller for managing interaction between the sections

# Contact
Feel free to contact me if you want to use this code or want to know more. 
