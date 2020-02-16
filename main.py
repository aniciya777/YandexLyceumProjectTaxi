import os
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
    border_top_left_sprites = pygame.sprite.Group()
    border_top_right_sprites = pygame.sprite.Group()
    border_bottom_left_sprites = pygame.sprite.Group()
    border_bottom_right_sprites = pygame.sprite.Group()
    callbacks = []
    tile_images = {}


try:
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    loader(Game)
    Game.set_mode()
    pygame.display.set_caption('ГоняйТакси')
    menu(Game)
except SystemExit:
    Game.quit()
