import pygame as pg
import random
from settings import *

map_size = int(WIDTH / TILE_SIZE)
minimap = []


def get_number():
    n = random.random()
    if n <= 0.4:
        return random.randint(2, 3)
    elif n >= 0.9:
        return random.randint(7, 9)
    else:
        return random.randint(4, 6)


for x in range(0, map_size):
    minimap.append([get_number() for i in range(0, map_size)])
print(minimap, "\n")


class Map:
    def __init__(self):
        self.minimap = minimap
        self.world_map = {}
        self.tiles = []
        self.wall = pg.transform.scale(pg.image.load("assets/map/ground0.png").convert(), (WALL_SIZE, WALL_SIZE))

        # Set map coordenates and values of tilesets
        for i, row in enumerate(self.minimap):
            for j, value in enumerate(row):
                self.world_map[(i, j)] = value
        # Replace ground value for image (For not to loses FPS with pg.transform.scale())
        for x in range(1, 10):
            self.tiles.append(pg.transform.scale(pg.image.load(f"assets/map/ground{x}.png").convert(), (TILE_SIZE, TILE_SIZE)))

    def draw(self, screen):
        # Drawn ground
        for pos in self.world_map:
            x, y = pos[1] * TILE_SIZE, MENU_HEIGHT + pos[0] * TILE_SIZE  # pos = (x, y)
            screen.blit(self.tiles[self.world_map[pos] - 1], (x, y))
        for i in range(0, map_size * WALL_DIFF):
            for j in range(0, map_size * WALL_DIFF):
                if i == 0 or i == map_size * WALL_DIFF - 1:
                    screen.blit(self.wall, (WALL_SIZE * i, MENU_HEIGHT + WALL_SIZE * j))
                elif j == map_size * WALL_DIFF - 1:
                    screen.blit(self.wall, (WALL_SIZE * i, MENU_HEIGHT + WALL_SIZE * j))
