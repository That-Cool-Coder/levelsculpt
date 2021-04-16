from levelsculpt.common import Vector2
from levelsculpt.storage import BlockType, Level, Block, BlockSet

PRODUCTION_NAME = 'levelsculpt'
ICON_PATH = 'assets\icon.png'

DEFAULT_EDITOR_SIZE = Vector2(600, 400)
DEFAULT_BLOCKSET = BlockSet('Default', [
    BlockType('platform', Vector2(50, 50), 'lightgoldenrod'),
    BlockType('spike', Vector2(50, 50), 'grey60'),
    BlockType('finishPoint', Vector2(50, 10), '#00ff00'),
])

DEFAULT_LEVEL_BACKGROUND = 'skyblue'
DEFAULT_LEVEL_BLOCKS = [
    Block(DEFAULT_BLOCKSET.getBlockType('platform'))
]