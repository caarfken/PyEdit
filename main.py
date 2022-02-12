from tkinter import *
import os

import sys
from tkinter import messagebox
import utils
import subprocess
def open_file(event=None):
        global contents
        global file
        contents, file = utils.open_file()
        end_tuple = os.path.splitext(file.name)
        noLang = True
        titleLang = ""
        global command
        command = False
        for sect in langs:
            lang, newext, newcommand = sect.split(",")
            if newext == end_tuple[1]:
                command = newcommand
                titleLang = lang
                noLang = False
                break
            else:
                noLang = True
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

def main(event=None):
    # Initialize variables
    name = ""
    ctrl_pressed = False
    file_opened = False
    # Get theme
    global theme
    theme = open("theme.csv")
    menuColor, edColor = theme.read().split(",")
    # Setup extensions
    langsFile = open("langs.csv")
    global langs
    langs = langsFile.readlines()
    # Start Tkinter
    global root
    root = Tk()
    global t
    t = Text(root, background=edColor, foreground="white")
    t.pack(expand=True, fill=BOTH)
    # Keybindings
    t.bind("<Control-s>", save_file)
    t.bind("<Control-S>", save_file_as)
    t.bind("<Control-o>", open_file)
    t.bind("<Control-r>", run_file)
    t.bind("<Control-n>", main)
    # Menubar
    menubar = Menu(root, background=menuColor, foreground="white", activebackground=edColor, activeforeground="white")
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=main)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Save as...", command=save_file_as)
    filemenu.add_command(label="Run file", command=run_file)
    menubar.add_cascade(label="File", menu=filemenu)
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
        sys.exit()
        
if __name__ == "__main__":
    main()