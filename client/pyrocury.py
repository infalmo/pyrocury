from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import customtkinter
import time


customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("C:\\Users\\andre\\Documents\\GitHub\\pyrocury\\client\\customcolor.json")

window = customtkinter.CTk()
window.geometry("1000x600")
window.title("Pyrocury")

# change logo maybe if don't like
logo = PhotoImage(file="icon.png")
window.iconphoto(True, logo)

# toolbar

# video selection frame
videoSelectionFrame = customtkinter.CTkFrame(master=window,
	height=55,
	corner_radius=0)
videoSelectionFrame.pack(fill=X, side=TOP)
videoSelectionFrame.pack_propagate(False)

# choose from file
videoFilePathStr = ""

def openFile():
	videoFilePathStr = filedialog.askopenfilename(initialdir="C:\\Users\\andre\\Documents\\",
		title="Which mp4 file do you want to choose?",
		filetypes=(('MP4 files', '*.mp4'), ('All files', '*.*')))
	videoURLStr = ""

folderIconLight = PhotoImage(file="foldericonlight.png")
folderIconDark = PhotoImage(file="foldericondark.png")

selectFileButton = customtkinter.CTkButton(master=videoSelectionFrame,
	text="Choose From File",
	text_font=("", 11),
	height=49,
	corner_radius=0,
	image=folderIconLight,
	compound="left",
	command=openFile)
selectFileButton.pack(side=LEFT, padx=5, pady=3)

# border
border1 = Frame(videoSelectionFrame,
	width=2,
	height=60,
	bg="#d3d3d3")
border1.pack(side=LEFT)

# youtube url button
videoURLStr = ""

def findURL():
	def returnURL():
		videoURLStr = url_entrybox.get()
		videoFilePathStr = ""
		url_window.destroy()

	url_window = Toplevel()
	url_window.geometry("500x120")
	url_window.title("Youtube URL Box")

	Label(url_window, text="Enter Youtube URL: ", padx=20, pady=20).grid(row=0, column=0)
	url_entrybox = customtkinter.CTkEntry(master=url_window,
		placeholder_text="http://www.youtube.com/...",
		width=240)
	url_entrybox.grid(row=0, column=1)

	url_submitButton = customtkinter.CTkButton(master=url_window,
		text="Use Selected URL",
		command=returnURL)
	url_submitButton.grid(row=1, column=0, columnspan=2)

youtubeIconLight = PhotoImage(file="youtubeiconlight.png")
youtubeIconDark = PhotoImage(file="youtubeicondark.png")

urlVideoButton = customtkinter.CTkButton(master=videoSelectionFrame,
	text="Choose From URL",
	text_font=("", 11),
	height=49,
	corner_radius=0,
	image=youtubeIconLight,
	compound="left",
	command=findURL)
urlVideoButton.pack(side=LEFT, padx=5, pady=3)

# border
border2 = Frame(videoSelectionFrame,
	width=2,
	height=60,
	bg="#d3d3d3")
border2.pack(side=LEFT)

# play vid
def playVideo():
	pass

playvidIconLight = PhotoImage(file="playvidiconlight.png")
playvidIconDark = PhotoImage(file="playvidicondark.png")

playVideoButton = customtkinter.CTkButton(master=videoSelectionFrame,
	text="Play Normalized Video",
	text_font=("", 11),
	height=49,
	corner_radius=0,
	text_color_disabled="#8a0303",
	image=playvidIconLight,
	compound="left",
	state=DISABLED,
	command=playVideo)
playVideoButton.pack(side=LEFT, padx=5, pady=3)

# bottom border
bottomBorder = Frame(window,
	height=3,
	bg="#d3d3d3")
bottomBorder.pack(fill=X)


# bottom bar
footerbarFrame = customtkinter.CTkFrame(master=window,
	height=60,
	corner_radius=0)
footerbarFrame.pack(fill=X, side=BOTTOM)
footerbarFrame.pack_propagate(False)

# dark or light mode
brightnessOptionsFrame = customtkinter.CTkFrame(master=footerbarFrame,
	height=50)
brightnessOptionsFrame.pack(side=LEFT, padx=20)
brightnessOptionsFrame.pack_propagate(False)

def changeBrightness(new_appearance_mode):
	customtkinter.set_appearance_mode(new_appearance_mode)
	if (new_appearance_mode == "Light"):
		selectFileButton.configure(image=folderIconLight)
		urlVideoButton.configure(image=youtubeIconLight)
		playVideoButton.configure(image=playvidIconLight)
		border1.config(bg="#d3d3d3")
		border2.config(bg="#d3d3d3")
		bottomBorder.config(bg="#d3d3d3")
	else:
		selectFileButton.configure(image=folderIconDark)
		urlVideoButton.configure(image=youtubeIconDark)
		playVideoButton.configure(image=playvidIconDark)
		border1.config(bg="black")
		border2.config(bg="black")
		bottomBorder.config(bg="black")

brightnessOptionMenu = customtkinter.CTkOptionMenu(master=brightnessOptionsFrame,
	values=["Light", "Dark"],
	fg_color="#608BD5",
	command=changeBrightness)
brightnessOptionMenu.pack(side=LEFT)

# start normalization
normalizationButtonFrame = customtkinter.CTkFrame(master=footerbarFrame,
	height=50)
normalizationButtonFrame.pack(side=RIGHT, padx=18)
normalizationButtonFrame.pack_propagate(False)

def startNormalization():
	pass

startNormalizationButton = customtkinter.CTkButton(master=normalizationButtonFrame,
	text="Start Normalization",
	text_font=("", 11),
	text_color="black",
	height=35,
	width=150,
	border_width=2,
	fg_color="#3CB043",
	hover_color="#228C22",
	command=startNormalization)
startNormalizationButton.pack(side=RIGHT)

window.mainloop()