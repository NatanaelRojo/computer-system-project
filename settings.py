import os
import pathlib

import pygame

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

# Size of the square tiles used in this environment.
TILE_SIZE = 24

# Grid
ROWS = 10
COLS = 10

NUM_TILES = ROWS * COLS
NUM_ACTIONS = 4
INITIAL_STATE = 0

# Building maze parameters
START = 0
END = 77
# REWARD_POSITION = [21, 33, 34]
# WALLS = set([(1, 7), (7, 8), (9, 10), (14, 15), (15, 21), (24, 30),
#             (24, 25), (25, 26), (28, 34), (32, 33)])
# HOLES = [3, 12, 17, 20, 35]

REWARD_POSITION = [43, 77]
# self.tri_force = 77
WALLS = set([(0, 10), (2, 12), (2, 3), (4, 5), (4, 14), (6, 16), (8, 18), (11, 12),
            (13, 14), (15, 16), (17, 18), (19, 29), (20, 21), (21, 31), (23, 33),
            (25, 35), (27, 37), (27, 28), (28, 29), (30, 31), (32, 42), (34, 44),
            (34, 35), (36, 37), (42, 43), (44, 54), (46, 47), (47, 57), (59, 69),
            (61, 62), (64, 65), (65, 75), (65, 66), (68, 69), (71, 81), (71, 72),
            (75, 85), (81, 82), (82, 92), (96, 97)])

HOLES = [4, 24, 40, 48, 54, 56, 60, 63, 78, 84, 86, 90, 92, 99]


# Resolution to emulate
VIRTUAL_WIDTH = TILE_SIZE * COLS
VIRTUAL_HEIGHT = TILE_SIZE * ROWS

# Scale factor between virtual screen and window
H_SCALE = 3
V_SCALE = 3

# Resolution of the actual window
WINDOW_WIDTH = VIRTUAL_WIDTH * H_SCALE
WINDOW_HEIGHT = VIRTUAL_HEIGHT * V_SCALE

# Default pause time between steps (in seconds)
DEFAULT_DELAY = 1.0

BASE_DIR = pathlib.Path(__file__).parent

# Textures used in the environment
TEXTURES = {
    "ice": pygame.image.load(BASE_DIR / "assets" / "graphics" / "ice.png"),
    "hole": pygame.image.load(BASE_DIR / "assets" / "graphics" / "hole.png"),
    "cracked_hole": pygame.image.load(
        BASE_DIR / "assets" / "graphics" / "cracked_hole.png"
    ),
    "goal": pygame.image.load(BASE_DIR / "assets" / "graphics" / "goal.png"),
    "reco": pygame.image.load(BASE_DIR / "assets" / "graphics" / "reco.png"),
    "stool": pygame.image.load(BASE_DIR / "assets" / "graphics" / "stool.png"),
    "diamon": pygame.image.load(BASE_DIR / "assets" / "graphics" / "diamon.png"),
    "wood": pygame.image.load(BASE_DIR / "assets" / "graphics" / "wood.png"),
    "Arbol": pygame.image.load(BASE_DIR / "assets" / "graphics" / "Arbol.png"),
    "pozo": pygame.image.load(BASE_DIR / "assets" / "graphics" / "pozo.png"),
    "forest": pygame.image.load(BASE_DIR / "assets" / "graphics" / "forest.png"),

    "character": [
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_left.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_down.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_right.png"),
        pygame.image.load(BASE_DIR / "assets" / "graphics" / "elf_up.png"),
    ],
}

# Initializing the mixer
pygame.mixer.init()

# Loading music
pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "c_rides.ogg")

# Sound effects
SOUNDS = {
    "ice_cracking": pygame.mixer.Sound(
        BASE_DIR / "assets" / "sounds" / "ice_cracking.ogg"
    ),
    "water_splash": pygame.mixer.Sound(
        BASE_DIR / "assets" / "sounds" / "water_splash.ogg"
    ),
    "win": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "win.ogg"),
}
