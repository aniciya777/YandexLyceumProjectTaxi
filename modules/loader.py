import pygame


WIDTH = 400
HEIGHT = 300
TIMER = 3

class LoaderBanner(pygame.sprite.Sprite):
    def __init__(self, Game, *group):
        super().__init__(*group)
        self.image = Game.load_image('images/loader.png')
        self.rect = self.image.get_rect()


def loader(Game):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.NOFRAME)
    all_sprites = pygame.sprite.Group()
    LoaderBanner(Game, all_sprites)
    running = True
    screen.fill(Game.back_color)
    all_sprites.draw(screen)
    pygame.display.flip()
    timer = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return 0
        Game.tick()
        timer += 1 / Game.fps
        if timer > TIMER:
            return 0
