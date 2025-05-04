import pygame
from config import *
import random

class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos, groups, ball, name, keys):
        super().__init__(groups)
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(COLORS['paddle'])  # White color
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = PADDLE_SPEED
        self.ball = ball
        self.name = name
        self.keys = keys
        self.score = 0

    def update(self, dt):
        if self.keys is not None:
          keys = pygame.key.get_pressed()
          if keys[self.keys[0]]:
              self.rect.y -= self.speed * dt
          if keys[self.keys[1]]:
              self.rect.y += self.speed * dt
          # Keep the paddle within the screen bounds
          if self.rect.top < 0:
              self.rect.top = 0
          if self.rect.bottom > SCREEN_HEIGHT:
              self.rect.bottom = SCREEN_HEIGHT
        elif self.ball is not None:
          if self.rect.y < self.ball.rect.y:
            self.rect.y += self.speed * dt
          if self.rect.y > self.ball.rect.y:
            self.rect.y -= self.speed * dt

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, groups, paddle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        pygame.draw.circle(self.image, COLORS['ball'], (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.direction = pygame.Vector2(random.randint(0,1), random.randint(0,1))
        if self.direction.x == 0:
           self.speed_x *= -1
        if self.direction.y == 0:
           self.speed_y *= -1
        self.collided = pygame.Vector2()
        self.paddle_sprites = paddle_sprites
        self.old_rect = self.rect.copy()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.collide_screen()
        self.collide_paddle_ball()
        self.bounce()

    def move(self, dt):
        self.rect.x += self.speed_x * dt
        self.rect.y += self.speed_y * dt
        # if self.rect.left < self.rect.width or self.rect.right + self.rect.width > SCREEN_WIDTH:
        #     self.kill()
        
    def collide_screen(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.collided.y = 1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.collided.y = 1
        if self.rect.right < -10:
            # self.rect.left = 0
            for paddle_sprite in self.paddle_sprites:
                if paddle_sprite.name == 'right':
                    paddle_sprite.score += 1
            # self.collided.x = 1
            self.kill()
        if self.rect.left > SCREEN_WIDTH + 10:
            # self.rect.right = SCREEN_WIDTH
            for paddle_sprite in self.paddle_sprites:
                if paddle_sprite.name == 'left':
                    paddle_sprite.score += 1
            self.kill()
            # self.collided.x = 1
    
    def bounce(self):
      if self.collided.x != 0:
        self.speed_x *= -1
        self.collided.x = 0
      if self.collided.y != 0:
        self.speed_y *= -1
        self.collided.y = 0
    
    # move collition to ball class and check for previous frame of bal for collition check in four sides
    def collide_paddle_ball(self):
      for paddle_sprite in self.paddle_sprites:
        if pygame.sprite.spritecollide(self, self.paddle_sprites, False, pygame.sprite.collide_mask):   
        # if paddle_sprite.rect.colliderect(self.rect):
          if self.rect.right >= paddle_sprite.rect.left and self.old_rect.right <= paddle_sprite.rect.left:
            self.rect.right = paddle_sprite.rect.left
            self.collided.x = 1
          if self.rect.left <= paddle_sprite.rect.right and self.old_rect.left >= paddle_sprite.rect.right:
            self.rect.left = paddle_sprite.rect.right
            self.collided.x = 1
          if self.rect.top <= paddle_sprite.rect.bottom and self.old_rect.top >= paddle_sprite.rect.bottom:
            self.rect.top = paddle_sprite.rect.bottom
            self.collided.y = 1
            self.collided.x = 1
          if self.rect.bottom >= paddle_sprite.rect.top and self.old_rect.bottom <= paddle_sprite.rect.top:
            self.collided.y = 1
            self.collided.x = 1
            self.rect.bottom = paddle_sprite.rect.top
          