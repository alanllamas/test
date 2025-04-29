import pygame
from os.path import join
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, FPS, PLAYER_LAYER

class Player(pygame.sprite.Sprite):
  def __init__(self, groups, collition_sprites):
    super().__init__(groups)
    self._layer = PLAYER_LAYER
    self.right_frames = [pygame.image.load(join("assets","images", "player", "right", f"{i}.png")).convert_alpha() for i in range(4)]
    self.left_frames = [pygame.image.load(join("assets","images", "player", "left", f"{i}.png")).convert_alpha() for i in range(4)]
    self.up_frames = [pygame.image.load(join("assets","images", "player", "up", f"{i}.png")).convert_alpha() for i in range(4)]
    self.down_frames = [pygame.image.load(join("assets","images", "player", "down", f"{i}.png")).convert_alpha() for i in range(4)]
    self.image = self.down_frames[0]
    self.rect = self.image.get_frect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
    self.hit_box = self.rect.inflate(-40, 0)
    self.speed = 0.5
    self.direction = pygame.Vector2()
    self.collition_sprites = collition_sprites

  def update(self, dt):
    self.move(dt)

  def move(self, dt):
    keys = pygame.key.get_pressed()

    self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
    self.collition("horizontal")
    self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
    self.collition("vertical")
    self.direction = self.direction.normalize() if self.direction.magnitude() > 0 else pygame.Vector2()
    self.hit_box.move_ip(self.direction * self.speed * dt)
    # self.rect.move_ip(self.direction * self.speed * dt)

    self.rect.center = self.hit_box.center
    # if self.direction.x > 0:

  def collition(self, direction):
    for sprite in self.collition_sprites:
      if sprite.rect.colliderect(self.hit_box):
        if direction == "horizontal":
          if self.direction.x > 0:
            # self.rect.right = sprite.rect.left
            self.hit_box.right = sprite.rect.left
          if self.direction.x < 0:
            # self.rect.left = sprite.rect.right
            self.hit_box.left = sprite.rect.right
        if direction == "vertical":
          if self.direction.y > 0:
            # self.rect.bottom = sprite.rect.top
            self.hit_box.bottom = sprite.rect.top
          if self.direction.y < 0:
            # self.rect.top = sprite.rect.bottom
            self.hit_box.top = sprite.rect.bottom