import pygame as pg
from settings import *
import math
from random import randint, sample


class Enemy:
    def __init__(self, game):
        self.game = game
        self.image = pg.transform.scale(pg.image.load("assets/ghost.png").convert_alpha(), (TILE_SIZE * 2, TILE_SIZE * 2))
        self.rect = self.image.get_rect(center=(sample([0, WIDTH], 1)[0], randint(MENU_HEIGHT, MENU_HEIGHT + HEIGHT)))
        self.direction = "right"

    def update(self):
        player = self.game.player
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance <= self.game.player.rect.width:
            distance = 0.1
            player.hp -= 1
        self.rect.x += dx * ENEMY_SPEED / distance
        self.rect.y += dy * ENEMY_SPEED / distance
        if dx < 0 and self.direction != "right":
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "right"
        if dx > 0 and self.direction != "left":
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "left"

    def draw(self, screen):
        screen.blit(self.image, self.rect)
