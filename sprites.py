# Sprite classes for platform game
import pygame as pg
from settings import *
from random import choice
vec = pg.math.Vector2

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height,scaler=0.5):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (int(width*scaler), int(height*scaler)))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (60, HEIGHT - 115)
        self.pos = vec(60, HEIGHT - 115)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet2.get_image(0, 236, 215, 210),
                                self.game.spritesheet2.get_image(340, 0, 215, 210)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet2.get_image(340, 472, 215, 210),
                              self.game.spritesheet2.get_image(0, 472, 215, 210)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet2.get_image(340, 236, 215, 210)
        self.jump_frame.set_colorkey(BLACK)


    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 10
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 10
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        #self.pos += self.vel + 0.5 * self.acc
        
        # Updates y position of player
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.midbottom = self.pos

        # Moves the platforms in reverse of the player
        for plat in self.game.platforms:
            plat.rect.x -= (self.vel.x + 0.5 * self.acc.x)
        # Move background
        #self.game.background.rect.x -= (self.vel.x + 0.5 * self.acc.x)
        
        #self.game.right_platform-= (self.vel.x + 0.5 * self.acc.x)

        
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        sc = 1.2
        images = [self.game.spritesheet.get_image(0, 0, 315, 90,sc)]
                  #self.game.spritesheet.get_image(0, 95, 315, 90,sc)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Background(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        sc = 6/9
        self.image = self.game.spritesheet3.get_image(0, 0, 1920, 1080,sc)
                  #self.game.spritesheet.get_image(0, 95, 315, 90,sc)]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()