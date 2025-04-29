from os.path import join
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60


def animate(frames, speed):
  def __init__(self, frames, speed):
    self.frames = frames
    self.speed = speed
    self.index = 0
    self.image = self.frames[self.index]
    self.time = 0
    self.update()

  def update(self, dt):
    self.time += dt
    if self.time >= self.speed:
      self.index += 1
      if self.index >= len(self.frames):
        self.index = 0
      self.image = self.frames[self.index]
      self.time = 0
class Player(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self._layer = 1
    self.right_frames = [pygame.image.load(join("assets","images", "player", "right", f"{i}.png")).convert_alpha() for i in range(4)]
    self.left_frames = [pygame.image.load(join("assets","images", "player", "left", f"{i}.png")).convert_alpha() for i in range(4)]
    self.up_frames = [pygame.image.load(join("assets","images", "player", "up", f"{i}.png")).convert_alpha() for i in range(4)]
    self.down_frames = [pygame.image.load(join("assets","images", "player", "down", f"{i}.png")).convert_alpha() for i in range(4)]
    self.image = self.down_frames[0]
    self.rect = self.image.get_frect(center=(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
    self.speed = 5
    self.direction = pygame.Vector2(0, 0)

  def update(self):
    self.move()

  def move(self):
    keys = pygame.key.get_pressed()

    self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
    self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
    self.rect.move_ip(self.direction * self.speed)
    # if self.direction.x > 0:


class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vampire Survivor")
    self.clock = pygame.time.Clock()
    self.running = True
    self.all_sprites = pygame.sprite.Group()
    self.player = Player(self.all_sprites)
    self.dt = 0

  def start(self):
    while self.running:
      self.dt = self.clock.tick(FPS)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

      self.screen.fill((0, 0, 0))
      self.all_sprites.draw(self.screen)
      self.all_sprites.update()
      # self.screen.blit(self.player.image, self.player.rect)
      pygame.display.flip()
      # pygame.display.update()

    pygame.quit()

game = Game()
game.start()