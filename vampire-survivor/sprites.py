import pygame
from os.path import join
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_LAYER, PLAYER_LAYER
import random
from os import walk

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, position, image):
        super().__init__(groups)
        self._layer = BG_LAYER
        self.image = image
        self.rect = self.image.get_frect(topleft=position)
        self.ground = True

class CollitionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, position, image):
        super().__init__(groups)
        self._layer = BG_LAYER
        self.image = image
        self.rect = self.image.get_frect(topleft=position)

class Gun(pygame.sprite.Sprite):
    def __init__(self, groups, player, bullet_sprites):
        super().__init__(groups)
        self.player = player
        self._layer = PLAYER_LAYER
        self.bullet_sprites = bullet_sprites
        self.all_sprites = groups
        self.surf = pygame.image.load(join("assets", "images", "gun", "gun.png")).convert_alpha()
        self.image = self.surf
        self.player_direction = pygame.Vector2(0, 0)
        self.distance = 140
        self.rect = self.image.get_frect(center=self.player.rect.center + self.player_direction * self.distance)
        self.can_shoot = True
        self.shoot_delay = 100
        self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            if pygame.time.get_ticks() - self.shoot_time > self.shoot_delay:
                self.can_shoot = True
                self.shoot_time = pygame.time.get_ticks()

    def get_direction(self):
        mouse_pos = pygame.mouse.get_pos()
        player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = self.player_direction.angle_to(pygame.Vector2(1, -0.1))
        self.image = pygame.transform.rotate(self.surf, angle)
        self.rect = self.image.get_frect(center=self.rect.center)

    def shoot(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.can_shoot:
            Bullet((self.all_sprites, self.bullet_sprites), self.rect.center + self.player_direction * 80, self.player_direction)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def update(self, dt):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        self.gun_timer()
        self.shoot()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, position, direction):
        super().__init__(groups)
        self.image = pygame.image.load(join("assets", "images", "gun", "bullet.png")).convert_alpha()
        self.rect = self.image.get_frect(center=position)
        self.spawn_time = pygame.time.get_ticks()
        self._layer = PLAYER_LAYER
        self.direction = direction
        self.speed = 1

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time > 1000:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, player, collition_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join("assets", "images", "enemies", "bat", "0.png")).convert_alpha()
        self.random_position = pygame.Vector2(random.randint(-500, 500),random.randint(-500, 500))
        self.player_offset = pygame.Vector2(random.randint(-300, 300),random.randint(-300, 300))
        self.rect = self.image.get_frect(center=player.rect.center + self.player_offset + self.random_position)
        self._layer = PLAYER_LAYER
        self.speed = 1
        self.player = player
        self.direction = (pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)) 
        self.collition_sprites = collition_sprites
        self.enemies = ['bat', 'blob', 'skeleton']
        self.enemy = random.choice(self.enemies)
        self.frame_index = 0
        self.load_images()

    def update(self, dt):
        self.direction = (pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)) 
        self.rect.center += self.direction * self.speed * dt / 1000
        self.collition()
        self.run_animation(dt)

    def collition(self):
      for sprite in self.collition_sprites:
        if sprite.rect.colliderect(self.rect):
          if self.direction[0] != 0:
            if self.direction.x > 0:
              self.rect.right = sprite.rect.left
            if self.direction.x < 0:
              self.rect.left = sprite.rect.right
          if self.direction[0] != 0:
            if self.direction.y > 0:
              self.rect.bottom = sprite.rect.top
            if self.direction.y < 0:
              self.rect.top = sprite.rect.bottom
    
    def load_images(self):
      self.frames = {
        'bat': [],
        'blob': [],
        'skeleton': []
      }

      for enemy in self.frames.keys():
          for path, folders, files in walk(join("assets", "images", "enemies", enemy)):
              if files:
                  for file in sorted(files, key=lambda x: int(x.split(".")[0])):
                      full_path = join(path, file)
                      self.frames[enemy].append(pygame.image.load(full_path).convert_alpha())
      self.image = self.frames[self.enemy][self.frame_index]

    def run_animation(self, dt):
      self.frame_index += 0.5 * dt
      self.image = self.frames[self.enemy][int(self.frame_index) % len(self.frames[self.enemy])]