# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 12
# Video link: https://youtu.be/qnUVjACD3WM
# Platform Graphics
# Art from Kenney.nl

import pygame as pg
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load obstacles
        self.spritesheet1 = Spritesheet(path.join(img_dir, OBSTACLES))
        # load background
        self.spritesheet3 = Spritesheet(path.join(img_dir, BACKGROUND))
        # load player sprite
        self.spritesheet2 = Spritesheet(path.join(img_dir, PLAYER))


    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        

        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.obstacles = pg.sprite.Group()
        
        # Adding obstacles
        px = WIDTH//2 + random.randrange(1, WIDTH//4)
        while px < WIDTH:
            p = Obstacle(self, px)
            print(px)
            self.obstacles.add(p)
            self.all_sprites.add(p)
            px = p.rect.left + 150 
            if px < WIDTH:
                px = random.randrange(px, WIDTH)
            
        self.background = Background(self)
        self.all_sprites.add(self.background)
        self.background2 = Background(self,WIDTH)
        self.all_sprites.add(self.background2)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            if self.player.pos.y > HEIGHT - 115:
                self.player.pos.y = HEIGHT - 115
                self.player.vel.y = 0

        # create new obstacles
        for obs in self.obstacles:
            if obs.rect.left < -50:
                obs.kill()
                px = WIDTH + random.randrange(1, WIDTH//2)
                p = Obstacle(self, px)
                print(px)
                self.obstacles.add(p)
                self.all_sprites.add(p)

        if self.background.rect.right < 0:
            self.background.kill()
            # Swap background
            self.background = self.background2
            # New background
            self.background2 = Background(self,self.background.rect.left)
            # Adds to the group of sprites
            self.all_sprites.add(self.background2)



        # Die!
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        if hits:
            for sprite in self.all_sprites:
                sprite.kill()
            self.playing = False

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()