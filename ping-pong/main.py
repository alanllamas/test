import pygame
import random
import sys
from config import *
from sprites import *
class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.screen.fill(COLORS['bg'])
    pygame.display.set_caption("Ping Pong Game")
    self.clock = pygame.time.Clock()
    self.running = True
    self.font = pygame.font.Font(None, 36)
    self.score = [0, 0]
    self.setup()
    self.screen_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.screen_background.fill(COLORS['bg'])

  def setup(self):
    self.all_sprites = pygame.sprite.Group()
    self.paddle_sprites = pygame.sprite.Group()
    self.ball_sprites = pygame.sprite.Group()

    self.left_paddle_pos = [25, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2]
    self.right_paddle_pos = [SCREEN_WIDTH - PADDLE_WIDTH, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2]
    self.ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

    self.left_paddle = Paddle(self.left_paddle_pos, (self.all_sprites, self.paddle_sprites), 0 )
    self.right_paddle = Paddle(self.right_paddle_pos, (self.all_sprites, self.paddle_sprites), 1 )
    self.ball = Ball(self.ball_pos, (self.all_sprites, self.ball_sprites))

  def run(self):
    while self.running:
      dt = self.clock.tick(FPS)
      self.handle_events()
      self.collide_paddle_ball()
      self.update(dt)
      # self.screen.draw()
    pygame.quit()
    sys.exit()
# move collition to ball class and check for previous frame of bal for collition check in four sides
  def collide_paddle_ball(self):
    paddle_collitions = pygame.sprite.groupcollide(self.paddle_sprites, self.ball_sprites, False, False)
    if paddle_collitions:
      for paddle in paddle_collitions:
        if self.ball.rect.colliderect(paddle.rect):
          self.ball.collided.x = 1


  def handle_events(self):

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.running = False
  
  def update(self, dt):
    # self.screen.fill((0, 0, 0))  # Clear the screen with black
    self.screen.blit(self.screen_background, (0, 0))
    self.all_sprites.update(dt)
    self.all_sprites.draw(self.screen)
    pygame.display.flip()  # Update the display


game = Game()
game.run()