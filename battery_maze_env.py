import numpy as np
import time
import gym
import pygame
import settings
from tilemap import TileMap
from KruskalMazeGenerator import KruskalMazeGenerator


class RobotMazeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.action_space = gym.spaces.Discrete(settings.NUM_ACTIONS)
        self.observation_space = gym.spaces.Discrete(settings.NUM_TILES)
        self.maze = KruskalMazeGenerator(settings.ROWS, settings.COLS)
        self.initial_state = self.maze.entrance_index
        self.finish_state = self.maze.exit_index
        self.total_tiles = self.maze.num_rows * self.maze.num_cols
        self.keys_counter = 0
        self.total_keys = len(settings.REWARD_POSITION)
        self.rewards = self.maze.chests
        self.trees = [6, 14, 29, 35, 47,49, 69, 82, 85, 97]
        self.tree_p = [30, 65]
        self.wood = [40, 42, 54, 55, 56, 57]
        self.P = {current_state: {action: [] for action in range(
            settings.NUM_ACTIONS)} for current_state in range(self.total_tiles) if (self.__is_valid_state(current_state))}
        self.__build_P()
        self.VIRTUAL_WIDTH = settings.TILE_SIZE * self.maze.num_cols
        self.VIRTUAL_HEIGHT = settings.TILE_SIZE * self.maze.num_rows
        self.WINDOW_WIDTH = self.VIRTUAL_WIDTH * settings.H_SCALE
        self.WINDOW_HEIGHT = self.VIRTUAL_HEIGHT * settings.V_SCALE
        self.delay = settings.DEFAULT_DELAY

        if self.render_mode is not None:
            self.init_render_mode(self.render_mode)

        self.render_character = True
        self.render_goal = True
        self.tilemap = None
        self.__build_tilemap()
        self.reset()

    def init_render_mode(self, render_mode):
        self.render_mode = render_mode

        pygame.init()
        pygame.display.init()
        pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (self.VIRTUAL_WIDTH, self.VIRTUAL_HEIGHT)
        )
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("TreasureTrail-v1")

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if options is not None:
            if not isinstance(options, dict):
                raise RuntimeError("Variable options is not a dictionary")
            self.delay = options.get('delay', 0.5)

        self.current_state, self.current_action, self.current_reward, self.keys_counter = self.initial_state, 1, 0.0, 0
        self.rewards = settings.REWARD_POSITION
        self.maze.chests = [43, 75, 89]
        self.render_character, self.render_goal = True, True

        for tile in self.tilemap.tiles:
            tile.texture_name = "hole" if tile.texture_name == "cracked_hole" else tile.texture_name

        return self.current_state, {}

    def step(self, action):
        probability, next_state, reward, terminated = self.P[self.current_state][action][0]
        state_aux = self.current_state
        self.current_state, self.current_action = next_state, action

        if (self.check_chest_exists(next_state)):
            terminated = False
            self.maze.chests.remove(next_state)
            self.__build_P()
            self.keys_counter += 1
        if self.keys_counter == self.total_keys:
            terminated = True
            self.P[state_aux][action][0] = (
                probability, next_state, 1.0, terminated)

        if (self.render_mode is not None):
            if next_state == 43 or next_state == 75 or next_state == 89:
                settings.SOUNDS["winner"].play()
                self.tilemap.tiles[next_state].texture_name = "ice"
                self.render_surface.blit(
                    settings.TEXTURES["ice"],
                    (self.tilemap.tiles[next_state].x,
                     self.tilemap.tiles[next_state].y),
                )

            if terminated:
                if next_state == self.finish_state or self.keys_counter == self.total_keys:
                    self.render_goal = False
                    settings.SOUNDS["win"].play()
                else:
                    self.tilemap.tiles[next_state].texture_name = "cracked_hole"
                    self.render_character = False
                    settings.SOUNDS["winner"].play()
            self.render()
            time.sleep(self.delay)

        return next_state, reward, terminated, False, {}

    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        self.render_trees()
        self.render_wood()
        self.render_tree_p()

        self.render_surface.blit(
            settings.TEXTURES["stool"],
            (self.tilemap.tiles[self.initial_state].x,
             self.tilemap.tiles[self.initial_state].y),
        )

        self.render_goals()

        if self.render_goal:
            self.render_surface.blit(
                settings.TEXTURES["goal"],
                (
                    self.tilemap.tiles[self.finish_state].x,
                    self.tilemap.tiles[self.finish_state].y,
                ),
            )

        if self.render_character:
            self.render_surface.blit(
                settings.TEXTURES["character"][self.current_action],
                (self.tilemap.tiles[self.current_state].x,
                 self.tilemap.tiles[self.current_state].y),
            )

        #self.__render_walls()

        self.screen.blit(
            pygame.transform.scale(self.render_surface,
                                   self.screen.get_size()), (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()

    def check_wall_exists(self, current_state, next_state):
        return (current_state, next_state) in self.maze.walls

    def check_chest_exists(self, index):
        return index in self.maze.chests

    def check_hole_exists(self, state):
        return state in self.maze.holes

    def __build_transition(self, action, current_state):
        col, row = self.maze.compute_coordinates(current_state)
        if (action == 0):
            next_state = self.maze.compute_index(
                col - 1, row) if (col > 0) else current_state
            next_state = current_state if (self.check_wall_exists(
                current_state, next_state)) else next_state
        elif (action == 1):
            next_state = self.maze.compute_index(
                col, row + 1) if (row < settings.ROWS - 1) else current_state
            next_state = current_state if (self.check_wall_exists(
                current_state, next_state)) else next_state
        elif (action == 2):
            next_state = self.maze.compute_index(
                col + 1, row) if (col < settings.COLS - 1) else current_state
            next_state = current_state if (self.check_wall_exists(
                current_state, next_state)) else next_state
        else:
            next_state = self.maze.compute_index(
                col, row - 1) if (row > 0) else current_state
            next_state = current_state if (self.check_wall_exists(
                current_state, next_state)) else next_state
        probability = 1

        hole_exists = self.check_hole_exists(next_state)
        chest_exists = self.check_chest_exists(next_state)

        if hole_exists:
            self.P[current_state][action] = [
                (probability, next_state, 0.0, True)]
            return
        elif (chest_exists):
            self.P[current_state][action] = [
                (probability, next_state, 1.0, False)]
            return
        else:
            self.P[current_state][action] = [
                (probability, next_state, 0.0, False)]
            return

    def __build_P(self):
        for row in range(self.maze.num_rows):
            for col in range(self.maze.num_cols):
                current_state = self.maze.compute_index(col, row)
                if current_state in self.maze.holes:
                    continue
                for action in range(settings.NUM_ACTIONS):
                    self.__build_transition(action, current_state)

    def __build_tilemap(self) -> None:
        tile_texture_names = ["ice"] * self.total_tiles

        for possibilities in self.P.values():
            for state, reward, terminated in (possibility[0][1:] for possibility in possibilities.values()):
                if terminated:
                    tile_texture_names[state] = "hole" if reward <= 0 else "ice"
                # elif (state in self.rewards):
                    # tile_texture_names[state] = "reco"

        tile_texture_names[self.finish_state] = "ice"
        self.tilemap = TileMap(
            self.maze.num_rows, self.maze.num_cols, tile_texture_names)


    def __is_valid_state(self, state):
        return state not in self.maze.holes

    def __check_if_chest_is_open(self, index):
        for chest in self.maze.chests:
            if chest[1]:
                return True
        return False

    def render_goals(self):
        for reward in self.maze.chests:
            if (reward == self.finish_state):
                continue
            self.render_surface.blit(
                settings.TEXTURES["diamon"],
                (self.tilemap.tiles[reward].x,
                 self.tilemap.tiles[reward].y),
            )

    def render_trees(self):
        for tree in self.trees:
            self.render_surface.blit(
                settings.TEXTURES["Arbol"],
                (self.tilemap.tiles[tree].x,
                 self.tilemap.tiles[tree].y),
            )

    def render_wood(self):
        for wood in self.wood:
            self.render_surface.blit(
                settings.TEXTURES["wood"],
                (self.tilemap.tiles[wood].x,
                 self.tilemap.tiles[wood].y),
        )
    
    def render_tree_p(self):
        for tree_p in self.tree_p:    
            self.render_surface.blit(
                settings.TEXTURES["forest"],
                (self.tilemap.tiles[tree_p].x,
                self.tilemap.tiles[tree_p].y),
        )
           
    def __render_walls(self):
        for tile in range(self.total_tiles):
            col, row = self.maze.compute_coordinates(tile)
            bottom_wall_exists = (
                tile, tile + self.maze.num_cols) in self.maze.walls
            right_wall_exists = (tile, tile + 1) in self.maze.walls
            x, y = col * settings.TILE_SIZE, row * settings.TILE_SIZE

            if bottom_wall_exists:
                start_pos = (x, y + settings.TILE_SIZE)
                end_pos = (x + settings.TILE_SIZE, y + settings.TILE_SIZE)
                pygame.draw.line(self.render_surface, pygame.Color(
                    34, 139, 34), start_pos, end_pos)
            if right_wall_exists:
                start_pos = (x + settings.TILE_SIZE, y)
                end_pos = (x + settings.TILE_SIZE, y + settings.TILE_SIZE)
                pygame.draw.line(self.render_surface, pygame.Color(
                    34, 139, 34), start_pos, end_pos)
            
