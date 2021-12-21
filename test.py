import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CamView():  
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)

        self.lmain2 = tk.Label(self.window)
        self.lmain2.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.close) 
        self.show_frame()

    def show_frame(self):
        imgtk = ImageTk.PhotoImage(image=self.parent.img)
        self.lmain2.imgtk = imgtk
        self.lmain2.configure(image=imgtk)

    def close(self):
        self.parent.test_frame = None
        self.window.destroy()

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())

class Main(tk.Frame):
    def __init__(self, parent):

        self.lmain = tk.Label(parent)
        self.lmain.pack()

        self.test_frame = None
        frame = tk.Frame.__init__(self,parent)
        a = tk.Label(text='hello!').pack()
        b = tk.Button(frame, text='open', command=self.load_window)
        b.pack()

        width, height = 800, 600
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.do_stuff()

    def do_stuff(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.img = Image.fromarray(cv2image)
        if self.test_frame != None:
            self.test_frame.show_frame()
        self.lmain.after(10, self.do_stuff)

    def load_window(self):
        if self.test_frame == None:
            self.test_frame = CamView(self)

control = Main(root)
root.mainloop()