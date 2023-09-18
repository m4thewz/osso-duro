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
        self.walk_sprites = [pg.transform.scale(pg.image.load(f"assets/ghost/walk/{x}.png"), (TILE_SIZE * 2, TILE_SIZE * 2)) for x in [0,1]]
        self.dead_sprites = [pg.transform.scale(pg.image.load(f"assets/ghost/dead/{x}.png"), (TILE_SIZE * 2, TILE_SIZE * 2)) for x in range(4)]
        self.current_sprite = 0
        self.image = self.walk_sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=(x,y))
        self.group = pg.sprite.Group()
        self.mask = pg.mask.from_surface(self.image)
        self.direction = 0
        self.group.add(self)

        self.time = pg.time.get_ticks()
        self.prev = 0
        self.state = "walking"
        

    def update(self):
        if self.state not in ["dying", "attack"]:
            player = self.game.player
            dx, dy = self.game.distance(self.rect.center, player.rect.center)
            distance = hypot(dx, dy)
            if pg.sprite.spritecollide(self, self.game.player.group, False, pg.sprite.collide_mask):
                self.current_sprite = 0
                self.state = "attack"
            if dx <= 0 and self.direction != 0 or dx > 0 and self.direction != 1:
                self.image = pg.transform.flip(self.image, True, False)
                self.walk_sprites = [pg.transform.flip(image, True, False) for image in self.walk_sprites]
                self.dead_sprites = [pg.transform.flip(image, True, False) for image in self.dead_sprites]
                self.direction = dx > 0
            self.time = pg.time.get_ticks()
            if distance > 0:
                self.rect.x += dx * self.speed / distance
                self.rect.y += dy * self.speed / distance

        if self.state == "walking":
            if self.time - self.prev >= self.speed * 50:
                self.current_sprite = not self.current_sprite
                self.image = self.walk_sprites[self.current_sprite]
                self.prev = self.time
        elif self.state == "attack":
            if self.time - self.prev >= 30:
                self.image = self.dead_sprites[self.current_sprite]
                self.current_sprite += 1
                if self.current_sprite > 3:
                    self.game.player.hp -= 1
                    self.game.enemies.pop(self.game.enemies.index(self))
                self.prev = self.time
            self.time = pg.time.get_ticks()
        elif self.state == "dying":
            if self.time - self.prev >= 50:
                self.image = self.dead_sprites[self.current_sprite]
                self.current_sprite += 1
                if self.current_sprite > 3:
                    self.game.enemies.pop(self.game.enemies.index(self))
                self.prev = self.time
            self.time = pg.time.get_ticks()
            

    def draw(self, screen):
        screen.blit(self.image, self.rect)
