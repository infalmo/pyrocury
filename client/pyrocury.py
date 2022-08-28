import os

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import customtkinter
import time
from server.models.server import process
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("customcolor.json")

window = customtkinter.CTk()
window.geometry("1000x620")
window.title("Metrophon")

# change logo maybe if don't like
logo = PhotoImage(file="icon.png")
window.iconphoto(True, logo)

# video selection frame
videoSelectionFrame = customtkinter.CTkFrame(master=window,
	height=55,
	corner_radius=0)
videoSelectionFrame.pack(fill=X, side=TOP)
videoSelectionFrame.pack_propagate(False)

# choose from file
videoFilePathVar = tk.StringVar()

def openFile():
	file = filedialog.askopenfilename(title="Which mp4 file do you want to choose?",
		filetypes=(('MP4 files', '*.mp4'), ('All files', '*.*')))
	videoFilePathVar.set(file)
	videoPlayerScreen.configure(state=NORMAL)
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
border1 = customtkinter.CTkFrame(videoSelectionFrame,
	width=2,
	height=50,
	corner_radius=0,
	fg_color="#d3d3d3")
border1.pack(side=LEFT)

# youtube url button
videoURLStr = ""

def findURL():
	def returnURL():
		videoURLStr = url_entrybox.get()
		process(videoURLStr)
		videoFilePathVar.set(
			
		)
		videoPlayerScreen.configure(state=NORMAL)
		url_window.destroy()

	url_window = Toplevel()
	url_window.geometry("500x120")
	url_window.title("Youtube URL Box")

	customtkinter.CTkLabel(url_window, text="Enter Youtube URL: ", padx=20, pady=20).grid(row=0, column=0)
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
border2 = customtkinter.CTkFrame(videoSelectionFrame,
	width=2,
	height=50,
	corner_radius=0,
	fg_color="#d3d3d3")
border2.pack(side=LEFT)

# play vid nomarlized
def playVideoNormalized():
	os.system("\"" + saveFilePathEntryText.get() + "\"")

playvidIconLight = PhotoImage(file="playvidiconlight.png")
playvidIconDark = PhotoImage(file="playvidicondark.png")

playVideoButton = customtkinter.CTkButton(master=videoSelectionFrame,
	text="Play Normalized Video",
	text_font=("", 11),
	height=49,
	corner_radius=0,
	image=playvidIconLight,
	compound="left",
	command=playVideoNormalized,
	state=DISABLED
	)
playVideoButton.pack(side=LEFT, padx=5, pady=3)

# top border
bottomBorder = customtkinter.CTkFrame(window,
	height=2,
	corner_radius=0,
	fg_color="#d3d3d3")
bottomBorder.pack(fill=X)

# file chosen
customtkinter.CTkLabel(master=window,
	text="File Chosen: ",
	width=100,
	anchor='w',
	text_font=("",10,'bold')).place(x=15, y=70)

fileChosenPathBox = customtkinter.CTkEntry(master=window,
	textvariable=videoFilePathVar,
	text_font=("",10),
	width=300).place(x=115, y=70)

# speed selector
def setVideoSpeed(video_speed_level):
	if (video_speed_level == "Very Slow"):
		pass
	elif (video_speed_level == "Slow"):
		pass
	elif (video_speed_level == "Medium"):
		pass
	elif (video_speed_level == "Fast"):
		pass
	elif (video_speed_level == "Very Fast"):
		pass

customtkinter.CTkLabel(master=window,
	text="Video Speed: ",
	width=100,
	anchor='w',
	text_font=("",10,'bold')).place(x=15, y=110)

videoSpeedSelector = customtkinter.CTkOptionMenu(master=window,
	values=["Very Slow", "Slow", "Medium", "Fast", "Very Fast"],
	fg_color="#F5B364",
	button_color="#EA907A",
	button_hover_color="#EA644F",
	text_color="black",
	command=setVideoSpeed)
videoSpeedSelector.place(x=115, y=110)

# video player
def playVideoFile():
	os.system("\"" + videoFilePathVar.get() + "\"")

customtkinter.CTkLabel(master=window,
	text="Play selected video",
	text_font=("",10,'bold')).place(x=7, y=154)

videoScreenImage = PhotoImage(file='videoscreen.png')

videoPlayerScreen = customtkinter.CTkButton(master=window,
	text="",
	image=videoScreenImage,
	command=playVideoFile,
	state=DISABLED
	)
videoPlayerScreen.place(x=15, y=180)

# save to
saveFilePathEntryText = tk.StringVar()
# saveFileName = ""

def setSaveDestination():
	file = filedialog.asksaveasfile(defaultextension='.mp4',
		filetypes=[
		("MP4 file",".mp4"),
		("All files",".*")
		])
	# file = filedialog.askdirectory()			# this will prompt you to save to a directory. However, you would need to use a variable like saveFileName in order to put the file path in playVideoNormalized()
	if file is None:
		return

	saveFilePathEntryText.set(file.name)

	# file.dosomething
	# file.close()

customtkinter.CTkLabel(master=window,
	text="Save to: ",
	width=80,
	anchor='w',
	text_font=("",10,'bold')).place(x=15, y=500)

saveDestinationBox = customtkinter.CTkEntry(master=window,
	textvariable=saveFilePathEntryText,
	text_font=("",10),
	width=785).place(x=80, y=500)

saveDestinationButton = customtkinter.CTkButton(master=window,
	text="Browse",
	border_width=2,
	width=100,
	command=setSaveDestination).place(x=880, y=500)


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
completedNormalization = False

normalizationButtonFrame = customtkinter.CTkFrame(master=footerbarFrame,
	height=50)
normalizationButtonFrame.pack(side=RIGHT, padx=18)
normalizationButtonFrame.pack_propagate(False)

def startNormalization():
	progress_window = Toplevel()
	progress_window.geometry("500x120")
	progress_window.title("Normalizing...")
	progress_window.config(pady=20)

	progressbar = Progressbar(progress_window,
		orient=HORIZONTAL,
		length=300,
		mode="indeterminate")
	progressbar.pack(pady=10)
	customtkinter.CTkLabel(progress_window,
		text="Loading...").pack()

	progressbar.start()
	progress_window.update()

	if (completedNormalization):
		playVideoButton.configure(state=NORMAL)
		progress_window.destroy()

startNormalizationButton = customtkinter.CTkButton(master=normalizationButtonFrame,
	text="Start Normalization",
	text_font=("", 11),
	text_color="black",
	height=35,
	width=150,
	border_width=2,
	fg_color="#91C788",
	hover_color="#52734D",
	command=startNormalization)
startNormalizationButton.pack(side=RIGHT)

window.mainloop()