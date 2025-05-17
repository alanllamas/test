from config import *
import pygame

class AttackAnimationSprite(pygame.sprite.Sprite):
  def __init__(self, target, frames, groups):
    super().__init__(groups)
    self.frames = frames
    self.frame_index = 0
    self.image = self.frames[self.frame_index]
    self.rect = self.image.get_frect(center = target.rect.center)

  def update(self, dt):
    self.frame_index += .3 * dt
    if self.frame_index < len(self.frames):
      self.image = self.frames[int(self.frame_index)]
    else:
      self.kill()