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
DATA_LAYER = 2
PLAYER_LAYER = 1
BG_LAYER = 0
PLAYER_SPEED = 400
LASER_SPEED = 500
LASER_POWER = 30
METEOR_LIFE = 100
PLAYER_LIFE = 300
METEOR_POWER = 100
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
        self.shoot_cooldown = 200
        self.can_shoot = True
        self.shoot_time = 0
        self.life = PLAYER_LIFE
        self.lives = []
        self.score = 0
        self.set__initial_lives()


    def update(self):
        self.move()
        self.collide_boundries()
        self.shoot()
        self.shoot_timer()
        self.update_lives()

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
            laser_a = Laser(all_sprites)
            laser_a.rect.center = self.rect.center
            # laser_a.rect.x += 10
            laser_a.rect.y -= self.rect.height
            # laser_b = Laser(all_sprites)
            # laser_b.rect.center = self.rect.center
            # laser_b.rect.y -= self.rect.height
            # laser_b.rect.x -= 10

    def set__initial_lives(self):
        for i in range(0, int(self.life / 100)):
            self.lives.append(Life((5 * i) + 5 , 10, i , all_sprites))

    def update_lives(self):
        for life in self.lives:
            life.kill()
        for i in range(0, int(self.life / 100)):
            self.lives.append(Life((5 * i) + 5 , 10, i , all_sprites))

class Life(pygame.sprite.Sprite):
    def __init__(self, x, y, index, groups):
        self._layer = PLAYER_LAYER
        super().__init__(groups)
        self.pre_image = pygame.image.load("assets/player.png").convert_alpha()
        self.size = self.pre_image.get_size()
        self.image = pygame.transform.scale(self.pre_image, (int(self.size[0]/4), int(self.size[1]/4)) )
        self.rect = self.image.get_frect()
        self.rect.x = x + (index * self.rect.width)
        self.rect.y = y
        
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, y=None):
        self._layer = BG_LAYER
        super().__init__(groups)
        self.image = pygame.image.load("assets/star.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.rect.x = random.randint(0, int(SCREEN_WIDTH - self.rect.width))
        if y is None: 
            y = -self.rect.height
        else:
            y = random.randint(0, int(SCREEN_HEIGHT - self.rect.height)) 
        self.rect.y = y
    
    def update(self):
        self.rect.y += 1.5
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        
class Meteor(pygame.sprite.Sprite):
    def  __init__(self, groups):
        self._layer = PLAYER_LAYER     
        super().__init__(groups)
        self.default_image = pygame.image.load("assets/meteor.png").convert_alpha()
        self.image = self.default_image
        self.rect = self.image.get_frect()
        self.rect.x = random.randint(0, int(SCREEN_WIDTH - self.rect.width))
        self.rect.y = -self.rect.height
        self.speed = random.randint(400, 500)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.life = METEOR_LIFE
        self.damage = METEOR_POWER
        self.rotation = 0
    
    def update(self):
        self.move()
    
    def move(self):
        self.rect.center += self.direction * self.speed * dt
        self.rotation += 50 * dt
        self.image = pygame.transform.rotate(self.default_image, self.rotation)

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__((groups, laser_sprites))
        self._layer = PLAYER_LAYER
        self.image = pygame.image.load("assets/laser.png").convert_alpha()
        self.rect = self.image.get_frect()
        self.speed = LASER_SPEED
        self.damage = LASER_POWER
    
    def update(self):
        self.move()
    
    def move(self):
        self.rect.y -= self.speed * dt
        if self.rect.y < 0:
            self.kill()
    
def display_score():
    score_surf = font.render(f"Score: {str(player.score)}" , True, (240,240,240))
    # box_surf = pygame.Surface(score_surf.get_rect().inflate(10, 10).size, pygame.SRCALPHA)
    # box_surf.fill(WHITE)
    # box_surf.fill((0,0,0,100))
    # box_surf.blit(score_surf, score_surf.get_rect(center = box_surf.get_rect().center))
    time = int(pygame.time.get_ticks() / 1000)
    time_surf = font.render(f"Time: {str(time)}", True, (240,240,240))
    time_rect = time_surf.get_frect(topright = (int(SCREEN_WIDTH - 40), 50))
    
    score_rect = score_surf.get_frect(topright = (int(SCREEN_WIDTH - 40), 20))
    border_rect = score_rect.inflate(40, score_rect.y * 2)
    bg_surf = pygame.Surface(border_rect.size, pygame.SRCALPHA)
    bg_surf.fill((0,0,0,100))
    border_rect.y = score_rect.y - 7
    # pygame.draw.rect(screen, (0,0,0,0), bg_surf.get_frect(center = border_rect.center), 0, 5)
    # screen.blit(bg_surf, border_rect)
    pygame.draw.rect(screen, (240,240,240), border_rect, 2, 5)
    screen.blit(score_surf, score_rect)
    screen.blit(time_surf,time_rect)
    

# game setup
pygame.init()
running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.Font("assets/Oxanium-Bold.ttf", 20)

screen_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_background.fill("#3a2e3f")

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

# collitions
def collitions():
    global running
    # Check for collisions between lasers and meteors
    for laser in laser_sprites:
        meteor_hit = pygame.sprite.spritecollide(laser, meteor_sprites, False, pygame.sprite.collide_mask)
        if meteor_hit:
            laser.kill()
            for meteor in meteor_hit:
                # meteor.take_damage(laser.damage)
                meteor.life -= laser.damage
                if meteor.life <= 0:
                    player.score += 1
                    meteor.kill()
                # Add explosion effect here if needed

    # Check for collisions between player and meteors
    meteor_hit_player = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    if meteor_hit_player:
        for meteor in meteor_hit_player:
          player.life -= meteor.damage
          meteor.kill()
          if player.life <= 0:
              player.kill()
              running = False
        # Add game over logic here
# Game loop
while running:
    dt = clock.tick(FPS) / 1000
    time_surf = font.render(str(int(dt)), True, 'black')

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
    collitions()


    #draw game state
    all_sprites.draw(screen)
    display_score()
    # screen.blit(score_surf, (int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 40))
    # screen.blit(time_surf, (int(SCREEN_WIDTH - 40), 40))

    pygame.display.update()

pygame.quit()