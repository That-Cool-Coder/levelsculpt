import tkinter as tk

from levelsculptr.config import *

class EditorArea:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, background='skyblue')
        self.canvas.pack()

        self.levelData = []