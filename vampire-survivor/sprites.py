import pygame
from os.path import join
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, FPS, BG_LAYER

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, size, position):
        super().__init__(groups)
        self._layer = BG_LAYER
        self.image = pygame.surface.Surface(size)
        self.image.fill("blue")
        self.rect = self.image.get_frect(center=position)

    def update(self, dt):
        pass