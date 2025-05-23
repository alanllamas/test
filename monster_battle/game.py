import pygame
from config import *
from utils import *
from timers import *
from sprites import *
from random import *
from ui import *
from attack import AttackAnimationSprite

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

    player_monster_list = ['Ivieron', 'Gulfin', 'Atrox', 'Friolera', 'Cindrill', 'Pluma']
    # player_monster_list = ['Pluma']
    self.player_monsters = [ Monster(name, self.back_sprites[name], self.simple_sprites[name]) for name in player_monster_list]
    self.monster = self.player_monsters[0]
    monster_choice = choice(list(MONSTER_DATA.keys()))
    self.opponent_monster = Opponent(monster_choice, self.front_sprites[monster_choice], self.opponent_sprites)
    self.ui = UI(self.monster, self.player_monsters, self.get_input)
    self.OpponentUi = OpponentUi(self.opponent_monster)
    self.player_active = True
    self.audio['music'].play(-1)


    self.timers = {
       'player_end': Timer(1000, func= self.opponent_turn),
       'opponent_end': Timer(1000, func= self.player_turn)
    }

    self.all_sprites.add(self.monster, self.opponent_monster)

  def update(self, dt):
    self.all_sprites.update(dt)
    self.update_timers()
    if self.player_active:
      self.ui.update(dt)
    self.ui.update_stats()
    pygame.display.update()
    self.screen.blit(self.bg_surfs['bg'],(0,0))

  def update_timers(self):
    for timer in self.timers.values():
       timer.update()

  def opponent_turn(self):
    if self.opponent_monster.health <= 0:
      self.player_active = True
      self.opponent_monster.kill()
      monster_name = choice(list(MONSTER_DATA.keys()))
      self.opponent_monster = Opponent(monster_name, self.front_sprites[monster_name], self.all_sprites)
      self.OpponentUi.monster = self.opponent_monster
    else: 
      # print('opponent turn')
      attack = choice(self.opponent_monster.abilities)
      self.apply_attack(self.monster, attack)
      self.timers['opponent_end'].activate()

  def player_turn(self):
    self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and not monster.health <= 0]

    self.player_active = True
    if self.monster.health <= 0:
      if self.available_monsters.__len__() <= 0:
        self.running = False
      else:
        self.player_active = False
        self.monster.kill()
        monster = choice(self.available_monsters)
        # monster_name = monster
        print('monster.name: ', monster.name)
        self.monster = monster
        self.ui.monster = self.monster
        self.all_sprites.add(self.monster)
        # self.screen.blit(self.monster, (100, SCREEN_HEIGHT))
        self.timers['player_end'].activate()


  def draw(self):
     self.draw_monster_floor()
     self.all_sprites.draw(self.screen)
     self.ui.draw()
     self.OpponentUi.draw()

  def apply_attack(self, target, attack):
    print(attack)
    attack_data = ABILITIES_DATA[attack]
    attack_type = attack_data['element']
    element_data = ELEMENT_DATA[attack_type]
    damage = attack_data['damage']
    animation = attack_data['animation']
    self.audio[animation].play()
    print(self.attack_sprites[animation])
    AttackAnimationSprite(target, self.attack_sprites[animation], self.all_sprites)
    element_multiplier = element_data[target.element]
    target.health -= damage *  element_multiplier 
    print(target.name)
    print(f'{attack},{target.health}/{target.max_health}')

  def get_input(self, state, data = None):
    if state == 'escape':
        self.running = False

    elif state == 'attack':
       self.apply_attack(self.opponent_monster, data)

    elif state == 'heal':
      self.audio['green'].play()

      self.monster.health += 50
      AttackAnimationSprite(self.monster, self.attack_sprites['green'], self.all_sprites)

    elif state == 'switch':
       self.monster.kill()
       self.monster = data
       self.all_sprites.add(self.monster)
       self.ui.monster = self.monster
       

    self.player_active = False
    self.timers['player_end'].activate()
    print(state)
    print(data)

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
    self.attack_sprites = tile_importer(4, 'assets', 'images', 'attacks')
    self.audio = import_audio()
    # print(self.attack_sprites)
  
  def run(self):
    dt = self.clock.tick(FPS) / 1000
    while self.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.update(dt)
        self.draw()
    
    pygame.quit()