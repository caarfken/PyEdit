from tkinter import *
from tkinter import messagebox
import oschmod

convert = {
    "add" : "+",
    "remove" : "-",
    "Everyone" : "a",
    "Group" : "g",
    "Owner" : "o",
    "Read" : "r",
    "Write" : "w",
    "Execute" : "e"
}




def add(event=None):
    newPerms = f"{convert[target.get()]}{convert['add']}{convert[perm.get()]}"
    oschmod.set_mode(toChange.name, newPerms)
    messagebox.showinfo("Success!", "Successfully changed permissions.")
    
def remove(event=None):
    newPerms = f"{convert[target.get()]}{convert['remove']}{convert[perm.get()]}"
    oschmod.set_mode(toChange.name, newPerms)
    messagebox.showinfo("Success!", "Successfully changed permissions.")




def changePermissions(file, parent):
    permissions = [
        "Read",
        "Write",
        "Execute"
    ]
    
    targets = [
        "Owner",
        "Group",
        "Everyone"
    ]
    global toChange
    toChange = file
    
    global window
    window = Toplevel(parent)
    window.geometry("200x200")
    
    
    
    global perm
    perm = StringVar()
    perm.set("Read")
    
    permissionMenu = OptionMenu(window, perm, *permissions)
    permissionMenu.pack()
    
    
    global target
    target = StringVar()
    target.set("Owner")
    
    targetMenu = OptionMenu(window, target, *targets)
    targetMenu.pack()
    
    
    addPermButton = Button(window, text="Add selected permission", command=add)
    removePermButton = Button(window, text="Remove selected permission", command=remove)
    
    addPermButton.pack()
    removePermButton.pack()
    
    
    