from tkinter import *
from tkinter import ttk

def clicked():

    ttk.Label(frm, text="bye!").grid(column=0, row=0)

def try_gui():

    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    txt = Entry(frm,width=10)

    txt.grid(column=1, row=0)

    btn = Button(frm, text="export", command=clicked)
    btn.grid(column=2, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=3, row=0)
    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    frm = ttk.Frame(root, padding=100)
    try_gui()