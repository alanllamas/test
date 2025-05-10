from os.path import join
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, FPS
from player import Player
from sprites import *
from groups import *
from random import randint
from pytmx.util_pygame import load_pygame


class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vampire Survivor")
    self.clock = pygame.time.Clock()
    self.running = True
    self.all_sprites = AllSprites()
    self.collition_sprites = pygame.sprite.Group()
    self.bullet_sprites = pygame.sprite.Group()
    self.enemy_sprites = pygame.sprite.Group()
    self.spawn_positions = []
    
    # audio
    self.shoot_sound = pygame.mixer.Sound(join("assets", "audio", "shoot.wav"))
    self.shoot_sound.set_volume(0.2)
    self.impact_sound = pygame.mixer.Sound(join("assets", "audio", "impact.ogg"))
    self.impact_sound.set_volume(0.2)
    self.music = pygame.mixer.Sound(join("assets", "audio", "music.wav"))
    self.music.set_volume(0.3)
    self.music.play(-1)
    
    self.setup()



  def setup(self):
    self.create_enemy_event = pygame.event.custom_type()
    pygame.time.set_timer(self.create_enemy_event, 300)
    map = load_pygame(join("assets", "data", "maps", "world.tmx"))

    for x, y, image in map.get_layer_by_name("Ground").tiles():
      Sprite(self.all_sprites, (x * TILE_SIZE, y * TILE_SIZE), image)

    for sprite in map.get_layer_by_name("Objects"):
      CollitionSprite((self.all_sprites, self.collition_sprites), (sprite.x, sprite.y), sprite.image)

    for sprite in map.get_layer_by_name("Collisions"):
      # print(sprite)
      surf = pygame.surface.Surface((sprite.width, sprite.height))
      surf.fill("black")
      surf.set_colorkey("black")
      CollitionSprite(self.collition_sprites, (sprite.x, sprite.y ), surf)

    for sprite in map.get_layer_by_name("Entities"):
      if sprite.name == "Player":
        self.player = Player((sprite.x, sprite.y), self.all_sprites, self.collition_sprites)
        self.player.rect = self.player.image.get_frect(center=(sprite.x, sprite.y))
        Gun(self.all_sprites, self.player, self.bullet_sprites, self.shoot_sound)
      if sprite.name == "Enemy":
        self.spawn_positions.append((sprite.x, sprite.y))

  def collitions(self):
    if self.bullet_sprites:
      for bullet in self.bullet_sprites:
  #     if self.enemy_sprites.__len__() > 0 and self.bullet_sprites.__len__() > 0:
        bullet_hit_enemy = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False)
        # print(bullet_hit_enemy)
        if bullet_hit_enemy:
            for enemy in bullet_hit_enemy:
              # self.player.life -= meteor.damage
              # if explotion_sound:
              #     explotion_sound.set_volume(0.2)
              #     explotion_sound.play()
              
              enemy.destroy()
              # if self.player.life <= 0:
              #     self.player.kill()
              #     self.running = False
    if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
      enemy.destroy()
      self.running = False
      # print('collition')
      # for enemy in self.enemy_sprites:
      #   if enemy.death_time == 0:
      #     self.player.life -= enemy.damage
      #     if self.player.life <= 0:
      #       self.player.kill()
            # print('game over')
            # pygame.quit()



  def run(self):
    while self.running:
      dt = self.clock.tick(FPS)
      self.screen.fill((0, 0, 0))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        if event.type == self.create_enemy_event:
          Enemy(random.choice(self.spawn_positions), (self.all_sprites, self.enemy_sprites), self.player, self.collition_sprites, self.impact_sound)
          # print('created enemy')
      self.all_sprites.update(dt)
      self.collitions()
      # self.screen.blit(self.player.image, self.player.rect)
      self.all_sprites.draw_camera(self.player.rect.center)
      pygame.display.flip()
      # pygame.display.update()

    pygame.quit()
if __name__ == '__main__':
  game = Game()
  game.run()