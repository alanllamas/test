import pygame
import random

# Variables

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PLAYER_SPEED = 400
LASER_SPEED = 400
PLAYER_LAYER = 1
BG_LAYER = 0
# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        self._layer = PLAYER_LAYER
        super().__init__(groups)
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        self.speed = PLAYER_SPEED
        self.direction = pygame.Vector2()
        self.shoot_cooldown = 100
        self.can_shoot = True
        self.shoot_time = 0

    def update(self):
        self.move()
        self.collide_boundries()
        self.shoot()
        self.shoot_timer()

    def move(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] -keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        
    def collide_boundries(self):
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
          self.rect.right = SCREEN_WIDTH

    def shoot_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True
                self.shoot_time = 0
    def shoot(self):
        # Create a new laser
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            laser = Laser(all_sprites)
            laser.rect.center = self.rect.center
            laser.rect.y -= self.rect.height
            # return laser

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, y=None):
        self._layer = BG_LAYER
        super().__init__(groups)
        self.image = pygame.image.load("assets/star.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        if y is None: 
            y = -self.rect.height
        else:
            y = random.randint(0, SCREEN_HEIGHT - self.rect.height) 
        self.rect.y = y
    
    def update(self):
        self.rect.y += 1.5
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        
class Meteor(pygame.sprite.Sprite):
    def  __init__(self, groups):
        self._layer = PLAYER_LAYER     
        super().__init__(groups)
        self.image = pygame.image.load("assets/meteor.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(400, 500)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
    
    def update(self):
        self.move()
    
    def move(self):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
class Laser(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__((groups, laser_sprites))
        self._layer = PLAYER_LAYER
        self.image = pygame.image.load("assets/laser.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.speed = LASER_SPEED
    
    def update(self):
        self.move()
    
    def move(self):
        self.rect.y -= self.speed * dt
        if self.rect.y < 0:
            self.kill()
    
    
# game setup
pygame.init()
running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.Font("assets/Oxanium-Bold.ttf", 36)
screen_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_background.fill("darkgray")

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

player = Player((all_sprites, player_sprites))
stars = []
for y in range(0, 20):
  stars.append(Star(all_sprites, y))

# Events
create_meteor_event = pygame.event.custom_type()
pygame.time.set_timer(create_meteor_event, 750)
create_star_event = pygame.event.custom_type()
pygame.time.set_timer(create_star_event, 400)


# Game loop
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill(BLACK)
    screen.blit(screen_background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == create_star_event:
            # Create a new star
            stars.append(Star(all_sprites))
        if event.type == create_meteor_event:
            # Create a new star
            Meteor((all_sprites, meteor_sprites))

    # Update game state
    all_sprites.update()
    meteor_player_collition_sprites = pygame.sprite.groupcollide(meteor_sprites, player_sprites, False, False)
    meteor_laser_collition_sprites = pygame.sprite.groupcollide(meteor_sprites, laser_sprites, True, True)

    if meteor_player_collition_sprites:
        for meteor in meteor_player_collition_sprites:
            meteor.kill()
            player.kill()
            running = False


    #draw game state
    all_sprites.draw(screen)


    pygame.display.update()

pygame.quit()