import pygame
import modules
import random


class Label(pygame.sprite.Sprite):
    def __init__(self, Game, *args):
        super().__init__(*args)
        self.color = pygame.Color(255, 255, 2)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.game = Game

    def print(self, text, size=None):
        self.size = size
        if size is None:
            self.size = 22
        self.size = self.game._coord((self.size, self.size))[0]
        self.font = pygame.font.Font('data/fonts/Roboto-Medium.ttf', round(self.size))
        self.image = self.font.render(text, 1, self.color)
        self.rect = self.image.get_rect()
        return self

    def move(self, x, y):
        self.rect.x, self.rect.y = self.game._coord((x, y))
        return self


class Tile(pygame.sprite.Sprite):
    def __init__(self, Game, tile_type, pos_x, pos_y):
        super().__init__(Game.all_sprites, Game.rel_sprites)
        self.image = Game.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            Game._coord((
                Game.CELL_SIZE[0] * (pos_x - pos_y / 2),
                Game.CELL_SIZE[1] * pos_y / 2
            ))
        )
        self.rect.y -= self.rect.h - Game.CELL_SIZE[1]


class BackTile(Tile):
    def __init__(self, Game, tile_type, pos_x, pos_y):
        if tile_type is None:
            tile_type = random.choice(['back_1', 'back_2', 'back_3', 'back_4', 'back_5', 'back_6'])
        super().__init__(Game, tile_type, pos_x, pos_y)


class BuildTile(BackTile):
    def __init__(self, Game, tile_type, pos_x, pos_y):
        super().__init__(Game, tile_type, pos_x, pos_y)

class RoadTile(Tile):
    def __init__(self, Game, tile_type, pos_x, pos_y):
        if tile_type is None:
            tile_type = random.choice(['road_1'])
        super().__init__(Game, tile_type, pos_x, pos_y)


class RoadParkingTile(RoadTile):
    def __init__(self, Game, tile_type, pos_x, pos_y):
        if tile_type is None:
            tile_type = random.choice(['road_1'])
        super().__init__(Game, tile_type, pos_x, pos_y)


class RoadAroundBuildingTile(RoadParkingTile):
    def __init__(self, Game, tile_type, pos_x, pos_y):
        if tile_type is None:
            tile_type = random.choice(['road_1'])
        super().__init__(Game, tile_type, pos_x, pos_y)


class Car(pygame.sprite.Sprite):
    TOP_LEFT = 4
    TOP_RIGHT = 8
    BOTTOM_LEFT = 0
    BOTTOM_RIGHT = 12
    SPEED_COEFF = 0.2
    SPEED_ADD = 0.05

    def __init__(self, Game, firm, pos_x, pos_y):
        super().__init__(Game.all_sprites, Game.rel_sprites)
        self.game = Game
        self.speed_add = self.SPEED_ADD * Game.CELL_SIZE[0]
        self.color = self.get_color(firm)
        s = self.get_index()
        self.tile_type = self.get_type()
        self.images = []
        for i in range(1 + self.tile_type * 16, 1 + self.tile_type * 16 + 16):
            i_s = str(i)
            i_s = i_s.rjust(4, '0')
            self.images.append(Game.load_image(f'images\\vehicles\\{self.color}\\c{s}_s128_iso_{i_s}.png',
                                               -1, Game._coord((Game.CELL_SIZE[0], Game.CELL_SIZE[1])), False))
        self.direction = Car.BOTTOM_LEFT
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect().move(
            Game._coord((
                Game.CELL_SIZE[0] * (pos_x - pos_y / 2),
                Game.CELL_SIZE[1] * pos_y / 2
            ))
        )
        self.rect.y -= self.rect.h - Game.CELL_SIZE[1]
        self.x = self.rect.x
        self.y = self.rect.y

    def get_color(self, firm):
        if firm == 0:  # 'Яндекс.Такси'
            return 'yellow'
        if firm == 1:  # 'Uber'
            return random.choice(['black', 'blue', 'grey', 'white'])
        if firm == 2:  # 'Rutaxi'
            return random.choice(['pink', 'red'])
        if firm == 3:  # 'Maxim'
            return 'orange'

    def get_type(self):
        return random.randint(0, 13)

    def get_index(self):
        if self.color == 'black':
            return '07'
        if self.color == 'blue':
            return '02'
        if self.color == 'green':
            return '05'
        if self.color == 'grey':
            return '04'
        if self.color == 'orange':
            return '11'
        if self.color == 'pink':
            return '08'
        if self.color == 'purple':
            return '12'
        if self.color == 'red':
            return '01'
        if self.color == 'white':
            return '09'
        if self.color == 'yellow':
            return '10'

    def set_direction(self, direction):
        self.direction = direction
        self.image = self.images[direction]


