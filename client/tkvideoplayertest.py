import tkinter as tk
from tkVideoPlayer import TkinterVideo

window = tk.Tk()

videoplayer = TkinterVideo(master=window,
	scaled=True)
videoplayer.load(r"minecraft zombie break dance.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play()

window.mainloop()