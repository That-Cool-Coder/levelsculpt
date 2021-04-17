import tkinter as tk
from copy import copy, deepcopy

import jsonpickle

from levelsculpt.config import *
from levelsculpt.common.misc import *
from levelsculpt.storage import Level, BlockType, Block, BlockSet

class EditorSidebar:
    def __init__(self, master, settingsUpdateFunction, crntSettings=None):
        self.master = master
        self.settingsUpdateFunction = settingsUpdateFunction

        self.crntSettings = defaultIfNone(crntSettings, DEFAULT_EDITOR_SETTINGS)

        self.frame = tk.Frame(self.master, width=DEFAULT_EDITOR_SIDEBAR_SIZE.x,
            height=DEFAULT_EDITOR_SIDEBAR_SIZE.y,
            background='white')
        self.frame.pack()

        self.stringVars = {
            'blockType' : tk.StringVar(self.frame)
        }

        blockNames = self.crntSettings['blockSet'].getBlockTypeNames()
        self.stringVars['blockType'].set(self.crntSettings['blockType'].name)

        self.blockTypeSelect = tk.OptionMenu(self.frame, self.stringVars['blockType'],
            *blockNames, command=self.onSettingsChange)
        self.blockTypeSelect.pack()
    
    def onSettingsChange(self, event):
        self.crntSettings = {
            'blockSet' : self.crntSettings['blockSet'],
            'blockType' : self.crntSettings['blockSet'].getBlockType(self.stringVars['blockType'].get())
        }
        self.settingsUpdateFunction(self.crntSettings)