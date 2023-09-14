import pygame as pg
import math

from settings import *


class Bullet:
    def __init__(self, x, y, player):
        mx, my = pg.mouse.get_pos()
        dx, dy = mx - player.rect.centerx, my - player.rect.centery
        angle = math.atan2(dy, dx)
        bullet_angle = math.degrees(math.atan2(-dy, dx)) - 90

        self.image = pg.transform.rotate(pg.transform.scale(pg.image.load("assets/bullet.png").convert_alpha(), BULLET_SIZE), bullet_angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED
        self.angle = angle
        self.player = player

    def update(self):
        game = self.player.game
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery += math.sin(self.angle) * self.speed
        for enemy in game.enemies:
            if pg.Rect.colliderect(self.rect, enemy.rect):
                game.enemies.pop(game.enemies.index(enemy))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player:
    def __init__(self, game):
        self.game = game
        self.hp = 5
        self.direction = "right"
        self.bullets = []

        self.sprite = pg.image.load("assets/skeleton.png").convert_alpha()  # W: 128 H: 250
        self.image = pg.transform.scale(self.sprite, (64, 250 * 64 / 128))  # W: 128 H: 250
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.gun_sprite = pg.transform.scale(pg.image.load("assets/gun.png").convert_alpha(), (80, 10 * 80 / 30))
        self.gun_image = self.gun_sprite
        self.gun_rect = self.gun_image.get_rect(center=(self.rect.x, self.rect.y))

    def update(self):
        wall = WALL_SIZE * 1.5
        self.movement(pg.key.get_pressed(), self.rect)
        self.rotate_gun()
        for bullet in self.bullets:
            bullet_x, bullet_y = bullet.rect.center
            if bullet_x > WIDTH - wall or bullet_x < wall or bullet_y > HEIGHT + MENU_HEIGHT - wall or bullet_y < MENU_HEIGHT + wall:
                self.bullets.pop(self.bullets.index(bullet))
            else:
                bullet.update()

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.bullets.append(Bullet(self.gun_rect.centerx, self.gun_rect.centery, self))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.gun_image, self.gun_rect)
        for bullet in self.bullets:
            bullet.draw(screen)

    def rotate_gun(self):
        axi = 90 * self.rect.height / 100   # axi of gun rotation
        mx, my = pg.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 3
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        if distance == 0:
            distance = 0.1

        vx, vy = dx * axi / distance, dy * axi / distance  # makes the hypotenuse of a kind of scale
        self.distancia = (dx, dy)

        self.gun_image = pg.transform.rotate(self.gun_sprite, angle)
        self.gun_rect = self.gun_image.get_rect(center=(self.rect.centerx + vx, self.rect.centery + vy))
        self.change_direction(dx)
        # self.get_gun_pos(dx, dy)

    def movement(self, keys, pos):
        keys_pressed = 0
        dy, dx = 0, 0

        if keys[pg.K_w]:
            keys_pressed += 1
            dy -= PLAYER_SPEED

        if keys[pg.K_a]:
            keys_pressed += 1
            dx -= PLAYER_SPEED

        if keys[pg.K_s]:
            keys_pressed += 1
            dy += PLAYER_SPEED

        if keys[pg.K_d]:
            keys_pressed += 1
            dx += PLAYER_SPEED

        if keys_pressed == 2:  # trying correction (pythagoras)
            correction = 1 / math.sqrt(2)
            dx *= correction
            dy *= correction

        nx, ny = pos.x + dx, pos.y + dy  # new x, y
        if nx >= WALL_SIZE and nx + pos.width < WIDTH - WALL_SIZE:
            pos.x = nx
        if ny >= MENU_HEIGHT and ny + pos.height < HEIGHT + MENU_HEIGHT - WALL_SIZE:
            pos.y = ny

    def change_direction(self, dx):
        if dx <= 0 and self.direction != "left":
            self.gun_sprite = pg.transform.flip(self.gun_sprite, False, True)
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "left"
        elif dx > 0 and self.direction != "right":
            self.gun_sprite = pg.transform.flip(self.gun_sprite, False, True)
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "right"
