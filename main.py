import pygame
from sprites import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Test Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.character_spritesheet = Spritesheet('assets/character.png')
        self.terrain_spritesheet = Spritesheet('assets/terrain.png')
        self.enemy_spritesheet = Spritesheet('assets/enemy.png')

    def createTileMap(self):
        for y, row in enumerate(TILE_MAP):
            for x, tile in enumerate(row):
                Ground(self, x, y)
                if tile == 'E':
                    Enemy(self, x, y)
                if tile == 'W':
                    Wall(self, x, y)
                if tile == 'p':
                    self.player = Player(self, x, y)
                    self.player.move()
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.createTileMap()
        
    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def game_over(self):
        pass

    def intro_screen(self):
        pass

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
           
        self.running = False

        pygame.quit()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