class CarPlayer(Car):
    def __init__(self, Game, pos_x, pos_y):
        super().__init__(Game, Game.firm, pos_x, pos_y)
        self.dx = 0
        self.dy = 0
        self.running = False

    def go_top(self):
        if self.direction == self.BOTTOM_LEFT:
            self.set_direction(self.TOP_LEFT)
        elif self.direction == self.BOTTOM_RIGHT:
            self.set_direction(self.TOP_RIGHT)

    def go_bottom(self):
        if self.direction == self.TOP_LEFT:
            self.set_direction(self.BOTTOM_LEFT)
        elif self.direction == self.TOP_RIGHT:
            self.set_direction(self.BOTTOM_RIGHT)

    def go_left(self):
        if self.direction == self.TOP_RIGHT:
            self.set_direction(self.TOP_LEFT)
        elif self.direction == self.BOTTOM_RIGHT:
            self.set_direction(self.BOTTOM_LEFT)

    def go_right(self):
        if self.direction == self.TOP_LEFT:
            self.set_direction(self.TOP_RIGHT)
        elif self.direction == self.BOTTOM_LEFT:
            self.set_direction(self.BOTTOM_RIGHT)

    def run(self):
        self.running = True

    def stop(self):
        self.running = False

    def go(self):
        sp_add = self.speed_add / self.game.fps
        sp_add = self.game._coord((sp_add, None))[0]
        if self.direction == self.TOP_LEFT:
            self.dx -= sp_add
            self.dy -= sp_add / 2
        elif self.direction == self.TOP_RIGHT:
            self.dx += sp_add
            self.dy -= sp_add / 2
        elif self.direction == self.BOTTOM_LEFT:
            self.dx -= sp_add
            self.dy += sp_add / 2
        elif self.direction == self.BOTTOM_RIGHT:
            self.dx += sp_add
            self.dy += sp_add / 2

    def update(self, *args):
        self.dx *= self.SPEED_COEFF ** (1 / self.game.fps)
        self.dy *= self.SPEED_COEFF ** (1 / self.game.fps)
        if self.running:
            self.go()
        # TODO
        self.x += self.dx
        self.y += self.dy
        self.rect.x += int(self.x)
        self.rect.y += int(self.y)
        self.x -= int(self.x)
        self.y -= int(self.y)


class CarBot(Car):
    def __init__(self, Game, firm, pos_x, pos_y):
        super().__init__(Game, firm, pos_x, pos_y)


class Board:
    # создание поля
    def __init__(self, Game):
        self.game = Game
        self.board = Game.load_level(Game.level)
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.player = self.generate_level()
        self.cell_size = Game.CELL_SIZE

    def generate_level(self):
        free_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == '#':
                    BuildTile(self.game, 'build_1', x, y)
                elif self.board[y][x] == '.':
                    BackTile(self.game, None, x, y)
                else:
                    free_cells.append((x, y))
                    if self.board[y][x] == ' ':
                        RoadTile(self.game, None, x, y)
                    elif self.board[y][x] == 'П':
                        RoadParkingTile(self.game, None, x, y)
                    elif self.board[y][x] == '*':
                        RoadAroundBuildingTile(self.game, None, x, y)
        new_player = CarPlayer(self.game, *free_cells[0])
        return new_player


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)


def load_tiles(Game):
    Game.tile_images['build_1'] = Game.load_image(r'images\tiles\buildings\1.png',
                                                  -1, Game._coord((Game.CELL_SIZE[0], None)), False)
    Game.tile_images['back_1'] = Game.load_image(r'images\tiles\back\1.png',
                                                  -1, Game._coord((Game.CELL_SIZE[0], None)), False)
    Game.tile_images['back_2'] = Game.load_image(r'images\tiles\back\2.png',
                                                 -1, Game._coord((Game.CELL_SIZE[0], None)), False)
    Game.tile_images['back_3'] = Game.load_image(r'images\tiles\back\3.png',
                                                 -1, Game._coord((Game.CELL_SIZE[0], None)), False)
    Game.tile_images['back_4'] = Game.load_image(r'images\tiles\back\4.png',
                                                 -1, Game._coord((Game.CELL_SIZE[0], None)), False)
    Game.tile_images['back_5'] = Game.load_image(r'images\tiles\back\5.png',
                                                 -1, Game._coord((Game.CELL_SIZE[0], None)), False)
    Game.tile_images['back_6'] = Game.load_image(r'images\tiles\back\6.png',
                                                 -1, Game._coord((Game.CELL_SIZE[0], None)), False)
    Game.tile_images['road_1'] = Game.load_image(r'images\tiles\road\1.png',
                                                 -1, Game._coord((Game.CELL_SIZE[0], None)), False)


def game(Game):
    Game.back_color = pygame.Color(126, 206, 97)
    camera = Camera(Game.real_width, Game.real_height)
    load_tiles(Game)
    Game.all_sprites.empty()
    Game.rel_sprites.empty()
    Game.level = Game.get_level()
    Game.board = Board(Game)
    player1 = Game.board.player
    player2 = Game.board.player
    fps_label = Label(Game, Game.all_sprites)

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
                elif event.key == pygame.K_UP:
                    player1.go_top()
                elif event.key == pygame.K_DOWN:
                    player1.go_bottom()
                elif event.key == pygame.K_LEFT:
                    player1.go_left()
                elif event.key == pygame.K_RIGHT:
                    player1.go_right()
                elif event.key == pygame.K_w:
                    player2.go_top()
                elif event.key == pygame.K_s:
                    player2.go_bottom()
                elif event.key == pygame.K_a:
                    player2.go_left()
                elif event.key == pygame.K_d:
                    player2.go_right()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT:
                    if event.type == pygame.KEYDOWN:
                        player1.run()
                    else:
                        player1.stop()
                elif event.key == pygame.K_LSHIFT:
                    if event.type == pygame.KEYDOWN:
                        player2.run()
                    else:
                        player2.stop()
        fps_label.print(str(round(Game.fps_real)), 15).move(5, 380)
        Game.update(event)
        # изменяем ракурс камеры
        camera.update(Game.board.player);
        # обновляем положение всех спрайтов
        for sprite in Game.rel_sprites:
            camera.apply(sprite)
        pygame.display.flip()
        Game.tick()
