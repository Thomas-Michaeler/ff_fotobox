import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class Countdown(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="")
        self.label.config(font=("Courier", 60))
        self.label.config(bg=("green"))
        
        self.label.pack()
        self.remaining = 0
        self.countdown(5)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="Cheeeeeeeeeese!!!!")
            #
            #
            #
            # hier capture_image einfügen!!!
            #
            #
            #
            img = PhotoImage(file="test.png") #JPG files don't work!!!
            self.label.configure(image=img)
            self.label.image = img
            
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining -1
            self.after(1000, self.countdown)

if __name__ == "__main__":
    app = Countdown()
    app.attributes("-fullscreen", True)
    app.mainloop()
