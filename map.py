import pygame as pg
import random
from settings import *

map_width = WIDTH // TILE_SIZE
map_height = HEIGHT // TILE_SIZE
minimap = [[random.choices([random.randint(2, 3), random.randint(4, 6), random.randint(7, 9)], [0.35, 0.6, 0.05])[0] for _ in range(map_width)] for _ in range(map_height)]  # Use map_height instead of map_width here

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
        for x in range(0, map_width * WALL_DIFF):
            for y in range(0, map_height * WALL_DIFF):  # Use map_height here instead of map_width
                if x == 0 or x == map_width * WALL_DIFF - 1:
                    screen.blit(self.wall, (WALL_SIZE * x, MENU_HEIGHT + WALL_SIZE * y))
                elif y == map_height * WALL_DIFF - 1:  # Use map_height here instead of map_width
                    screen.blit(self.wall, (WALL_SIZE * x, HEIGHT + MENU_HEIGHT - WALL_SIZE))

