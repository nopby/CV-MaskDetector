
from tkinter import Toplevel, Label, filedialog, Button
from PIL import ImageTk, Image
import cv2

class Camera:
    def __init__(self, controller):
        self.controller = controller
        self.window = None
        self.label = None
        self.button = None
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

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

    def mainloop(self):
        if self.running:
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            (locs, preds) = self.controller.utils.pred(frame)

            for (box, pred) in zip(locs, preds):
                (x0, y0, x1, y1) = box
                (mask, withoutMask) = pred

                label = "Mask" if mask > withoutMask else "No Mask"
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, .45, color, 2)
                cv2.rectangle(frame, (x0, y0), (x1, y1), color, 2)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.image = Image.fromarray(cv2image)
            imagetk = ImageTk.PhotoImage(image=self.image)
            self.label.imagetk = imagetk
            self.label.configure(image=self.label.imagetk)

        self.label.after(10, self.mainloop)

    def destroy(self):
        self.label = None
        self.window.destroy()

    def save(self):
        self.running = False
        dir = filedialog.asksaveasfile(mode="w", filetypes=(("JPEG", "*.jpg"), ("PNG", "*.png")) ,defaultextension=".jpg")
        if dir:
            self.image.save(dir)
        self.running = True

