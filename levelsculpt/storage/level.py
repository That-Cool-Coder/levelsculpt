from copy import copy, deepcopy

from levelsculpt.common.misc import *
from levelsculpt.storage import Block, BlockType, BlockSet

class Level:
    # Call with no args and you get the default level
    def __init__(self, name:str, index:int,
        background:str, blockset:BlockSet, blocks:list):
        self.name = name
        self.index = index
        self.background = background
        self.blockset = blockset
        self.blocks = blocks
