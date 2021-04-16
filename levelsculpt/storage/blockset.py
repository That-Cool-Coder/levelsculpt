from copy import copy, deepcopy

from levelsculpt.config import *
from levelsculpt.storage import BlockType

class BlockSet:
    def __init__(self, name:str, blockTypes:list):
        self.name = name

        # Blocktypes are stored internally as a dict
        # this makes lookup super easy
        self.blockTypes = {}
        self.addBlockTypes(blockTypes)

    def getBlockType(self, typeName:str):
        try:
            return self.blockTypes[typeName]
        except IndexError:
            return None

    def addBlockType(self, blockType:BlockType):
        self.blockTypes[blockType.name] = deepcopy(blockType)
    
    def addBlockTypes(self, blockTypes:list):
        for blockType in blockTypes:
            self.addBlockType(blockType)

    def removeBlockType(self, blockTypeName:BlockType):
        del self.blockTypes[blockType.name]
    
    def removeBlockTypes(self, blockTypeNames:list):
        for blockTypeName in blockTypeNames:
            self.removeBlockType(blockTypeName)