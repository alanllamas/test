import pygame
from config import *
from random import sample

class Creature:
  def get_data(self, name):
    self.element = MONSTER_DATA[name]['element']
    self._health = self.max_health = MONSTER_DATA[name]['health']
    self.abilities = sample(list(ABILITIES_DATA.keys()), 4)
    self.name = name

    print(
      self.element,
      self.health,
      self.name,
      self.abilities,
    )
  @property
  def health(self):
    return self._health
  
  @health.setter
  def health(self, value):
    self._health = min(self.max_health, max(0, value))


class Monster(pygame.sprite.Sprite, Creature):
  def __init__(self, name, back, simple):
    super().__init__()
    self.image = back
    self.simple = simple
    self.rect = self.image.get_frect(bottomleft = (100, SCREEN_HEIGHT))
    self.get_data(name)

  def __repr__(self):
    return f'{self.name}: {self.health}/{self.max_health}'
  def update(self, dt):
    pass

class Opponent(pygame.sprite.Sprite, Creature):
  def __init__(self, name, surf, groups):
    super().__init__(groups)
    self.image = surf
    self.rect = self.image.get_frect(midbottom = (SCREEN_WIDTH - 250, 300))
    self.get_data(name)

  def update(self, dt):
    pass