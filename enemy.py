import pygame as pg
from settings import *
import math
from random import randint, sample


class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(pg.image.load("assets/ghost.png").convert_alpha(), (TILE_SIZE * 2, TILE_SIZE * 2))
        self.rect = self.image.get_rect(center=(sample([0, WIDTH], 1)[0], randint(MENU_HEIGHT, MENU_HEIGHT + HEIGHT)))
        self.group = pg.sprite.Group()
        self.mask = pg.mask.from_surface(self.image)
        self.direction = 0
        self.group.add(self)

    def update(self):
        player = self.game.player
        dx, dy = self.game.distance(self.rect.center, player.rect.center)
        distance = math.hypot(dx, dy)
        if pg.sprite.spritecollide(self, self.game.player.group, False, pg.sprite.collide_mask):
            player.hp -= 1
            self.game.enemies.pop(self.game.enemies.index(self))
        if dx <= 0 and self.direction != 0 or dx > 0 and self.direction != 1:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = dx > 0
        self.rect.x += dx * ENEMY_SPEED / distance
        self.rect.y += dy * ENEMY_SPEED / distance

    def draw(self, screen):
        screen.blit(self.image, self.rect)
