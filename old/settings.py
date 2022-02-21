import sys
from tkinter import *
from tkinter import ttk

def main():
    root = Tk()

    root.geometry("400x400")

    def done():    
        with open("theme.csv", "w") as file:
            if edcolor.get() == "" and mencolor.get() == "":
                file.write("#ffffff, #ffffff")
            elif edcolor.get() == "":
                file.write(mencolor.get() + "," + "#000000")
            elif mencolor.get() == "":
                file.write("#000000" + "," + edcolor.get())
            else:
                file.write(mencolor.get() + "," + edcolor.get())
        sys.exit()
    edcolor = StringVar(root)
    mencolor = StringVar(root)

    edLabel = ttk.Label(root, text="Editor color: ")
    edLabel.pack()

    edInput = ttk.Entry(root, textvariable=edcolor)
    edInput.pack()

    menLabel = ttk.Label(root, text="Menu bar color: ")
    menLabel.pack()

    menInput = ttk.Entry(root, textvariable=mencolor)
    menInput.pack()

    ttk.Button(root, text="Done", command=done).pack()
    root.mainloop()

if __name__ == "__main__":
    main()