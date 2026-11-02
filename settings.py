# settings.py

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 672
FPS = 60

# Maze settings
TILE_SIZE = 32
MAZE_COLS = SCREEN_WIDTH // TILE_SIZE   # 25
MAZE_ROWS = 19  # 20

# Game settings
TOTAL_MISSIONS = 50
PLAYER_START_X = 1
PLAYER_START_Y = 1

# Colours (RGB)
BLACK = (15, 18, 25)
WHITE = (245, 245, 245)
WALL_COLOR = (45, 55, 75)
FLOOR_COLOR = (220, 215, 190)
PLAYER_COLOR = (40, 130, 255)
KEY_COLOR = (255, 205, 40)
DOOR_COLOR = (140, 75, 35)
EXIT_COLOR = (40, 190, 100)
CRYSTAL_COLOR = (80, 210, 235)
TEXT_COLOR = (255, 255, 255)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "assets", "images")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")