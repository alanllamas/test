import pygame
import math
import random
from config import *

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.y_change = 0
        self.x_change = 0

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.move()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.y_change = 0
        self.x_change = 0
    
    def move (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.x_change += MOVE_SPEED
        if keys[pygame.K_UP]:
            self.y_change -= MOVE_SPEED
        if keys[pygame.K_DOWN]:
            self.y_change += MOVE_SPEED
        
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self._layer = TILE_MAP_LAYER
        self.groups = game.all_sprites, game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y