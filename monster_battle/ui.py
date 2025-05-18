import pygame
from config import *
class UI:
  def __init__(self, monster, player_monsters, get_input):
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(None, 32)
    self.left = SCREEN_WIDTH / 2 - 100
    self.top = SCREEN_HEIGHT / 2 + 50
    self.monster = monster
    self.player_monsters = player_monsters
    self.available_monsters = [ monster for monster in self.player_monsters if monster != self.monster and monster.health > 0 ]
    self.visible_monsters = 4
    self.get_input = get_input
    self.general_options = ['attack', 'heal', 'switch', 'escape']
    self.general_index = { 'col': 0, 'row': 0 }
    
    self.attack_options =  ['scratch', 'nuke', 'shards', 'spiral']
    self.attack_index = { 'col': 0, 'row': 0 }

    self.switch_index = 0

    self.state = 'general'
    self.rows = 2
    self.cols = 2

  def input(self):
    keys = pygame.key.get_just_pressed()

    if self.state == 'general': 
      self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % self.rows
      self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % self.cols
      if keys[pygame.K_SPACE]:
        self.state = self.general_options[self.general_index['col'] + self.general_index['row'] * 2]

    elif self.state == 'attack': 
      self.attack_index['row'] = (self.attack_index['row'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % self.rows
      self.attack_index['col'] = (self.attack_index['col'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % self.cols
      if keys[pygame.K_SPACE]:
        self.get_input(self.state, self.monster.abilities[self.attack_index['col'] + self.attack_index['row'] * 2])
        self.state = 'general'

    elif self.state == 'switch': 
      if self.available_monsters:
        self.switch_index = (self.switch_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.available_monsters)
        if keys[pygame.K_SPACE]:
          self.get_input(self.state, self.available_monsters[self.switch_index])
          self.state = 'general'
          # self.state = self.general_options[self.general_index['col'] + self.general_index['row'] * self.player_monsters]
    elif self.state == 'heal':
        self.get_input('heal', self.monster)
        self.state = 'general'

    elif self.state == 'escape':
      self.get_input('escape')

    if keys[pygame.K_ESCAPE]:
      self.state = 'general'
      self.general_index = { 'col': 0, 'row': 0 }
      self.attack_index = { 'col': 0, 'row': 0 }
      self.switch_index = 0
  
  def generate_menu(self, cols, rows, index, options):
    rect = pygame.FRect(self.left + 40, self.top, 400, 200)
    pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
    pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

    for col in range(cols):
      for row in range(rows):
          x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
          y = rect.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
          
          i = col + 2 * row
          color = COLORS['gray'] if col == index['col'] and row == index['row'] else COLORS['black']

          text_surf = self.font.render(options[i], True, color)
          text_rect = text_surf.get_frect(center=(x,y))
          self.screen.blit(text_surf, text_rect)

  def switch(self):
    rect = pygame.FRect(self.left + 40, self.top - 300, 400, 400)
    pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
    pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

    v_offset = 0 if self.switch_index <= self.visible_monsters else -(self.switch_index - self.visible_monsters + 1) * rect.height / self.visible_monsters

    for i in range(len(self.available_monsters)):  
      # print(i)
      x = rect.centerx
      y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset
      color = COLORS['gray'] if i == self.switch_index else COLORS['black']
      # color = COLORS['black']

      name = self.available_monsters[i].name
      simple_surf = self.available_monsters[i].simple
      simple_rect = simple_surf.get_frect(center=(x - 100,y)) 
      text_surf = self.font.render(name, True, color)
      text_rect = text_surf.get_frect(center=(x,y)) 
      if rect.collidepoint(text_rect.center):
        self.screen.blit(text_surf, text_rect)
        self.screen.blit(simple_surf, simple_rect)

  def stats(self):
    rect = pygame.FRect(self.left, self.top + -60, 250, 80)
    pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
    pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

    name_surf = self.font.render(self.monster.name, True, COLORS['black'])
    name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))
    self.screen.blit(name_surf, name_rect)

    health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
    pygame.draw.rect(self.screen, COLORS['gray'], health_rect)
    self.draw_bar(health_rect, self.monster.health, self.monster.max_health)

  def general(self):
    self.generate_menu(self.cols ,self.rows , self.general_index, self.general_options)
          
  def attack(self):
    self.generate_menu(self.cols ,self.rows , self.attack_index, self.monster.abilities)
          
  def draw_bar(self, rect, value, max_value):
    ratio = rect.width / max_value
    progress_rect = pygame.FRect(rect.topleft, (value * ratio, rect.height))
    pygame.draw.rect(self.screen, COLORS['red'], progress_rect)

  def update(self, dt):
    self.input()
    self.available_monsters = [monster for monster in self.player_monsters if monster  != self.monster and monster.health > 0]
  
  def update_stats(self):
    self.stats()
  
  def draw(self):
    # print(self.state)
    if self.state == 'general': self.general()
    if self.state == 'attack': self.attack()
    if self.state == 'switch': self.switch()
    # if self.state == 'heal': self.general()
    # if self.state == 'escape': self.general()

class OpponentUi:
  def __init__(self, monster):
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(None, 32)
    self.monster = monster
  
  def draw(self):
    rect = pygame.FRect((0,0), (250, 80)).move_to(midleft = (500, self.monster.rect.centery))
    pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
    pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

    name_surf = self.font.render(self.monster.name, True, COLORS['black'])
    name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))
    self.screen.blit(name_surf, name_rect)

    health_rect = pygame.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
    pygame.draw.rect(self.screen, COLORS['gray'], health_rect)
    self.draw_bar(health_rect, self.monster.health, self.monster.max_health)

  def draw_bar(self, rect, value, max_value):
    ratio = rect.width / max_value
    progress_rect = pygame.FRect(rect.topleft, (value * ratio, rect.height))
    pygame.draw.rect(self.screen, COLORS['red'], progress_rect)