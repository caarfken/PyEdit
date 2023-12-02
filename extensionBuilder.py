from tkinter import *
from tkinter import simpledialog

root = Tk()
root.withdraw()

name = simpledialog.askstring("Language Name", "Please enter the language's name, e.g. Python")
extension = simpledialog.askstring("Language Extension", "Please enter the language's extension, e.g. .py")
command = simpledialog.askstring("Language Command", "Please enter the language's run command e.g. python")

file = open("langs.csv", "a+")
file.write(name + "," + extension + "," + command)
file.write("\n")
file.close()