import tkinter as tk

from levelsculpt.config import *
from copy import copy, deepcopy

class EditorViewport:
    def __init__(self, master,
        size=DEFAULT_EDITOR_SIZE, level=DEFAULT_LEVEL):

        self.master = master
        self.level = deepcopy(level)

        self.canvas = tk.Canvas(self.master, background=self.level.background,
            width=size.x, height=size.y)
        self.canvas.pack()