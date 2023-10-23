import pygame as pg
import sys
from settings import *
from map import Map
from player import Player
from enemy import Enemy

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT + MENU_HEIGHT)) # tela de exibição do jogo
        self.clock = pg.time.Clock() # relogio (pra contar os fps)
        self.skull = pg.transform.scale(pg.image.load("assets/skull.png").convert_alpha(), (MENU_HEIGHT - WALL_SIZE * 2, MENU_HEIGHT - WALL_SIZE * 2)) # Simbolo do HP, com o tamanho do menu 
        # fonte e seus tamanhos
        self.font = pg.font.Font("assets/dogicapixel.ttf", MENU_HEIGHT - WALL_SIZE * 2)
        self.font_title = pg.font.Font("assets/dogicapixel.ttf", TILE_SIZE * 2)
        self.font_small = pg.font.Font("assets/dogicapixel.ttf", TILE_SIZE // 3)
        self.distance = lambda pos1, pos2: (pos2[0] - pos1[0], pos2[1] - pos1[1]) # retorna a distancia entre 2 pontos (x,y)
        self.start = False # jogo iniciou ou nao
        self.image = pg.transform.scale(self.skull, (30 / 100 * WIDTH, 30 / 100 * WIDTH)) # imagem do menu inicial
        self.new_game(0, False)
        self.last_score = 0
        with open("score.txt", "r") as arquivo:
            self.last_score = int(arquivo.read()) # pega o score maximo
        
        # pg.mouse.set_visible(False)

    def new_game(self, pre=0, new=True): # cria um novo jogo, criando o mapa, jogador, inimigos e reseta variaveis relacionadas a tempo
        self.map = Map()
        self.player = Player(self)
        self.enemies = []
        self.time, self.prev_time, self.pre_time, self.enemy_delay = 0, 0, pre, START_DELAY
        self.score = 0

    def event_loop(self): # event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if not self.start and event.type == pg.KEYDOWN: # incia o jogo (se estiver na tela principal)
                self.score = 0
                self.time = 0
                self.pre_time = 0
                print(self.pre_time, self.time, self.score)
                self.start = True
            elif self.player.hp <= 0 and event.type == pg.KEYDOWN and event.key == pg.K_SPACE: # reseta o jogo (se o jogador perdeu)
                self.new_game(self.time)
            else:
                self.player.get_event(event) # passa o evento pro player
    def write_score(self): #escreve a pontuação no arquivo score.txt
        with open("score.txt", "w") as arquivo:
            if self.score > self.last_score: 
                arquivo.write(str(self.score))
                self.last_score = self.score
            else:
                arquivo.write(str(self.last_score))
    def update(self): # atualiza o jogador e adiciona os inimigos na tela
        if self.start:
            self.player.update()
            if self.time - self.prev_time >= self.enemy_delay:
                self.enemies.append(Enemy(self))
                self.prev_time = self.time
                if self.enemy_delay != 500:
                    self.enemy_delay -= 2
            [enemy.update() for enemy in self.enemies]

            self.time = pg.time.get_ticks()
            if self.player.hp > 0:
                self.score = self.time - self.pre_time
        self.clock.tick(60)
        pg.display.set_caption(f'Osso duro: {self.clock.get_fps() :.1f} FPS')

    def draw(self):
        screen = self.screen

        screen.fill(BACKGROUND)
        if not self.start: # desenha a tela inicial
            title_size = self.font_title.size("Osso Duro")
            score_size = self.font_small.size(f"Pontuação maxima: {self.last_score / 1000 :.2f}")
            retry_size = self.font_small.size("Pressione qualquer tecla para iniciar")
            title_pos = (HEIGHT + MENU_HEIGHT) / 2 - title_size[1]
            score_pos = 85 / 100 * (HEIGHT + MENU_HEIGHT)

            screen.blit(self.image, ((WIDTH - self.image.get_width()) / 2, (title_pos - self.image.get_height()) / 2))
            screen.blit(self.font_title.render("Osso Duro", True, WHITE), ((WIDTH - title_size[0]) / 2, title_pos))
            screen.blit(self.font_small.render(f"Pontuação maxima: {self.last_score / 1000 :.2f}", True, WHITE), ((WIDTH - score_size[0]) / 2, score_pos))
            screen.blit(self.font_small.render("Pressione qualquer tecla para iniciar", True, WHITE), ((WIDTH - retry_size[0]) / 2, score_pos + score_size[1] + 25))


        elif self.player.hp > 0: # desenha o jogo
            self.map.draw(screen)
            self.player.draw(screen)
            [enemy.draw(screen) for enemy in self.enemies]
            self.map.draw_borders(screen)
            # Top menu
            for pos in range(self.player.hp):
                x = WALL_SIZE + (self.skull.get_width() + WALL_SIZE) * pos
                screen.blit(self.skull, (x, WALL_SIZE))
            score = self.font.render(f"{(self.time - self.pre_time) / 1000 :.1f}", True, WHITE)
            score_rect = score.get_rect(center=(MENU_HEIGHT / 2, MENU_HEIGHT / 2))
            score_rect.right = WIDTH - WALL_SIZE
            screen.blit(score, score_rect)
            # pg.draw.rect(screen, pg.Color("Red"), self.player.rect, 1)
            # [pg.draw.rect(screen, pg.Color("Purple"), bullet.rect, 1) for bullet in self.player.bullets]
            # [pg.draw.rect(screen, pg.Color("Green"), enemy.rect, 1) for enemy in self.enemies]

        else: # desenha a tela de game over
            title_size = self.font_title.size("Game Over")
            score_size = self.font.size(f"Pontuação: {self.score / 1000 :.2f}")
            retry_size = self.font_small.size("Pressione espaço para tentar novamente")
            title_pos = (HEIGHT + MENU_HEIGHT) / 2 - title_size[1]
            score_pos = 85 / 100 * (HEIGHT + MENU_HEIGHT)

            screen.blit(self.image, ((WIDTH - self.image.get_width()) / 2, (title_pos - self.image.get_height()) / 2))
            screen.blit(self.font_title.render("Game Over", True, WHITE), ((WIDTH - title_size[0]) / 2, title_pos))
            screen.blit(self.font.render(f"Pontuação: {self.score / 1000 :.2f}", True, WHITE), ((WIDTH - score_size[0]) / 2, score_pos))
            screen.blit(self.font_small.render("Pressione espaço para tentar novamente", True, WHITE), ((WIDTH - retry_size[0]) / 2, score_pos + score_size[1] + 25))

    def run(self): # loop princial do pygame, constantemente checa eventos, atualiza o jogo e o desenha
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    Game().run()
