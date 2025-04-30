import pygame
from os.path import join
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, FPS, BG_LAYER

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, position, image):
        super().__init__(groups)
        self._layer = BG_LAYER
        self.image = image
        self.rect = self.image.get_frect(topleft=position)
        self.ground = True

class CollitionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, position, image):
        super().__init__(groups)
        self._layer = BG_LAYER
        self.image = image
        self.rect = self.image.get_frect(topleft=position)

    def update(self, dt):
        pass