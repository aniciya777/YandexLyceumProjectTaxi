import pygame
from modules.settings_form import settings_form
from modules.game import game


class MenuBanner(pygame.sprite.Sprite):
    def __init__(self, Game, *group):
        super().__init__(*group)
        self.image = Game.load_image('images/menu.png', None, Game.size(), False, '#111111')
        self.rect = self.image.get_rect()


class Buttons(pygame.sprite.Sprite):
    def update(self, *args):
        for event in args[0]:
            if event and event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.click(*args)

    def click(self, *args):
        pass


class NewGameButton(Buttons):
    def __init__(self, Game, *group):
        super().__init__(*group)
        self.image = Game.load_image('images/buttons/new game.png', -1, Game._coord((250, None)), False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Game._coord((300, 50))

    def click(self, *args):
        args[1].running = False
        args[1].callbacks.append(game)


class SettingsButton(Buttons):
    def __init__(self, Game, *group):
        super().__init__(*group)
        self.image = Game.load_image('images/buttons/settings.png', -1, Game._coord((250, None)), False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Game._coord((300, 150))

    def click(self, *args):
        args[1].callbacks.append(settings_form)
        args[1].running = False


class ExitButton(Buttons):
    def __init__(self, Game, *group):
        super().__init__(*group)
        self.image = Game.load_image('images/buttons/exit.png', -1, Game._coord((250, None)), False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Game._coord((300, 250))

    def click(self, *args):
        args[1].callbacks.append(args[1].quit)
        args[1].running = False


def menu(Game):
    Game.back_color = pygame.Color('black')
    Game.all_sprites.empty()
    MenuBanner(Game, Game.all_sprites)
    NewGameButton(Game, Game.all_sprites)
    SettingsButton(Game, Game.all_sprites)
    ExitButton(Game, Game.all_sprites)
    Game.running = True
    while Game.running:
        event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
        Game.update(event)
        pygame.display.flip()
        Game.tick()
