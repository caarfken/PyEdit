from tkinter import *
import os
import sys
from tkinter import messagebox
import utils
import subprocess


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname("./")
    return os.path.join(datadir, filename)

def open_file(event=None):
        # open file
        global contents
        global file
        contents, file = utils.open_file()
        end_tuple = os.path.splitext(file.name)
        noLang = True
        titleLang = ""
        global command
        command = False
        # check programming language
        for sect in langs:
            lang, newext, newcommand = sect.split(",")
            if newext == end_tuple[1]:
                command = newcommand
                titleLang = lang
                noLang = False
                break
            else:
                noLang = True
        # set title
        if noLang:
            root.title(file.name + " - PyEdit")
        else:
            root.title(file.name + " - " + titleLang + " - PyEdit")
        t.insert('1.0', contents)
def save_file(event=None):
    utils.save_file(t, file)
def save_file_as(event=None):
    utils.save_file_as(t.get("1.0", END))
def run_file(event=None):
    messagebox.showinfo("Output", subprocess.check_output([command.strip(), file.name]))
def themeChanger(theme):
    activeTheme = open(find_data_file("activeTheme.conf"), "w")
    activeTheme.write(theme)
    activeTheme.close()
    messagebox.showinfo("Theme Change", "Theme succesfully changed. This will not take effect until you restart the application")
def darkTheme(event=None):
    themeChanger(find_data_file("darkTheme.csv"))
def lightTheme(event=None):
    themeChanger(find_data_file("lightTheme.csv"))
def customTheme(event=None):
    file = utils.get_open_dialog()
    themeChanger(file.name)

def main(event=None):
    # Initialize variables
    name = ""
    ctrl_pressed = False
    file_opened = False
    # Get theme
    themeName = open(find_data_file("activeTheme.conf"))
    global theme
    theme = open(themeName.read())
    menuColor, edColor, textColor = theme.read().split(",")
    # Setup extensions
    langsFile = open(find_data_file("langs.csv"))
    global langs
    langs = langsFile.readlines()
    # Start Tkinter
    global root
    root = Tk()
    global t
    t = Text(root, background=edColor, foreground=textColor)
    t.pack(expand=True, fill=BOTH)
    # Keybindings
    t.bind("<Control-s>", save_file)
    t.bind("<Control-S>", save_file_as)
    t.bind("<Control-o>", open_file)
    t.bind("<Control-r>", run_file)
    t.bind("<Control-n>", main)
    # Menubar
    menubar = Menu(root, background=menuColor, foreground=textColor, activebackground=edColor, activeforeground="white")
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=main)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Save as...", command=save_file_as)
    filemenu.add_command(label="Run file", command=run_file)
    filemenu.add_command(label="Quit", command=sys.exit)
    menubar.add_cascade(label="File", menu=filemenu)
    thememenu = Menu(menubar, tearoff=0)
    thememenu.add_command(label="Dark Theme", command=darkTheme)
    thememenu.add_command(label="Light Theme", command=lightTheme)
    thememenu.add_command(label="Custom Theme", command=customTheme)
    menubar.add_cascade(label="Themes", menu=thememenu)
    
    root.config(menu=menubar)
    # Set title
    root.title("PyEdit")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Shut everything down
        file.close()
        langsFile.close()
        theme.close()
        themeName.close()
        sys.exit()
        
if __name__ == "__main__":
    main()
