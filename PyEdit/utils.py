from tkinter import END, filedialog

def get_save_as_dialog():
    file = filedialog.asksaveasfilename()
    file = open(file, "w+")
    return file
def save_file_as(contents):
    file = get_save_as_dialog()
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
    file.write(contents)
    file.close()
