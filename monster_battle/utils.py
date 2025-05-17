import pygame
from os.path import join
from os import walk

def import_image(*path, format = 'png', alpha= True):
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def import_audio():
    audio_dict = {}
    for path, _, files in walk(join("assets", "audio")):
       for file in sorted(files):
          full_path = join(path, file)
          audio_dict[file.split('.')[0]] = pygame.mixer.Sound(full_path)
    return audio_dict

def tile_importer(cols, *path):
    attack_frames = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path).convert_alpha()
            attack_frames[file_name.split('.')[0]] = []
            cutout_width = surf.get_width() / cols
            for col in range(cols):
                cutout_surf = pygame.Surface((cutout_width, surf.get_height()), pygame.SRCALPHA)
                cutout_rect = pygame.FRect(cutout_width * col, 0, cutout_width, surf.get_height())
                cutout_surf.blit(surf, (0,0), cutout_rect)
                attack_frames[file_name.split('.')[0]].append(cutout_surf)
    return attack_frames