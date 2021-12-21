from App.constant import HEIGHT, WIDTH
from .camera import Camera
from .image import Img
from .utils import Utils
from tkinter import filedialog

class Controller:
    def __init__(self, master):
        self.master = master
        self.camera = Camera(self)
        self.image = Img(self)
        self.utils = Utils()
        self.item_id = 0
    
    def show_frame(self, frame):
        frame = self.master.frames[frame]
        frame.tkraise()

    def show_camera(self):
        self.camera.start()
        self.camera.mainloop()

    def show_image(self):
        file = filedialog.askopenfilename(
                title="Select An Image", 
                filetypes=(
                    ("JPG files", "*.jpg"),
                    ("PNG files", "*.png")
                )
            )
        if file:
            self.image.start()
            self.image.show(file)


    def findXCenter(self, canvas, item):
        coords = canvas.bbox(item)
        xOffset = (WIDTH / 2) - ((coords[2] - coords[0]) / 2)
        return xOffset

    def destroy(self):
        self.master.destroy()