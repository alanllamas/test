import pygame
from config import *
from pytmx.util_pygame import load_pygame
from os.path import join
from sprites import *
from groups import *
from os import walk
from random import *
from timers import *


def import_image(*path, format = 'png', alpha= True):
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for path, subfolders, files in walk(join(*path)):
       for file in sorted(files, key = lambda name: int(name.split('.')[0])):
          full_path = join(path, file)
          frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

def import_audio():
    audio_dict = {}
    for path, _, files in walk(join("assets", "audio")):
       for file in sorted(files):
          full_path = join(path, file)
          audio_dict[file.split('.')[0]] = pygame.mixer.Sound(full_path)
    return audio_dict

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Game")
        self.setup()

    def setup(self):
        self.all_sprites = AllSprites()
        self.tile_sprites = pygame.sprite.Group()
        self.collition_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_assets()
        self.set_timers()
        self.draw_sprites()

    def set_timers(self):
       self.bee_timer = Timer(200, self.create_bee, autoStart=True, repeat=True)

    def play_audio(self, file_name, volume = .2):
        self.audio[file_name].set_volume(volume)
        self.audio[file_name].play()
    
    def load_assets(self):
        self.map = load_pygame(join("assets", "data", "maps", "world.tmx"))
        self.player_frames = import_folder("assets", "images", "player")
        self.bee_frames = import_folder("assets", "images", "enemies", "bee")
        self.worm_frames = import_folder("assets", "images", "enemies", "worm")
        self.bullet_image = import_image("assets", "images", "gun", "bullet")
        self.fire_image = import_image("assets", "images", "gun", "fire")
        self.audio = import_audio()
        print(self.audio)

    def draw_sprites(self):
        for x, y, image in self.map.get_layer_by_name("Main").tiles():
          Tile((self.all_sprites, self.tile_sprites, self.collition_sprites), (x, y), image)
        
        for x, y, image in self.map.get_layer_by_name("Decoration").tiles():
          Tile((self.all_sprites, self.tile_sprites), (x, y), image)
        
        for sprite in self.map.get_layer_by_name("Entities"):
          if sprite.name == 'Player':
            self.player = Player((self.all_sprites, self.player_sprites), (sprite.x, sprite.y), self.player_frames, self.collition_sprites, self.create_bullet)
          if sprite.name == 'Worm':
            Worm((self.all_sprites, self.enemy_sprites), (sprite.x, sprite.y), self.worm_frames, self.collition_sprites)
    
    def create_bullet(self, pos, direction):
      x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_image.get_width()
      Bullet((self.all_sprites, self.bullet_sprites), (x, pos[1]), self.bullet_image, direction)
      Fire((self.all_sprites), pos,  self.fire_image, self.player)


    def create_bee(self):
        print('create bee')
        x = randint(200, 600)
        y = randint(200, 600)
        Bee((self.all_sprites, self.enemy_sprites), (x, y), self.bee_frames, self.collition_sprites)
       
    def update(self, dt):
        self.all_sprites.update(dt)
        pygame.display.flip()
        self.bee_timer.update()
        self.screen.fill((200, 200, 200))

    def run(self):
        # self.play_audio('music')
        dt = self.clock.tick(FPS) / 1000
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update(dt)
            self.all_sprites.draw_camera(self.player.rect.center)


        pygame.quit()
if __name__ == "__main__":
    game = Game()
    game.run()