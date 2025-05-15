import pygame
from config import *
from timers import *
from math import sin
from random import randint

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
    self.animation_speed = .8
    self.collidable = False

  def animate(self, dt):
    # get state
      self.frame_index += self.animation_speed * dt
      self.image = self.frames[int(self.frame_index) % len(self.frames)]
  
  def move(self):
      pass

class Enemy(AnimatedSprite):
    def __init__(self, groups, pos, frames):
      super().__init__(groups, pos, frames)
      self.death_timer = Timer(200, func = self.kill)
  
    def destroy(self):
      self.death_timer.activate()
      self.animation_speed = 0
      self.image = pygame.mask.from_surface(self.image).to_surface()
      self.image.set_colorkey('black')


    def update(self, dt):

      self.death_timer.update()
      if not self.death_timer:
        self.move(dt)
        self.animate(dt)
               
class Bee(Enemy):
  def __init__(self, groups, pos, frames):
    super().__init__(groups, pos, frames)
    self.direction = pygame.Vector2()
    self.speed = randint(60, 100)
    self.amplitude = randint(100, 300)
    self.frequency = randint(100, 300)
    self.move_x = pos[0]

  def move(self, dt):
    self.move_x -= self.speed * dt
    self.rect.x = self.move_x
    self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt
    if self.rect.x <= -500:
       self.kill()

class Worm(Enemy):
  def __init__(self, groups, pos, frames, width):
      super().__init__(groups, pos, frames)
      self.flip = False
      self.initial_position = pos[0] - 32
      self.max_position = pos[0] + width - 64
      self.speed = 20
      self.direction = 1
      self.pos_x = self.initial_position
      
  def move(self, dt):
    if self.rect.x >= self.max_position:
      self.flip = True
      self.direction = -1
      # self.image = pygame.transform.flip(self.image, self.flip, False)
    elif self.rect.x <= self.initial_position:
      self.flip = False
      self.direction = 1
    self.image = pygame.transform.flip(self.image, self.flip, False)
    self.pos_x += self.speed * dt * self.direction
    self.rect.x = self.pos_x
  
  def animate(self, dt):
    # get state
      self.frame_index += .8 * dt
      self.image = pygame.transform.flip(self.frames[int(self.frame_index) % len(self.frames)], self.flip, False)

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

class Fire(pygame.sprite.Sprite):
  def __init__(self, groups, position, surf, player):
    super().__init__(groups)
    self.image = surf
    self.player = player
    self.rect = self.image.get_rect(topleft=position)
    self.timer = Timer(100, autoStart = True, func = self.kill)
    self.collidable = False
    self.y_offset = pygame.Vector2(0,10)
    self.x_offset = pygame.Vector2(30,0)

    if self.player.flip:
       self.rect.midright = self.player.rect.midleft + self.y_offset
       self.image = pygame.transform.flip(self.image, True, False)
    else:
       self.rect.midright = self.player.rect.midright + self.y_offset + self.x_offset

  def update(self, dt):
      self.timer.update()

      if self.player.flip:
        self.rect.midright = self.player.rect.midleft + self.y_offset
      else:
        self.rect.midright = self.player.rect.midright + self.y_offset + self.x_offset
  
class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, position, surf, direction):
      super().__init__(groups)
      self.image = surf
      self.rect = self.image.get_rect(topleft=position)
      self.direction = direction
      self.speed = 300
      self.collidable = False
      self.bullet_timer = Timer(1000, func = self.kill, autoStart=True)
      self.image = pygame.transform.flip(self.image, direction == -1, False)

    def update(self, dt):
       self.bullet_timer.update()
       self.rect.x += self.direction *  self.speed * dt 
   
class Player(AnimatedSprite):
    def __init__(self, groups, position, frames, collition_sprites, create_bullet, shoot_sound):
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
        self.shoot_timer = Timer(300)
        self.create_bullet = create_bullet
        self.shoot_sound = shoot_sound
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
         self.shoot_sound.set_volume(.1)
         self.shoot_sound.play()
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