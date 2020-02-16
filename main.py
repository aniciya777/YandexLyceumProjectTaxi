import os
from win32api import GetSystemMetrics
import pygame
from modules.settings import SETTINGS
from modules.functions import Functions
from modules.loader import loader
from modules.menu import menu


class Game(SETTINGS, Functions):
    clock = pygame.time.Clock()
    back_color = pygame.Color('black')
    all_sprites = pygame.sprite.Group()
    rel_sprites = pygame.sprite.Group()
    cars_sprites = pygame.sprite.Group()
    callbacks = []
    tile_images = {}


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
loader(Game)
if Game.fullscrean:
    Game.real_width = GetSystemMetrics(0)
    Game.real_height = GetSystemMetrics(1)
    Game.screen = pygame.display.set_mode(Game.size(), flags=pygame.FULLSCREEN)
else:
    Game.screen = pygame.display.set_mode((Game.width, Game.height))
pygame.display.set_caption('ГоняйТакси')
menu(Game)
