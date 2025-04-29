from os.path import join
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, FPS
from player import Player
from sprites import CollisionSprite
from random import randint


class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vampire Survivor")
    self.clock = pygame.time.Clock()
    self.running = True
    self.all_sprites = pygame.sprite.Group()
    self.collition_sprites = pygame.sprite.Group()
    self.player = Player(self.all_sprites, self.collition_sprites)
    for i in range(6):
      pos = (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
      size = (randint(60, 100), randint(50, 100))
      CollisionSprite((self.all_sprites, self.collition_sprites), size, pos)

  def run(self):
    while self.running:
      dt = self.clock.tick(FPS)
      self.screen.fill((0, 0, 0))

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

      self.all_sprites.update(dt)
      # self.screen.blit(self.player.image, self.player.rect)
      self.all_sprites.draw(self.screen)
      pygame.display.flip()
      # pygame.display.update()

    pygame.quit()
if __name__ == '__main__':
  game = Game()
  game.run()