import pygame as pg
import sys
from settings import *
from map import Map
from player import Player
from enemy import Enemy


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT + MENU_HEIGHT))
        self.clock = pg.time.Clock()
        self.skull = pg.transform.scale(pg.image.load("assets/skull.png").convert_alpha(), (MENU_HEIGHT - WALL_SIZE * 2, MENU_HEIGHT - WALL_SIZE * 2))
        self.font = pg.font.Font("assets/dogicapixel.ttf", MENU_HEIGHT - WALL_SIZE * 2)
        self.font_title = pg.font.Font("assets/dogicapixel.ttf", TILE_SIZE * 2)
        self.font_small = pg.font.Font("assets/dogicapixel.ttf", TILE_SIZE // 3)
        self.distance = lambda pos1, pos2: (pos2[0] - pos1[0], pos2[1] - pos1[1])
        self.new_game()

    def new_game(self, pre=0):
        self.map = Map()
        self.player = Player(self)
        self.enemies = []
        self.time, self.prev_time, self.pre_time, self.enemy_delay = 0, 0, pre, START_DELAY
        self.score = 0

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif self.player.hp <= 0 and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.new_game(self.time)
            else:
                self.player.get_event(event)

    def update(self):
        self.player.update()
        if self.time - self.prev_time >= self.enemy_delay:
            self.enemies.append(Enemy(self))
            self.prev_time = self.time
            if self.enemy_delay >= 900:
                self.enemy_delay -= 5
        [enemy.update() for enemy in self.enemies]

        self.clock.tick(60)
        self.time = pg.time.get_ticks()
        if self.player.hp > 0:
            self.score = self.time - self.pre_time
        pg.display.set_caption(f'Osso duro: {self.clock.get_fps() :.1f} FPS')

    def draw(self):
        screen = self.screen

        screen.fill(BACKGROUND)
        if self.player.hp > 0:
            for pos in range(self.player.hp):
                x = WALL_SIZE + (self.skull.get_width() + WALL_SIZE) * pos
                screen.blit(self.skull, (x, WALL_SIZE))
            score = self.font.render(f"{(self.time - self.pre_time) / 1000 :.1f}", True, WHITE)
            score_rect = score.get_rect(center=(MENU_HEIGHT / 2, MENU_HEIGHT / 2))
            score_rect.right = WIDTH - WALL_SIZE
            screen.blit(score, score_rect)
            self.map.draw(screen)
            self.player.draw(screen)
            [enemy.draw(screen) for enemy in self.enemies]
            # pg.draw.rect(screen, pg.Color("Red"), self.player.rect, 1)
            # [pg.draw.rect(screen, pg.Color("Purple"), bullet.rect, 1) for bullet in self.player.bullets]
            # [pg.draw.rect(screen, pg.Color("Green"), enemy.rect, 1) for enemy in self.enemies]

        else:
            image = pg.transform.scale(self.skull, (30 / 100 * WIDTH, 30 / 100 * WIDTH))
            title_size = self.font_title.size("Game Over")
            score_size = self.font.size(f"Pontuação: {self.score / 1000 :.2f}")
            retry_size = self.font_small.size("Pressione espaço para tentar novamente")
            title_pos = (HEIGHT + MENU_HEIGHT) / 2 - title_size[1]
            score_pos = 85 / 100 * (HEIGHT + MENU_HEIGHT)

            screen.blit(image, ((WIDTH - image.get_width()) / 2, (title_pos - image.get_height()) / 2))
            screen.blit(self.font_title.render("Game Over", True, WHITE), ((WIDTH - title_size[0]) / 2, title_pos))
            screen.blit(self.font.render(f"Pontuação: {self.score / 1000 :.2f}", True, WHITE), ((WIDTH - score_size[0]) / 2, score_pos))
            screen.blit(self.font_small.render("Pressione espaço para tentar novamente", True, WHITE), ((WIDTH - retry_size[0]) / 2, score_pos + score_size[1] + 25))

    def run(self):
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    Game().run()
