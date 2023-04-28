import os
import pathlib

import pygame

# Allowing environment to have sounds
if "SDL_AUDIODRIVER" in os.environ:
    del os.environ["SDL_AUDIODRIVER"]

# Size of the square tiles used in this environment.
TILE_SIZE = 32

# Grid
ROWS = 10
COLS = 10

NUM_TILES = ROWS * COLS
NUM_ACTIONS = 4
INITIAL_STATE = 0

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
    "stool": pygame.image.load(BASE_DIR / "assets" / "graphics" / "stool.png"),
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
pygame.mixer.music.load(BASE_DIR / "assets" / "sounds" / "ice_village.ogg")

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
