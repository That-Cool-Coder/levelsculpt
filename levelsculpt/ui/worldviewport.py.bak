import tkinter as tk
from copy import copy, deepcopy

import jsonpickle

from levelsculpt.config import *
from levelsculpt.common.misc import *
from levelsculpt.storage import Level, BlockType, Block, BlockSet

class WorldViewport:
    def __init__(self, master,
        size=None, level=None):

        size = defaultIfNone(size, DEFAULT_EDITOR_SIZE)
        level = defaultIfNone(level, DEFAULT_LEVEL, True)

        self.master = master
        self.size = deepcopy(size)
        self.level = deepcopy(level)

        self.zoomAmount = 1
        self.panAmount = Vector2(0, 0)

        self.selectedBlock = None
        self.selectedBlockIndex = None

        self.selectionHandles = [] # order is clockwise from top left

        self.setupCanvas()

    def setupCanvas(self):
        self.canvas = tk.Canvas(self.master, background=self.level.background,
            width=self.size.x, height=self.size.y)
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.tryToSelectBlock)
        self.canvas.bind('<Button-3>', self.resetBlockSprites)
        self.canvas.bind('<MouseWheel>', self.zoom)

        self.resetBlockSprites()

    def resetBlockSprites(self, *args):
        self.blockSprites = []
        self.canvas.delete(tk.ALL)
        
        for block in self.level.blocks:
            self.createBlockSprite(block)
            
        middleOfCanvas = self.getCanvasSize() / 2
        self.canvas.scale(tk.ALL, middleOfCanvas.x, middleOfCanvas.y,
            self.zoomAmount, self.zoomAmount)
    
    def createBlockSprite(self, block:Block):
        bottomRight = block.topLeftPos + block.size
        rect = self.canvas.create_rectangle(
            block.topLeftPos.x,
            block.topLeftPos.y,
            bottomRight.x,
            bottomRight.y,
            fill = block.blockType.color)
        self.blockSprites.append(rect)
    
    def addBlock(self, topLeftPos:Vector2, blockType:BlockType, size:Vector2=None):
        block = Block(topLeftPos, blockType, size)
        self.level.blocks.append(block)
        self.createBlockSprite(block)

    def getCanvasSize(self):
        return Vector2(self.canvas.winfo_width(), self.canvas.winfo_height())

    def canvasToWorldPos(self, position:Vector2):
        posFromCenter = position - self.getCanvasSize() / 2
        posFromCenter *= self.zoomAmount
        return posFromCenter + self.getCanvasSize() / 2
    
    def worldToCanvasPos(self, position:Vector2):
        posFromCenter = position - self.getCanvasSize() / 2
        posFromCenter /= self.zoomAmount
        return posFromCenter + self.getCanvasSize() / 2

    def createSelectionHandles(self):

        # First remove the old handles (just in case they exist)
        self.deleteSelectionHandles()

        # Then create new ones
        for i in range(4):
            handle = self.canvas.create_oval(
                -SELECTION_HANDLE_RADIUS,
                -SELECTION_HANDLE_RADIUS,
                SELECTION_HANDLE_RADIUS,
                SELECTION_HANDLE_RADIUS,
                fill='', outline='white',
                width=SELECTION_HANDLE_THICKNESS)
            self.selectionHandles.append(handle)
        
    def deleteSelectionHandles(self):
        for handle in self.selectionHandles:
            self.canvas.delete(handle)
        self.selectionHandles = []

    def moveSelectionHandlesTo(self, topLeft, bottomRight):
        # Move the selection handles so that they encase
        # a rect from topLeft to bottomRight

        r = SELECTION_HANDLE_RADIUS
        self.canvas.moveto(self.selectionHandles[0], x=topLeft.x - r, y=topLeft.y - r)
        self.canvas.moveto(self.selectionHandles[1], x=bottomRight.x - r, y=topLeft.y - r)
        self.canvas.moveto(self.selectionHandles[2], x=bottomRight.x - r, y=bottomRight.y - r)
        self.canvas.moveto(self.selectionHandles[3], x=topLeft.x - r, y=bottomRight.y - r)

    # Canvas bindings:
    # ----------------

    def zoom(self, event):
        factor = WORLD_ZOOM_SPEED ** event.delta
        middleOfCanvas = self.getCanvasSize() / 2
        self.canvas.scale(tk.ALL, middleOfCanvas.x, middleOfCanvas.y,
            factor, factor)
        self.zoomAmount *= factor
    
    def tryToSelectBlock(self, event):
        pos = self.canvasToWorldPos(Vector2(event.x, event.y))

        self.selectedBlock = None
        self.selectedBlockIndex = None
        for idx, block in enumerate(self.level.blocks):
            if pointInsideRect(pos, block.topLeftPos, block.size):
                self.selectedBlock = block
                self.selectedBlockIndex = idx
        
        # If something is now selected
        if self.selectedBlock is not None:
            topLeft = self.worldToCanvasPos(self.selectedBlock.topLeftPos)
            bottomRight = self.worldToCanvasPos(self.selectedBlock.topLeftPos +
                self.selectedBlock.size)
            self.createSelectionHandles()
            self.moveSelectionHandlesTo(topLeft, bottomRight)
        else:
            self.deleteSelectionHandles()