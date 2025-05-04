import pygame
import json
import sys
from config import *
from sprites import *
from os.path import join
class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.screen.fill(COLORS['bg'])
    pygame.display.set_caption("Ping Pong Game")
    self.clock = pygame.time.Clock()
    self.running = True
    self.font = pygame.font.Font(None, 160)
    self.setup()
    self.screen_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.screen_background.fill(COLORS['bg'])


  def display_score(self):
    if self.left_paddle is not None:
      opponent_score_text = self.font.render(str(self.left_paddle.score), True, COLORS['bg detail'])
      opponent_score_rect = opponent_score_text.get_rect(center=((SCREEN_WIDTH / 2) - 100, SCREEN_HEIGHT / 2))
      self.screen.blit(opponent_score_text, opponent_score_rect)
    
    player_score_text = self.font.render(str(self.right_paddle.score), True, COLORS['bg detail'])
    player_score_rect = player_score_text.get_rect(center=((SCREEN_WIDTH / 2) + 100, SCREEN_HEIGHT / 2))
    self.screen.blit(player_score_text, player_score_rect)
    pygame.draw.line(self.screen, COLORS['bg detail'], (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT), 3)

  def setup(self):
    self.all_sprites = pygame.sprite.Group()
    self.paddle_sprites = pygame.sprite.Group()
    self.ball_sprites = pygame.sprite.Group()
    self.ball = None

    self.left_paddle_pos = [PADDLE_OFFSET, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2]
    self.right_paddle_pos = [SCREEN_WIDTH - PADDLE_OFFSET, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2]
    self.ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    try:
      with open(join('data', 'score.txt'), 'r') as f:
        self.score = json.load(f)
    except:
      self.score = {'left': 0, 'right': 0}
    self.left_paddle = None
    # self.left_paddle = Paddle(self.left_paddle_pos, (self.all_sprites, self.paddle_sprites), self.ball, 'left', keys=[pygame.K_w, pygame.K_s])
    self.right_paddle = Paddle(self.right_paddle_pos, (self.all_sprites, self.paddle_sprites), self.ball, 'right', keys=[pygame.K_UP, pygame.K_DOWN])
    if self.left_paddle is not None:
      self.left_paddle.score= self.score['left']
    self.right_paddle.score = self.score['right']
    self.create_ball_event = pygame.event.custom_type()
    pygame.time.set_timer(self.create_ball_event, 1500)

  def run(self):
    while self.running:
      dt = self.clock.tick(FPS)
      self.handle_events()
      self.update(dt)
    pygame.quit()
    sys.exit()



  def handle_events(self):

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        with open(join('data', 'score.txt'), 'w') as f:
          print('Saving score', f)
          json.dump({
            'left': self.left_paddle.score,
            'right': self.right_paddle.score
          }, f)
        self.running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          with open(join('data', 'score.txt'), 'w') as f:
            print('Saving score', f)
            json.dump({
              'left': self.left_paddle.score,
              'right': self.right_paddle.score
            }, f)
          self.running = False
      if event.type == self.create_ball_event:
        if self.ball is None:
          self.ball = Ball(self.ball_pos, (self.all_sprites, self.ball_sprites), self.paddle_sprites)
        if self.left_paddle is None:
          self.left_paddle = Paddle(self.left_paddle_pos, (self.all_sprites, self.paddle_sprites), self.ball, 'left', keys=None)
          self.left_paddle.score= self.score['left']

        elif self.ball.groups().__len__() == 0:
          self.ball = Ball(self.ball_pos, (self.all_sprites, self.ball_sprites), self.paddle_sprites)
          self.left_paddle.ball = self.ball
        # elif :
        #   print(self.ball.groups())

            # Create a new star
            # Meteor((all_sprites, meteor_sprites))
  
  def update(self, dt):
    self.screen.blit(self.screen_background, (0, 0))
    self.display_score()
    self.all_sprites.update(dt)
    self.all_sprites.draw(self.screen)
    pygame.display.flip()  # Update the display


game = Game()
game.run()