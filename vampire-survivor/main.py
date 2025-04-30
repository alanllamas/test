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
    self.setup()

  def setup(self):
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
        self.player = Player( (sprite.x, sprite.y), self.all_sprites, self.collition_sprites)
        # self.player.image = sprite.image
        self.player.rect = self.player.image.get_frect(center=(sprite.x, sprite.y))


  def run(self):
    while self.running:
      dt = self.clock.tick(FPS)
      self.screen.fill((0, 0, 0))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

      self.all_sprites.update(dt)
      # self.screen.blit(self.player.image, self.player.rect)
      self.all_sprites.draw_camera(self.player.rect.center)
      pygame.display.flip()
      # pygame.display.update()

    pygame.quit()
if __name__ == '__main__':
  game = Game()
  game.run()