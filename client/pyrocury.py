from tkinter import*
from tkinter.ttk import *
import tkinter.messagebox
import customtkinter
import time

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.geometry("800x400")
window.title("Pyrocury")

# change logo maybe if don't like
logo = PhotoImage(file="icon.png")
window.iconphoto(True, logo)

# toolbar
def openFile():
	pass

def saveFile():
	pass

toolsbar = Menu(window)
window.config(menu=toolsbar)

filebar = Menu(toolsbar, tearoff=0)
toolsbar.add_cascade(label="File",menu=filebar)

filebar.add_command(label="Open", command=openFile)
filebar.add_command(label="Save",command=saveFile)



window.mainloop()