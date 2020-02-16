import os
import pygame
import numpy
import json
from win32api import GetSystemMetrics

class Functions:
    @classmethod
    def quit(cls, *args):
        pygame.quit()
        config = {
            'status': cls.status,
            'firm': cls.firm,
            'fps': cls.fps,
            'fullscreen': 'on' if cls.fullscrean else 'off'
        }
        with open('data/config.json', 'w') as file:
            file.write(json.dumps(config))
        exit(0)

    @staticmethod
    def load_image(name, colorkey=None, size=None, scale=True, colorfill=None):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname).convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        if size:
            rect = image.get_rect()
            size = list(size)
            if size[1] is None:
                scale_x = size[0] / rect.width
                size[1] = (rect.height * scale_x)
            elif size[0] is None:
                scale_y = size[1] / rect.height
                size[0] = (rect.width * scale_y)
            if not scale:
                scale_x = size[0] / rect.width
                scale_y = size[1] / rect.height
                min_scale = min(scale_x, scale_y)
                width2 = round(rect.width * min_scale)
                height2 = round(rect.height * min_scale)
                image2 = pygame.transform.scale(image, (width2, height2))
                image = pygame.Surface(size, pygame.SRCALPHA)
                if colorfill:
                    image.fill(pygame.Color(colorfill))
                else:
                    image.fill(pygame.transform.average_color(image2))
                padding_left = (size[0] - width2) / 2
                padding_top = (size[1] - height2) / 2
                image.blit(image2, (padding_left, padding_top))
            else:
                image = pygame.transform.scale(image, size)
        return image

    @staticmethod
    def grayscale(img):
        arr = pygame.surfarray.array3d(img)
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
        arr = numpy.array([[[avg, avg, avg] for avg in col] for col in avgs])
        return pygame.surfarray.make_surface(arr)

    @classmethod
    def _coord(cls, pos):
        if cls.fullscrean:
            x, y = pos
            if not (x is None):
                x = (pos[0] * cls.real_width / cls.width)
            if not (y is None):
                y = (pos[1] * cls.real_height / cls.height)
            return x, y
        return pos

    @classmethod
    def _rect(cls, rect):
        return pygame.rect.Rect(
            *cls._coord(rect[:2]),
            *cls._coord(rect[2:])
        )

    @classmethod
    def size(cls):
        return cls.real_width, cls.real_height

    @classmethod
    def update(cls, *events):
        cls.screen.fill(cls.back_color)
        cls.all_sprites.draw(cls.screen)
        cls.all_sprites.update(events, cls)
        for i in range(len(cls.callbacks) - 1, -1, -1):
            callback = cls.callbacks[i]
            del cls.callbacks[i]
            callback(cls)

    @classmethod
    def tick(cls):
        t = cls.clock.tick(cls.fps)
        cls.fps_real = cls.fps_real * (1 - cls.FPS_COEFF) + cls.FPS_COEFF * (1000 / t)
        print(f'\rFPS:\t{round(cls.fps_real)}', end='')

    @classmethod
    def get_level(cls):
        return 1

    @staticmethod
    def load_level(filename):
        filename = f'data/levels/{filename}.txt'
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r', encoding='utf-8') as mapFile:
            level_map = [line.strip() for line in mapFile]
        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))
        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    @classmethod
    def set_mode(cls):
        if cls.fullscrean:
            cls.real_width = GetSystemMetrics(0)
            cls.real_height = GetSystemMetrics(1)
            cls.screen = pygame.display.set_mode(cls.size(), flags=pygame.FULLSCREEN)
        else:
            cls.screen = pygame.display.set_mode((cls.width, cls.height))
            cls.real_width = cls.width
            cls.real_height = cls.height
