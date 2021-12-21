import os
from tkinter import Button, Canvas, Frame, Label, filedialog
from PIL import Image, ImageTk



class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg = Image.open("App/Etc/background.jpg")
        self.bg = ImageTk.PhotoImage(bg)
        canvas = Canvas(self)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg, anchor="nw")

        title = canvas.create_text(0, 0, text="Mask Detector", font=("Arial", 50), fill="red", anchor="nw")
        canvas.move(title, controller.findXCenter(canvas, title), 100)

        detect_btn = canvas.create_window(
            0, 0, window=Button(canvas, text="Detect", font=("Arial", 15), 
            width=10, command=lambda: controller.show_image()),
            anchor="nw"
        )
        canvas.move(detect_btn, controller.findXCenter(canvas, detect_btn), 200)

        exit_btn = canvas.create_window(
            0, 0, window=Button(canvas, text="Exit", font=("Arial", 15), 
            width=10, command=lambda: controller.destroy()),
            anchor="nw"            
        )
        canvas.move(exit_btn, controller.findXCenter(canvas, exit_btn), 270)

    




