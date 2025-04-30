import pygame
from os import walk
from os.path import join
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, FPS, PLAYER_LAYER

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, groups, collition_sprites):
    super().__init__(groups)
    self.state = 'down'
    self.frame_index = 0
    self.load_images()
    self._layer = PLAYER_LAYER
    self.rect = self.image.get_frect(center=pos)
    self.hit_box = self.rect.inflate(-50, -80)
    self.speed = 0.5
    self.direction = pygame.Vector2()
    self.collition_sprites = collition_sprites

  def load_images(self):
    self.frames = {
      'right': [],
      'left': [],
      'up': [],
      'down': []
    }
    # pygame.image.load(join("assets","images", "player", "right", f"{i}.png")).convert_alpha() for i in range(4)
    # pygame.image.load(join("assets","images", "player", "left", f"{i}.png")).convert_alpha() for i in range(4)
    # pygame.image.load(join("assets","images", "player", "up", f"{i}.png")).convert_alpha() for i in range(4)
    # pygame.image.load(join("assets","images", "player", "down", f"{i}.png")).convert_alpha() for i in range(4)
    for state in self.frames.keys():
      for path, folders, files in walk(join("assets", "images", "player", state)):
        if files:
          for file in sorted(files, key=lambda x: int(x.split(".")[0])):
            full_path = join(path, file)
            self.frames[state].append(pygame.image.load(full_path).convert_alpha())
    self.image = self.frames[self.state][self.frame_index]
    print(self.frames)
  def update(self, dt):
    self.move(dt)

  def move(self, dt):
    self.animate(dt)
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

  def animate(self, dt):
    # get state
    if self.direction.x != 0 or self.direction.y != 0:
      if self.direction.x != 0:
        if self.direction.x > 0:
          self.state = "right"
        else:
          self.state = "left"
      elif self.direction.y != 0:
        if self.direction.y > 0:
          self.state = "down"
        else:
          self.state = "up"
      self.run_animation(dt)
    else:
      self.image = self.frames[self.state][0]

   
    

  def run_animation(self, dt):
    self.frame_index += 0.5 * dt
    self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

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