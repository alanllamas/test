import pygame
from config import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, pos, groups, keys=0):
        super().__init__(groups)
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(COLORS['paddle'])  # White color
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = PADDLE_SPEED
        self.keys = [
            pygame.K_w,  # Up key
            pygame.K_s,  # Down key
        ] if keys == 0 else [
            pygame.K_UP,  # Up key
            pygame.K_DOWN,  # Down key
        ]

    def update(self, dt):
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

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.fill(COLORS['ball'])  # White color
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.collided = pygame.Vector2()

    def update(self, dt):
        self.move(dt)
        self.collide_screen()
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
        if self.rect.left < 0:
            self.rect.left = 0
            self.collided.x = 1
        # if self.rect.right > SCREEN_WIDTH:
        #     self.rect.right = SCREEN_WIDTH
        #     self.collided.x = 1
    
    def bounce(self):
        if self.collided.x != 0:
          self.speed_x *= -1
          self.collided.x = 0
        if self.collided.y != 0:
          self.speed_y *= -1
          self.collided.y = 0