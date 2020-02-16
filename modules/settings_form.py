import pygame
import modules


class Label(pygame.sprite.Sprite):
    def __init__(self, Game, *args):
        super().__init__(*args)
        self.color = pygame.Color(255, 255, 2)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.game = Game

    def print(self, text, size=22):
        size = self.game._coord((size, size))[0]
        self.font = pygame.font.Font('data/fonts/Roboto-Medium.ttf', round(size))
        self.image = self.font.render(text, 1, self.color)
        self.rect = self.image.get_rect()
        return self

    def move(self, x, y):
        self.rect.x, self.rect.y = self.game._coord((x, y))
        return self


class Buttons(pygame.sprite.Sprite):
    def __init__(self, Game, *args):
        super().__init__(*args)
        self.image = self.get_image()
        self.rect = self.image.get_rect()

    def get_image(self):
        if self.status:
            return self.image_orig
        try:
            return self.image_gray
        except:
            return self.image_orig

    def update(self, *args):
        self.image = self.get_image()
        for event in args[0]:
            if event and event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.click(*args)

    def click(self, *args):
        pass


class BackToMenuButton(Buttons):
    def __init__(self, Game, *group):
        self.status = True
        self.image_orig = Game.load_image('images/buttons/back to menu.png', -1,
                                          Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((425, 325))

    def click(self, *args):
        args[1].callbacks.append(modules.menu.menu)
        args[1].running = False


class StatusButton(Buttons):
    def __init__(self, Game, *group):
        self.status = Game.status == self.const
        super().__init__(Game, *group)

    def update(self, *args):
        super().update(*args)
        self.status = args[1].status == self.const

    def click(self, *args):
        args[1].status = self.const


class ContestButton(StatusButton):
    def __init__(self, Game, *group):
        self.const = Game.STATUS_CONTEST
        self.image_orig = Game.load_image('images/buttons/contest.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/contest_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((25, 100))


class FreeButton(StatusButton):
    def __init__(self, Game, *group):
        self.const = Game.STATUS_FREE
        self.image_orig = Game.load_image('images/buttons/free.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/free_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((25, 150))


class WindowModeButton(Buttons):
    def __init__(self, Game, *group):
        self.status = Game.fullscrean
        super().__init__(Game, *group)

    def update(self, *args):
        super().update(*args)
        self.status = args[1].fullscrean == self.const

    def click(self, *args):
        args[1].fullscrean = self.const
        args[1].set_mode()
        args[1].callbacks.append(modules.settings_form.settings_form)
        args[1].running = False


class OnWindowButton(WindowModeButton):
    def __init__(self, Game, *group):
        self.const = False
        self.image_orig = Game.load_image('images/buttons/on_window.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/on_window_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((25, 250))


class FullScreenButton(WindowModeButton):
    def __init__(self, Game, *group):
        self.const = True
        self.image_orig = Game.load_image('images/buttons/fullscreen.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/fullscreen_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((25, 300))


class TaxiButton(Buttons):
    def __init__(self, Game, *group):
        self.status = Game.firm == self.const
        super().__init__(Game, *group)

    def update(self, *args):
        super().update(*args)
        self.status = args[1].firm == self.const

    def click(self, *args):
        args[1].firm = self.const


class YandexTaxiButton(TaxiButton):
    def __init__(self, Game, *group):
        self.const = 0
        self.image_orig = Game.load_image('images/buttons/yandex.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/yandex_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((225, 100))


class UberButton(TaxiButton):
    def __init__(self, Game, *group):
        self.const = 1
        self.image_orig = Game.load_image('images/buttons/uber.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/uber_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((225, 150))


class RuTaxiButton(TaxiButton):
    def __init__(self, Game, *group):
        self.const = 2
        self.image_orig = Game.load_image('images/buttons/rutaxi.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/rutaxi_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((225, 200))


class MaximButton(TaxiButton):
    def __init__(self, Game, *group):
        self.const = 3
        self.image_orig = Game.load_image('images/buttons/maxim.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image('images/buttons/maxim_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((225, 250))


class FpsButton(Buttons):
    def __init__(self, Game, *group):
        self.status = Game.fps == self.const
        self.image_orig = Game.load_image(f'images/buttons/{self.const}.png',
                                          -1, Game._coord((150, None)), False)
        self.image_gray = Game.load_image(f'images/buttons/{self.const}_gray.png',
                                          -1, Game._coord((150, None)), False)
        super().__init__(Game, *group)

    def update(self, *args):
        super().update(*args)
        self.status = args[1].fps == self.const

    def click(self, *args):
        args[1].fps = self.const


class Fps10Button(FpsButton):
    def __init__(self, Game, *group):
        self.const = 10
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((425, 100))


class Fps20Button(FpsButton):
    def __init__(self, Game, *group):
        self.const = 20
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((425, 150))


class Fps30Button(FpsButton):
    def __init__(self, Game, *group):
        self.const = 30
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((425, 200))


class Fps60Button(FpsButton):
    def __init__(self, Game, *group):
        self.const = 60
        super().__init__(Game, *group)
        self.rect.x, self.rect.y = Game._coord((425, 250))


def settings_form(Game):
    Game.back_color = pygame.Color('black')
    Game.all_sprites.empty()
    Game.all_sprites.add(Label(Game).print('РЕЖИМ').move(60, 60))
    BackToMenuButton(Game, Game.all_sprites)
    ContestButton(Game, Game.all_sprites)
    FreeButton(Game, Game.all_sprites)
    Game.all_sprites.add(Label(Game).print('ОТОБРАЖЕНИЕ').move(18, 210))
    OnWindowButton(Game, Game.all_sprites)
    FullScreenButton(Game, Game.all_sprites)
    Game.all_sprites.add(Label(Game).print('ФИРМА').move(260, 60))
    YandexTaxiButton(Game, Game.all_sprites)
    UberButton(Game, Game.all_sprites)
    RuTaxiButton(Game, Game.all_sprites)
    MaximButton(Game, Game.all_sprites)
    Game.all_sprites.add(Label(Game).print('FPS').move(480, 60))
    Fps10Button(Game, Game.all_sprites)
    Fps20Button(Game, Game.all_sprites)
    Fps30Button(Game, Game.all_sprites)
    Fps60Button(Game, Game.all_sprites)
    Game.running = True
    while Game.running:
        event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game.running = False
                    Game.callbacks.append(modules.menu.menu)
        Game.update(event)
        pygame.display.flip()
        Game.tick()
