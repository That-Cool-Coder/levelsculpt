from copy import copy, deepcopy

from levelsculpt.config import *

class Level:
    # Call with no args and you get the default level
    def __init__(self, name=None, index=None,
        background=DEFAULT_LEVEL_BACKGROUND,
        blockset=DEFAULT_BLOCKSET, blocks=[]):

        self.name = name
        self.index = index
        self.background = background
        self.blockset = blockset
        self.blocks = blocks
