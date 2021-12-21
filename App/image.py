
from tkinter import Label, Toplevel, filedialog, Button
import cv2
from PIL import ImageTk, Image

class Img:
    def __init__(self, controller):
        self.controller = controller
        self.window = None
        self.label = None

    def start(self):
        if self.window:
            self.destroy()
        self.window = Toplevel(self.controller.master)
        self.window.resizable(width=False, height=False)
        self.window.protocol("WM_DELETE_WINDOW", self.destroy) 
        self.label = Label(self.window)
        self.label.pack()
        self.button = Button(self.window, text="Save", bg="#76b5c5", command=self.save)
        self.button.pack(expand=True, fill="both")

    def show(self, image):
        self.image = cv2.imread(image)
        self.image = cv2.resize(self.image, (800, 600), interpolation=cv2.INTER_AREA)
        (locs, preds) = self.controller.utils.pred(self.image)
        for (box, pred) in zip(locs, preds):
            (x0, y0, x1, y1) = box
            (mask, withoutMask) = pred

            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            cv2.putText(self.image, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.rectangle(self.image, (x0, y0), (x1, y1), color, 2)

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(self.image)
        imagetk = ImageTk.PhotoImage(image=self.image)
        self.label.imagetk = imagetk
        self.label.configure(image=self.label.imagetk)

    def destroy(self):
        self.frame = None
        self.window.destroy()

    def save(self):
        dir = filedialog.asksaveasfile(mode="w", filetypes=(("JPEG", "*.jpg"), ("PNG", "*.png")) ,defaultextension=".jpg")
        if dir:
            self.image.save(dir)
