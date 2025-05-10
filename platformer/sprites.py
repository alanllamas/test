import pygame
from config import *
from timers import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, position, image):
        super().__init__(groups)
        self._layer = BG_LAYER
        self.image = image
        self.position = pygame.Vector2(position)
        self.rect = self.image.get_rect(topleft=self.position * TILE_SIZE)
        self.collidable = True

class AnimatedSprite(pygame.sprite.Sprite):
  def __init__(self, groups, pos, frames):
    super().__init__(groups)
    self.frame_index = 0
    self.frames = frames
    self.image = self.frames[self.frame_index]
    self.rect = self.image.get_rect(midtop=pos)
    self.collidable = False

  def animate(self, dt):
    # get state
      self.frame_index += .8 * dt
      self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Bee(AnimatedSprite):
  def __init__(self, groups, pos, frames, collition_sprites):
      super().__init__(groups, pos, frames)
      self.collition_sprites = collition_sprites
      self.direction = pygame.Vector2()
  
  def update(self, dt):
     self.animate(dt)
    
  # def collition(self, direction):
  #   collitions = pygame.sprite.spritecollide(self, self.collition_sprites, False)
  #   if collitions:
  #     for sprite in collitions:
  #       if direction == "horizontal":
  #         if self.direction.x > 0:
  #           self.rect.right = sprite.rect.left
  #         elif self.direction.x < 0:
  #           self.image = pygame.transform.flip(self.image, True, False)
  #           self.rect.left = sprite.rect.right
  #       if direction == "vertical":
  #         if self.direction.y > 0:
  #           self.rect.bottom = sprite.rect.top
  #           self.can_jump = True
  #         if self.direction.y < 0:
  #           self.rect.top = sprite.rect.bottom
  #         self.direction.y = 0
      
class Worm(AnimatedSprite):
  def __init__(self, groups, pos, frames, collition_sprites):
      super().__init__(groups, pos, frames)
      self.collition_sprites = collition_sprites
      self.direction = pygame.Vector2()
  def update(self, dt):
     self.animate(dt)
  # def collition(self, direction):
  #   collitions = pygame.sprite.spritecollide(self, self.collition_sprites, False)
  #   if collitions:
  #     for sprite in collitions:
  #       if direction == "horizontal":
  #         if self.direction.x > 0:
  #           self.rect.right = sprite.rect.left
  #         elif self.direction.x < 0:
  #           self.image = pygame.transform.flip(self.image, True, False)
  #           self.rect.left = sprite.rect.right
  #       if direction == "vertical":
  #         if self.direction.y > 0:
  #           self.rect.bottom = sprite.rect.top
  #           self.can_jump = True
  #         if self.direction.y < 0:
  #           self.rect.top = sprite.rect.bottom
  #         self.direction.y = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, position, surf, direction):
      super().__init__(groups)
      self.image = surf
      self.rect = self.image.get_rect(topleft=position)
      self.direction = direction
      self.speed = 0
      self.collidable = False

      self.image = pygame.transform.flip(self.image, direction == -1, False)

    def update(self, dt):
       self.rect.x += self.direction *  self.speed * dt 
   
class Player(AnimatedSprite):
    def __init__(self, groups, position, frames, collition_sprites, create_bullet):
        super().__init__(groups, position, frames)
        self._layer = PLAYER_LAYER
        self.position = pygame.Vector2(position)
        self.speed = 1
        self.direction = pygame.Vector2()
        self.collition_sprites = collition_sprites
        self.gravity = 1.75
        self.pressed_keys = []
        self.can_jump = True
        self.flip = False
        self.shoot_timer = Timer(500)
        self.create_bullet = create_bullet

    def update(self, dt):
        self.input(dt)
        self.move(dt)
        self.animate(dt)
        self.shoot_timer.update()
    
    def input(self, dt):
      self.pressed_keys = pygame.key.get_pressed()
      if (self.pressed_keys[pygame.K_SPACE] or self.pressed_keys[pygame.K_UP]) and self.can_jump:
        self.direction.y = -200 * dt
        self.can_jump = False
      if self.pressed_keys[pygame.K_s] and not self.shoot_timer:
         self.create_bullet(self.rect.center, -1 if self.flip else 1)
         self.shoot_timer.activate()

    def move(self, dt):

        self.direction.x = int(int(self.pressed_keys[pygame.K_RIGHT] or self.pressed_keys[pygame.K_d]) - int(self.pressed_keys[pygame.K_LEFT] or self.pressed_keys[pygame.K_a]))
        self.collition("horizontal")
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        # self.direction.y = int(int(self.pressed_keys[pygame.K_DOWN] or self.pressed_keys[pygame.K_s]) - int(self.pressed_keys[pygame.K_UP] or self.pressed_keys[pygame.K_w]))
        # self.direction = self.direction.normalize() if self.direction.magnitude() > 0 else pygame.Vector2()
        self.rect.x += self.direction.x * self.speed 

        self.collition("vertical")
    
    def collition(self, direction):
      collitions = pygame.sprite.spritecollide(self, self.collition_sprites, False)
      if collitions:
        for sprite in collitions:
          if direction == "horizontal":
            if self.direction.x > 0:
              self.rect.right = sprite.rect.left
            elif self.direction.x < 0:
              self.image = pygame.transform.flip(self.image, True, False)
              self.rect.left = sprite.rect.right
          if direction == "vertical":
            if self.direction.y > 0:
              self.rect.bottom = sprite.rect.top
              self.can_jump = True
            if self.direction.y < 0:
              self.rect.top = sprite.rect.bottom
            self.direction.y = 0
    def animate(self, dt):
      # get state
      if self.direction.x != 0:
          self.frame_index += .8 * dt
          self.image = self.frames[int(self.frame_index) % len(self.frames)]
          self.flip = self.direction.x < 0
      else:
        self.image = self.frames[0]

      self.image = pygame.transform.flip(self.image, self.flip, False)