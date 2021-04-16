from copy import copy, deepcopy

from levelsculpt.config import *

class BlockType:
    def __init__(self, name, defaultSize, color):
        self.name = name
        self.defaultSize = copy(defaultSize)
        self.color = color