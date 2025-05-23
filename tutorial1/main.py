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
        self.attack_spritesheet = Spritesheet('assets/attack.png')
        self.font = pygame.font.Font("arial.ttf", 32)
        self.intro_background = pygame.image.load("assets/introbackground.png")
        self.gameover_background = pygame.image.load("assets/gameover.png")

    def createTileMap(self, map, x_index=0, y_index=0):
        for y, row in enumerate(map):
            for x, tile in enumerate(row):
                Ground(self, x + (x_index * 20), y + (y_index * 15))
                if tile == 'E':
                    Enemy(self, x + (x_index * 20), y + (y_index * 15))
                if tile == 'W':
                    Wall(self, x + (x_index * 20), y + (y_index * 15))
                if tile == 'p':
                    self.player = Player(self, x + (x_index * 20), y + (y_index * 15))
                    self.player.move()
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        
        for y, tile_rows in enumerate(TILE_MAPS):
            for x, tile in enumerate(tile_rows):
                self.createTileMap(tile, x, y)
        # self.createTileMap(TILE_MAP_B,1, 0)
        
    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "right":
                        self.player.attack = Attack(self, self.player.rect.x + TILE_SIZE, self.player.rect.y)
                    if self.player.facing == "left":
                        self.player.attack = Attack(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                    if self.player.facing == "up":    
                        self.player.attack = Attack(self, self.player.rect.x, self.player.rect.y - TILE_SIZE)
                    if self.player.facing == "down":
                        self.player.attack = Attack(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def game_over(self):
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_button = Button(10, SCREEN_HEIGHT -60, 120, 50, WHITE, BLACK, "Restart", 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_click):
                self.new()
                self.main()

            self.screen.blit(self.gameover_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        title = self.font.render("Welcome to the Game", True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        play_button= Button(10, 50,100, 50, WHITE, BLACK, "Play", 32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_click):
                intro = False
            
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
           
           

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
