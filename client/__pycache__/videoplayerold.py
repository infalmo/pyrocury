customtkinter.CTkLabel(master=window,
	text="Play selected video").place(x=15, y=160)

videoScreenImage = PhotoImage(file='videoscreen.png')

videoPlayerButton = customtkinter.CTkButton(master=window,
	text="",
	# image=videoScreenImage,
	# command=playVideo,
	state=DISABLED
	)
videoPlayerButton.place(x=25, y=168)