from tkinter import Frame, Tk
from .frame import StartPage
from .controller import Controller
from .constant import TITLE, WIDTH, HEIGHT

class Container(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack(side="top", fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.start(TITLE, WIDTH, HEIGHT)
        self.container = Container(self)
        self.controller = Controller(self)
        self.frame= StartPage(self.container, self.controller)
        self.frame.grid(row=0, column=0, sticky="nsew")
        

    def start(self, title, width, height):
        self.title(title)
        x = int(self.winfo_screenwidth() / 2 - width / 2)
        y = int(self.winfo_screenheight() / 2 - height / 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(width=False, height=False)




        
            

        
            