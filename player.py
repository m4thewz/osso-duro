import pygame as pg
import math

from settings import *


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, player):
        pg.sprite.Sprite.__init__(self)
        dx, dy = player.game.distance(player.rect.center, pg.mouse.get_pos())
        bullet_angle = math.degrees(math.atan2(-dy, dx)) - 90

        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load("assets/bullet.png").convert_alpha(), BULLET_SIZE), bullet_angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.speed = BULLET_SPEED
        self.angle = math.atan2(dy, dx)
        self.player = player
        self.group = pg.sprite.Group()
        self.group.add(self)


    def update(self):
        game = self.player.game
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery += math.sin(self.angle) * self.speed
        for enemy in game.enemies:
            if pg.sprite.spritecollide(self, enemy.group, False, pg.sprite.collide_mask):
                game.enemies.pop(game.enemies.index(enemy))


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.hp = 5
        self.direction = 1  # 0: Left, 1: Right
        self.bullets = []

        self.sprite = pg.image.load("assets/skeleton.png").convert_alpha()  # W: 128 H: 250
        self.gun_sprite = pg.transform.scale(pg.image.load("assets/gun.png").convert_alpha(), (80, 10 * 80 / 30))
        self.image = pg.transform.scale(self.sprite, (64, 250 * 64 / 128))  # W: 128 H: 250
        self.gun_image = self.gun_sprite
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.gun_rect = self.gun_image.get_rect(center=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.image)
        self.group = pg.sprite.Group()
        self.group.add(self)


    def update(self):
        wall = WALL_SIZE * 1.5
        self.movement(pg.key.get_pressed(), self.rect)
        self.rotate_gun()
        for bullet in self.bullets:
            bx, by = bullet.rect.center
            if bx > WIDTH - wall or bx < wall or by > HEIGHT + MENU_HEIGHT - wall or by < MENU_HEIGHT + wall:
                self.bullets.pop(self.bullets.index(bullet))
            else:
                bullet.update()

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.bullets.append(Bullet(self.gun_rect.centerx, self.gun_rect.centery, self))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.gun_image, self.gun_rect)
        [screen.blit(bullet.image, bullet.rect) for bullet in self.bullets]

    def rotate_gun(self):
        axi = 90 * self.rect.height / 100   # axi of gun rotation
        dx, dy = self.game.distance(self.rect.center, pg.mouse.get_pos())
        distance = math.hypot(dx, dy)
        vx, vy = dx * axi / distance, dy * axi / distance  # makes the hypotenuse of a kind of scale
        angle = math.degrees(math.atan2(-dy, dx)) - 3

        self.gun_image = pg.transform.rotate(self.gun_sprite, angle)
        self.gun_rect = self.gun_image.get_rect(center=(self.rect.centerx + vx, self.rect.centery + vy))
        self.change_direction(dx)

    def movement(self, keys, pos):
        keys_pressed = 0
        dy, dx = 0, 0
        directions = [(pg.K_w, pg.K_UP, 0, -1), (pg.K_a, pg.K_LEFT, -1, 0), (pg.K_s, pg.K_DOWN, 0, 1), (pg.K_d, pg.K_RIGHT, 1, 0)]

        for key, direction_key, x, y in directions:
            if keys[key] or keys[direction_key]:
                keys_pressed += 1
                dx += x * PLAYER_SPEED
                dy += y * PLAYER_SPEED

        if keys_pressed == 2:  # trying correction in diagonal movement (pythagoras)
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)

        nx, ny = pos.x + dx, pos.y + dy  # new x, y
        # disable player to move to walls
        if nx >= WALL_SIZE and nx + pos.width < WIDTH - WALL_SIZE:
            pos.x = nx
        if ny >= MENU_HEIGHT and ny + pos.height < HEIGHT + MENU_HEIGHT - WALL_SIZE:
            pos.y = ny

    def change_direction(self, dx):
        if dx <= 0 and self.direction != 0 or dx > 0 and self.direction != 1:
            self.gun_sprite = pg.transform.flip(self.gun_sprite, False, True)
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = dx > 0
