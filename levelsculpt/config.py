from levelsculpt.common import Vector2
from levelsculpt.storage import BlockType, Block, BlockSet, Level

print('Please ensure that config.py is not imported by anything in storage/')

PRODUCTION_NAME = 'levelsculpt'
ICON_PATH = 'assets\icon.png'

WORLD_ZOOM_SPEED = 1.001

SELECTION_BORDER_THICKNESS = 3
SELECTION_HANDLE_RADIUS = 10
SELECTION_HANDLE_THICKNESS = 3

EDITOR_FRAMERATE_S = 1 / 30
EDITOR_FRAMERATE_MS = int(EDITOR_FRAMERATE_S * 1000)

DEFAULT_EDITOR_SIZE = Vector2(800, 450)

DEFAULT_BLOCKSET = BlockSet('Default', [
    BlockType('platform', Vector2(50, 50), 'lightgoldenrod'),
    BlockType('spike', Vector2(50, 50), 'grey60'),
    BlockType('finishPoint', Vector2(50, 10), '#00ff00'),
])
DEFAULT_LEVEL_BLOCKS = [
    Block(DEFAULT_BLOCKSET.getBlockType('platform'), Vector2(300, 300))
]
DEFAULT_LEVEL = Level('unnamed level', 0, 'skyblue', DEFAULT_BLOCKSET, DEFAULT_LEVEL_BLOCKS)