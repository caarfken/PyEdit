from io import TextIOWrapper
import os
import sys
from tkinter import END, filedialog



def get_save_as_dialog() -> TextIOWrapper:
    '''Opens a save as dialog, then returns the chosen file'''
    file = filedialog.asksaveasfilename()
    file = open(file, "w+")
    return file

def save_file_as(contents):
    '''Writes to chosen file'''
    file = get_save_as_dialog()
    file.seek(0)
    file.write(contents)
    file.close()

def get_open_dialog():
    file = filedialog.askopenfile(mode="r+")
    return file

def open_file():
    file = get_open_dialog()
    cont = file.read()
    return cont, file

def save_file(t, file):
    contents = t.get('1.0', END)
    file.seek(0)
    file.write(contents)
    file.close()

def find_data_file(filename):
    '''This finds a data file if PyEdit has been frozen with cx_Freeze'''
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname("./")
    return os.path.join(datadir, filename)