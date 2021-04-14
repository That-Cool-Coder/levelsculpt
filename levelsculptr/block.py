from copy import copy, deepcopy
import tkinter as tk

from levelsculptr.common import Vector2

class Block:
    def __init__(self, canvas:tk.Canvas, topLeftPos:Vector2, size:Vector2, color):
        self.canvas = canvas
        self.topLeftPos = copy(topLeftPos)
        self.size = copy(size)
        self.color = color

        self.rect = self.canvas.create_rectangle(self.topLeftPos.x, self.topLeftPos.y,
            self.topLeftPos.x + self.size.x, self.topLeftPos.y + self.size.y,
            fill=self.color)