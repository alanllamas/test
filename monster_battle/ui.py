import pygame
from config import *
class UI:
  def __init__(self, monster):
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(None, 32)
    self.left = SCREEN_WIDTH / 2 - 100
    self.right = SCREEN_HEIGHT / 2 + 50
    self.monster = monster

    self.general_options = ['attack', 'heal', 'switch', 'escape' ]
    self.general_index = { 'col': 0, 'row': 0 }
    self.state = 'general'

  def input(self):
    keys = pygame.key.get_just_pressed()
    self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))
    self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))
    if keys[pygame.K_SPACE]:
      self.state = self.general_options[self.general_index['col'] + self.general_index['row'] * 2]

  def general(self):
    rect = pygame.FRect(self.left + 40, self.right, 400, 200)
    pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
    pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)


    cols, rows = 2, 2
    for col in range(cols):
       for row in range(rows):
          x = rect.left + rect.width / 4 + (rect.width / 2) * col
          y = rect.top + rect.height / 4 + (rect.height / 2) * row
          
          i = col + 2 * row
          color = COLORS['gray'] if col == self.general_index['col'] and row == self.general_index['row'] else COLORS['black']

          text_surf = self.font.render(self.general_options[i], True, color)
          text_rect = text_surf.get_frect(center=(x,y))
          self.screen.blit(text_surf, text_rect)
          

  def update(self, dt):
    self.input()
  
  def draw(self):
    print(self.state)
    if self.state == 'general': self.general()
    if self.state == 'attack': self.general()
    if self.state == 'switch': self.general()
    if self.state == 'heal': self.general()
    if self.state == 'escape': self.general()