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