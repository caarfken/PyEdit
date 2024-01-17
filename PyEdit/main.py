from tkinter import *
import os
import sys
from tkinter import messagebox
import utils
import subprocess
import permissionchanger
from tklinenums import TkLineNumbers



highlightWords = {}

def highlighter(event):
    '''the highlight function, called when a Key-press event occurs'''
    for k,v in highlightWords.items(): # iterate over dict
        startIndex = '1.0'
        while True:
            startIndex = t.search(k, startIndex, END) # search for occurence of k
            if startIndex:
                endIndex = t.index('%s+%dc' % (startIndex, (len(k)))) # find end of k
                t.tag_add(k, startIndex, endIndex) # add tag to k
                t.tag_config(k, foreground=v)      # and color it with v
                startIndex = endIndex # reset startIndex to continue searching
            else:
                break

def on_modified(event):
    t.edit_modified(False) # reset the internal modified flag
    root.after_idle(linenums.redraw) # update line numbers

def autoend(char):
    t.insert("insert", char)
    t.mark_set("insert", "insert-1c")

def autoparen(event=None):
    autoend(")")

def autoquote(event=None):
    autoend('"')
def autosinglequote(event=None):
    autoend("'")
def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

def popup(event):
      try:
        popupmenu.tk_popup(event.x_root, event.y_root, 0)
      finally:
        popupmenu.grab_release()

def copy(event=None):
    root.event_generate("<Control-c>")

def paste(event=None):
    root.event_generate("<Control-v>")

def cut(event=None):
    root.event_generate("<Control-x>")


def confirm_quit(event=None):
    if messagebox.askokcancel("Quit", "Do you want to quit? All unsaved work will be lost."):
        try:
            root.destroy()
        except:
            sys.exit()

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

def open_file(event=None):
        '''This opens a file in the editor'''
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
        t.delete('1.0', END)
        t.insert('1.0', contents)
        

def save_file(event=None):
    try:
        utils.save_file(t, file)
    except: save_file_as()
    finally: saved = True
    

def save_file_as(event=None):
    utils.save_file_as(t.get("1.0", END))

def run_file(event=None):
    messagebox.showinfo("Output", subprocess.check_output([command.strip(), file.name]))

def themeChanger(theme):
    '''This changes the theme. Called by darkTheme, lightTheme, and customTheme'''
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

def changePerms(event=None):
    global file
    permissionchanger.changePermissions(file, root)

def main(event=None):
    '''The main function'''
    # Initialize variables
    global fullscreen
    global command
    global highlightWords
    name = ""
    fullscreen = False
    
    
    # Get theme
    themeName = open(find_data_file("activeTheme.conf"))
    global theme
    global dark
    dark = False
    theme = open(themeName.read())
    menuColor, edColor, textColor = theme.read().split(",")
    if menuColor == "#333333":
        dark = True
    
    
    # Setup extensions
    langsFile = open(find_data_file("langs.csv"))
    global langs
    langs = langsFile.readlines()
    
    # Setup text highlighting
    if dark:
        highlightFile = open(find_data_file("textHighlightingDark.csv"))
    else:
        highlightFile = open(find_data_file("textHighlightingLight.csv"))
    lines = highlightFile.readlines()
    for line in lines:
        name, color = line.split(",")
        highlightWords[name.strip()] = color.strip()
    
    
    # Start Tkinter
    global root
    root = Tk()
    
    # Setup text input
    global t
    t = Text(root, background=edColor, foreground=textColor, insertbackground=textColor)
    t.pack(expand=True, side="right", fill=BOTH)
    
    
    # Handle window being closed
    root.protocol("WM_DELETE_WINDOW", confirm_quit)
    
    # Keybindings
    t.bind("<Key>", highlighter)
    t.bind("<KeyRelease-parenleft>", autoparen)
    t.bind("<KeyRelease-quotedbl>", autoquote)
    t.bind("<KeyRelease-quoteright>", autosinglequote)
    t.bind("<F11>", toggle_fullscreen)
    t.bind("<Control-s>", save_file)
    t.bind("<Control-S>", save_file_as)
    t.bind("<Control-o>", open_file)
    t.bind("<Control-r>", run_file)
    t.bind("<Control-n>", main)
    t.bind("<Control-q>", confirm_quit)
    
    
    # Menubar
    menubar = Menu(root, background=menuColor, foreground=textColor, activebackground=menuColor, activeforeground=textColor)
    
    filemenu = Menu(menubar, tearoff=0)
    
    filemenu.add_command(label="New", accelerator="Control-N", command=main)
    filemenu.add_command(label="Open", accelerator="Control-O", command=open_file)
    filemenu.add_command(label="Save", accelerator="Control-S", command=save_file)
    filemenu.add_command(label="Save as...", accelerator="Control-Shift-S", command=save_file_as)
    filemenu.add_command(label="Run file", accelerator="Control-R", command=run_file)
    filemenu.add_command(label="Quit", accelerator="Control-Q", command=confirm_quit)
    
    menubar.add_cascade(label="File", menu=filemenu)
    
    editmenu = Menu(menubar, tearoff=0)
    
    editmenu.add_command(label="Cut", accelerator="Control-X", command=cut)
    editmenu.add_command(label="Copy", accelerator="Control-C", command=copy)
    editmenu.add_command(label="Paste", accelerator="Control-V", command=paste)
    
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    thememenu = Menu(menubar, tearoff=0)
    
    viewmenu = Menu(menubar, tearoff=0)
    
    viewmenu.add_command(label="Fullscreen", accelerator="F11", command=toggle_fullscreen)
    
    menubar.add_cascade(label="View", menu=viewmenu)
    
    thememenu.add_command(label="Dark Theme", command=darkTheme)
    thememenu.add_command(label="Light Theme", command=lightTheme)
    thememenu.add_command(label="Custom Theme", command=customTheme)
    
    viewmenu.add_cascade(label="Themes", menu=thememenu)
    
    toolsmenu = Menu(menubar, tearoff=0)
    
    toolsmenu.add_command(label="Change Permissions", command=changePerms)
    
    menubar.add_cascade(label="Tools", menu=toolsmenu)
    
    root.config(menu=menubar)
    
    # Right-click menu
    global popupmenu
    
    popupmenu = Menu(root, background=menuColor, foreground=textColor, activebackground=menuColor, activeforeground=textColor, tearoff=0)
    popupmenu.add_command(label="Cut", command=cut)
    popupmenu.add_command(label="Copy", command=copy)
    popupmenu.add_command(label="Paste", command=paste)
    
    root.bind("<Button-3>", popup)
    
    global linenums
    linenums = TkLineNumbers(root, t, justify="left", colors=(textColor, menuColor))
    linenums.pack(fill="y", side="left")
    
    t.bind("<<Modified>>", on_modified, add=True)
    
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
