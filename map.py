import pygame as pg
import random
from settings import *

map_size = int(WIDTH / TILE_SIZE)
minimap = [[random.choices([random.randint(2, 3), random.randint(4, 6), random.randint(7, 9)], [0.35, 0.6, 0.05])[0] for _ in range(map_size)] for _ in range(map_size)]


class Map:
    def __init__(self):
        self.minimap = minimap
        self.world_map = {(i, j): value for i, row in enumerate(minimap) for j, value in enumerate(row)}
        self.tiles = [pg.transform.scale(pg.image.load(f"assets/map/ground{x}.png").convert(), (TILE_SIZE, TILE_SIZE)) for x in range(9)]
        self.wall = pg.transform.scale(pg.image.load("assets/map/ground0.png").convert(), (WALL_SIZE, WALL_SIZE))

    def draw(self, screen):
        # Drawn ground
        for pos in self.world_map:
            x, y = pos[1] * TILE_SIZE, MENU_HEIGHT + pos[0] * TILE_SIZE  # pos = (x, y)
            screen.blit(self.tiles[self.world_map[pos] - 1], (x, y))

    def draw_borders(self, screen):
        for i in range(0, map_size * WALL_DIFF):
            for j in range(0, map_size * WALL_DIFF):
                if i == 0 or i == map_size * WALL_DIFF - 1:
                    screen.blit(self.wall, (WALL_SIZE * i, MENU_HEIGHT + WALL_SIZE * j))
                elif j == map_size * WALL_DIFF - 1:
                    screen.blit(self.wall, (WALL_SIZE * i, MENU_HEIGHT + WALL_SIZE * j))
