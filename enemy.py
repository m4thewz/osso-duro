import pygame as pg
from settings import *
from math import hypot
from random import randint, uniform, random


class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        x, y = 0, 0
        if random() < 0.5:
            x = randint(0,WIDTH)
            y = MENU_HEIGHT if random() < 0.5 else MENU_HEIGHT + HEIGHT
        else:
            x = 0 if random() < 0.5 else WIDTH
            y = randint(MENU_HEIGHT, MENU_HEIGHT + HEIGHT)
        max_speed = ENEMY_SPEED * 1.5 if random() < 0.1 else ENEMY_SPEED * 2.5
        self.speed = round(uniform(ENEMY_SPEED,max_speed), 2)

        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.transform.scale(pg.image.load("assets/ghost.png").convert_alpha(), (TILE_SIZE * 2, TILE_SIZE * 2))
        self.rect = self.image.get_rect(center=(x,y))
        self.group = pg.sprite.Group()
        self.mask = pg.mask.from_surface(self.image)
        self.direction = 0
        self.group.add(self)

    def update(self):
        player = self.game.player
        dx, dy = self.game.distance(self.rect.center, player.rect.center)
        distance = hypot(dx, dy)
        if pg.sprite.spritecollide(self, self.game.player.group, False, pg.sprite.collide_mask):
            player.hp -= 1
            self.game.enemies.pop(self.game.enemies.index(self))
        if dx <= 0 and self.direction != 0 or dx > 0 and self.direction != 1:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = dx > 0
        self.rect.x += dx * self.speed / distance
        self.rect.y += dy * self.speed / distance

    def draw(self, screen):
        screen.blit(self.image, self.rect)
