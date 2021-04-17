import tkinter as tk
from copy import copy, deepcopy

import jsonpickle

from levelsculpt.config import *
from levelsculpt.common import KeyTracker
from levelsculpt.common.misc import *
from levelsculpt.storage import Level, BlockType, Block, BlockSet

class EditorViewport:
    def __init__(self, master,
        size=None, level=None, settings=None):

        size = defaultIfNone(size, DEFAULT_EDITOR_SIZE)
        level = defaultIfNone(level, DEFAULT_LEVEL)
        settings = defaultIfNone(settings, DEFAULT_EDITOR_SETTINGS)

        self.master = master
        self.size = deepcopy(size)
        self.level = deepcopy(level)

        self.zoomAmount = 1
        self.panAmount = Vector2(0, 0)

        self.settings = settings

        self.selectedBlock = None
        self.leftMouseDown = False
        self.rightMouseDown = False
        self.mousePos = Vector2(0, 0)

        self.isResizingBlock = False
        self.blockResizingSides = []

        self.setupCanvas()
        self.keyTracker = KeyTracker(self.canvas)

        self.topLevel = self.master.winfo_toplevel()
        self.topLevel.after(EDITOR_FRAMERATE_MS, self.drawLoop)

    def setupCanvas(self):
        self.canvas = tk.Canvas(self.master, background=self.level.background,
            width=self.size.x, height=self.size.y)
        self.canvas.pack()

        # Setup all of the bindings
        # add='+' means that previous bindings aren't deleted
        #self.canvas.bind('<B3-Motion>', self.panView)
        self.canvas.bind('<Button-3>', self.deleteBlockOnClick, add='+')
        self.canvas.bind('<Button-1>', self.startResizingBlock, add='+')
        self.canvas.bind('<Button-1>', self.createBlockOnClick, add='+')
        self.canvas.bind('<Button-1>', self.selectBlockOnClick, add='+')
        self.canvas.bind('<ButtonRelease-1>', self.stopResizingBlock, add='+')
        self.canvas.bind('<Motion>', self.updateMousePos, add='+')
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
        if self.isResizingBlock:
            worldMousePos = self.screenToWorldPos(self.mousePos)
            if 'top' in self.blockResizingSides:
                self.selectedBlock.size.y += self.selectedBlock.topLeftPos.y - \
                    worldMousePos.y
                self.selectedBlock.topLeftPos.y = worldMousePos.y
            if 'right' in self.blockResizingSides:
                self.selectedBlock.size.x = worldMousePos.x - \
                    self.selectedBlock.topLeftPos.x
            if 'bottom' in self.blockResizingSides:
                self.selectedBlock.size.y = worldMousePos.y - \
                    self.selectedBlock.topLeftPos.y
            if 'left' in self.blockResizingSides:
                self.selectedBlock.size.x += self.selectedBlock.topLeftPos.x - \
                    worldMousePos.x
                self.selectedBlock.topLeftPos.x = worldMousePos.x
    
    
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
            if pointInsideRect(self.mousePos, block.topLeftPos, block.size):
                blocks.append(block)
        return blocks
    
    # Canvas bindings
    # ---------------

    def zoom(self, event):
        self.zoomAmount *= EDITOR_ZOOM_SPEED ** event.delta
    
    def panView(self, event):
        pass
    
    def updateMousePos(self, event):
        self.mousePos = Vector2(event.x, event.y)

    def deleteBlockOnClick(self, event):
        clickedBlocks = self.getBlocksContainingPos(self.mousePos)
        if len(clickedBlocks) > 0:
            # Delete the latest (topmost) block
            self.level.blocks.remove(clickedBlocks[-1])

    def createBlockOnClick(self, event):
        # Only create block if control is up and no blocks are already clicked
        # and no block is selected

        worldMousePos = self.screenToWorldPos(self.mousePos)
        clickingExistingBlock = len(self.getBlocksContainingPos(worldMousePos)) > 0
        if not self.keyTracker.controlDown() and \
            not clickingExistingBlock and \
            self.selectedBlock is None:

            blockType = self.settings['blockType']
            pos = self.screenToWorldPos(Vector2(event.x, event.y))
            pos -= blockType.defaultSize / 2
            block = Block(blockType, pos, blockType.defaultSize)
            self.level.blocks.append(block)

            # It's really annoying to have to click off a block you just created,
            # so deselect the new block
            self.selectedBlock = None
    
    def selectBlockOnClick(self, event):
        clickedBlocks = self.getBlocksContainingPos(self.screenToWorldPos(self.mousePos))
        if len(clickedBlocks) > 0:
            # Get the last (topmost) block
            self.selectedBlock = clickedBlocks[-1]
        # Don't deselect blocks while they're being resized
        elif not self.isResizingBlock:
            self.selectedBlock = None
        
    def startResizingBlock(self, event):
        # Only resize block that is selected
        if self.selectedBlock is not None:
            self.blockResizingSides = []

            # Precalculate the corners of the block because it's a bit messy
            topLeftPos = self.selectedBlock.topLeftPos
            topRightPos = Vector2(topLeftPos.x +
                self.selectedBlock.size.x, topLeftPos.y)
            bottomRightPos = self.selectedBlock.topLeftPos + \
                self.selectedBlock.size
            bottomLeftPos = Vector2(topLeftPos.x, topLeftPos.y +
                self.selectedBlock.size.y)

            # Is top edge clicked?
            if lineIntersectsCircle(topLeftPos, topRightPos,
                self.mousePos, SELECTION_BORDER_GRAB_WIDTH):
                self.blockResizingSides.append('top')
            # Is right edge clicked?
            if lineIntersectsCircle(topRightPos, bottomRightPos,
                self.mousePos, SELECTION_BORDER_GRAB_WIDTH):
                self.blockResizingSides.append('right')
            # Is bottom edge clicked?
            if lineIntersectsCircle(bottomRightPos, bottomLeftPos,
                self.mousePos, SELECTION_BORDER_GRAB_WIDTH):
                self.blockResizingSides.append('bottom')
            # Is left edge clicked?
            if lineIntersectsCircle(bottomLeftPos, topLeftPos,
                self.mousePos, SELECTION_BORDER_GRAB_WIDTH):
                self.blockResizingSides.append('left')
            
            self.isResizingBlock = len(self.blockResizingSides) > 0
    
    def stopResizingBlock(self, event):
        self.isResizingBlock = False
        self.blockResizingSides = []