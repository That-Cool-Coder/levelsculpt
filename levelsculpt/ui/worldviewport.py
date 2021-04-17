import tkinter as tk
from copy import copy, deepcopy

import jsonpickle

from levelsculpt.config import *
from levelsculpt.common import KeyTracker
from levelsculpt.common.misc import *
from levelsculpt.storage import Level, BlockType, Block, BlockSet

class WorldViewport:
    def __init__(self, master,
        size=None, level=None):

        size = defaultIfNone(size, DEFAULT_EDITOR_SIZE)
        level = defaultIfNone(level, DEFAULT_LEVEL, True)

        self.master = master
        self.topLevel = self.master.winfo_toplevel()
        self.size = deepcopy(size)
        self.level = deepcopy(level)

        self.zoomAmount = 1
        self.panAmount = Vector2(0, 0)

        self.selectedBlock = None
        self.leftMouseDown = False
        self.rightMouseDown = False
        self.mousePos = Vector2(0, 0)

        self.setupCanvas()
        self.keyTracker = KeyTracker(self.canvas)

        self.topLevel.after(EDITOR_FRAMERATE_MS, self.drawLoop)

    def setupCanvas(self):
        self.canvas = tk.Canvas(self.master, background=self.level.background,
            width=self.size.x, height=self.size.y)
        self.canvas.pack()

        #self.canvas.bind('<B3-Motion>', self.panView)
        self.canvas.bind('<Button-3>', self.deleteClickedBlock)
        self.canvas.bind('<Button-1>', self.createBlockOnClick)
        self.canvas.bind('<Button-1>', self.selectBlockOnClick)
        self.canvas.bind('<Motion>', self.updateMousePos)
        self.canvas.bind('<MouseWheel>', self.zoom)

    def drawLoop(self):
        self.canvas.delete(tk.ALL)

        if self.rightMouseDown:
            self.panAmount += self.prevMousePos - self.mousePos

        for block in self.level.blocks:
            self.drawBlock(block)
        
        self.editSelectedBlock()
        self.drawSelectedBlockOutline()
        
        self.topLevel.after(EDITOR_FRAMERATE_MS, self.drawLoop)
        self.prevMousePos = deepcopy(self.mousePos)

    def drawBlock(self, block:Block):
        screenTopLeft = self.worldToScreenPos(block.topLeftPos)
        screenBottomRight = self.worldToScreenPos(block.topLeftPos + block.size)
        self.canvas.create_rectangle(screenTopLeft.x, screenTopLeft.y,
            screenBottomRight.x, screenBottomRight.y,
            fill=block.blockType.color)
    
    def drawSelectedBlockOutline(self):
        if self.selectedBlock is not None:
            topLeftPos = self.worldToScreenPos(self.selectedBlock.topLeftPos)
            bottomRightPos = self.worldToScreenPos(self.selectedBlock.topLeftPos +
                self.selectedBlock.size)
            self.canvas.create_rectangle(topLeftPos.x, topLeftPos.y,
                bottomRightPos.x, bottomRightPos.y, fill='', outline='white',
                width=SELECTION_BORDER_THICKNESS)
    
    def editSelectedBlock(self):
        if lineIntersectsCircle(Vector2(0, 100), Vector2(100, 100), self.mousePos, 5):
            self.canvas.create_oval(self.mousePos.x - 5, self.mousePos.y - 5, self.mousePos.x, self.mousePos.y, fill='red')
    
    def worldToScreenPos(self, pos:Vector2):
        newPos = pos - self.panAmount
        newPos += self.size / 2 / self.zoomAmount
        newPos *= self.zoomAmount
        newPos -= self.size / 2
        return newPos

    def screenToWorldPos(self, pos:Vector2):
        newPos = pos + self.size / 2
        newPos /= self.zoomAmount
        newPos -= self.size / 2 / self.zoomAmount
        newPos += self.panAmount
        return newPos
    
    def getBlocksContainingPos(self, pos):
        blocks = []
        for block in self.level.blocks:
            if pointInsideRect(block.topLeftPos, block.size, self.mousePos):
                blocks.append(block)
        return blocks
    
    # Canvas bindings
    # ---------------

    def zoom(self, event):
        self.zoomAmount *= WORLD_ZOOM_SPEED ** event.delta
    
    def panView(self, event):
        pass
    
    def updateMousePos(self, event):
        self.mousePos = Vector2(event.x, event.y)

    def deleteClickedBlock(self, event):
        clickedBlocks = self.getBlocksContainingPos(self.mousePos)
        if len(clickedBlocks) > 0:
            # Delete the latest (topmost) block
            self.level.blocks.remove(clickedBlocks[-1])

    def createBlockOnClick(self, event):
        # Only create block if control is up and no blocks are already clicked
        if not self.keyTracker.controlDown() and \
            len(self.getBlocksContainingPos(self.mousePos)) == 0:
            blockType = self.level.blockset.getBlockType('platform')
            pos = self.screenToWorldPos(Vector2(event.x, event.y))
            pos -= blockType.defaultSize / 2
            block = Block(blockType, pos, blockType.defaultSize)
            self.level.blocks.append(block)
    
    def selectBlockOnClick(self, event):
        clickedBlocks = self.getBlocksContainingPos(self.mousePos)
        if len(clickedBlocks) > 0:
            # Get the last (topmost) block
            self.selectedBlock = clickedBlocks[-1]
        else:
            self.selectedBlock = None