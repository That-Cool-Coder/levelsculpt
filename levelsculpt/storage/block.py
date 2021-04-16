from copy import copy, deepcopy

from levelsculpt.common import Vector2
from levelsculpt.storage import BlockType

class Block:
    def __init__(self, blockType:BlockType,
        topLeftPos:Vector2, size:Vector2=None):
        if size is None:
            size = blockType.defaultSize
            
        self.blockType = deepcopy(blockType)
        self.topLeftPos = deepcopy(topLeftPos)
        self.size = deepcopy(size)