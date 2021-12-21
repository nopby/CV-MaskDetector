from .window import Window

class App:
    def __init__(self):
        self.root = Window()
          
    def run(self):
        self.root.mainloop()

