import tkinter as tk

class GUIBuilder:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Simplex Method")

    def loop(self):
        self.master.mainloop()