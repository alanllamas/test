import pygame
from config import *
from utils import *
from timers import *
from sprites import *
from random import *
from ui import *


class Game:
  def __init__(self):
    self.setup()
  
  def setup(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Monster Battle')
    self.running = True
    self.clock = pygame.time.Clock()
    self.create_groups()
    self.load_assets()
    player_monster_list = ['Ivieron', 'Gulfin', 'Atrox']
    self.player_monsters =[ Monster(name, self.back_sprites[name]) for name in player_monster_list]
    self.monster = self.player_monsters[1]
    self.ui = UI(self.monster)

    monster_choice = choice(list(MONSTER_DATA.keys()))
    self.opponent_monster = Opponent(monster_choice, self.front_sprites[monster_choice], self.opponent_sprites)
    self.all_sprites.add(self.monster, self.opponent_monster)
  def update(self, dt):
    self.all_sprites.update(dt)
    self.ui.update(dt)
    pygame.display.update()
    self.screen.blit(self.bg_surfs['bg'],(0,0))

  def draw(self):
     self.ui.draw()
     self.draw_monster_floor()
     self.all_sprites.draw(self.screen)

  def draw_monster_floor(self):
    for sprite in self.all_sprites:
       floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
       self.screen.blit(self.bg_surfs['floor'], floor_rect)

  def create_groups(self):
    self.all_sprites = pygame.sprite.Group()
    self.opponent_sprites = pygame.sprite.Group()
  
  def load_assets(self):
    self.back_sprites = import_folder('assets', 'images', 'back')
    self.front_sprites = import_folder('assets', 'images', 'front')
    self.simple_sprites = import_folder('assets', 'images', 'simple')
    self.bg_surfs = import_folder('assets', 'images', 'other')
    print(self.back_sprites)
  
  def run(self):
    dt = self.clock.tick(FPS) / 1000
    while self.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.update(dt)
        self.draw()
    
    pygame.quit()