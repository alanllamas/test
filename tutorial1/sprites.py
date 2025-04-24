import pygame
import math
import random
from config import *

class Spritesheet(pygame.sprite.Sprite):
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x + X_SAFEAREA, y + Y_SAFEAREA, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.y_change = 0
        self.x_change = 0

        self.facing = "down"
        self.animation_loop = 1
        
        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.move()
        self.animate()
        self.collide_enemy()
        self.rect.x += self.x_change
        self.collide_wall("x")
        self.rect.y += self.y_change
        self.collide_wall("y")

        self.y_change = 0
        self.x_change = 0
    
    def move (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += MOVE_SPEED
            self.x_change -= MOVE_SPEED
            self.facing = "left"
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= MOVE_SPEED
            self.x_change += MOVE_SPEED
            self.facing = "right"
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += MOVE_SPEED
            self.y_change -= MOVE_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= MOVE_SPEED
            self.y_change += MOVE_SPEED
            self.facing = "down"

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_wall(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                elif self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                elif self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(65, 0, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(32, 32, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(65, 32, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(65, 96, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(65, 64, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image = down_animations[0]
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(down_animations):
                    self.animation_loop = 0
        if self.facing == "up":
            if self.y_change == 0:
                self.image = down_animations[0]
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(up_animations):
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = down_animations[0]
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(left_animations):
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = down_animations[0]
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= len(right_animations):
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.y_change = 0
        self.x_change = 0

        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 40)
        
        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.move()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.y_change = 0
        self.x_change = 0
    
    def move (self):
        if self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        if self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = "left"
        
        if random.randint(1, 100) < 5:
            self.facing = random.choice(["left", "right", "up", "down"])
    def animate(self):
        left_animations = [self.game.enemy_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(65, 96, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(0, 64, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(32, 64, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(65, 64, self.width, self.height)]
        
        if self.facing == "left":
           
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= len(left_animations):
                self.animation_loop = 1
        if self.facing == "right":
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= len(right_animations):
                self.animation_loop = 1

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE


        self.image = game.terrain_spritesheet.get_sprite(957, 446, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE


        self.image = game.terrain_spritesheet.get_sprite(61, 350, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self,x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font(None, fontsize)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.content = content

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
        self.image.blit(self.text, self.text_rect)
        
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.animation_loop = 0

    def update(self):
        self.animate()
        self.collide_enemy()

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            self.kill()
            
    def animate(self):
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]
        
        if self.game.player.facing == "down":
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= len(down_animations):
                self.kill()
        if self.game.player.facing == "up":
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= len(up_animations):
                self.kill()
        if self.game.player.facing == "left":
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= len(left_animations):
                self.kill()
        if self.game.player.facing == "right":
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= len(right_animations):
                self.kill()