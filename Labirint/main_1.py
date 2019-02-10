import os
import pygame

pygame.init()
size = width, height = 1266, 668
screen = pygame.display.set_mode(size)
x = 0
v = 30  # пикселей в секунду
fps = 60
clock = pygame.time.Clock()
d = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('sand.png')
}
tile_width = tile_height = 400


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(wall_group, tiles_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def load_level():
    filename = "data.txt"
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_hero, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_hero = Hero(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_hero, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, hero):
        hero.rect.x += self.dx
        hero.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Hero(pygame.sprite.Sprite):
    image_hero_d = load_image("bomb_2.png")
    image_hero_a = load_image("bomb.png")
    image_hero_w = load_image("bomb_2.png")
    image_hero_s = load_image("bomb.png")
    image_hero_attack = load_image("boom.png")

    def __init__(self, pos_x=0, pos_y=0):
        super().__init__(hero_group, all_sprites)
        self.image = Hero.image_hero_d
        self.rect = self.image.get_rect()
        self.start_x = tile_width * pos_x
        self.start_y = tile_height * pos_y
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        # self.tr = False
        # self.wall = True
        # self.x = p_x
        # self.y = p_y
        self.dx = 0
        self.dy = 0
        self.smash_x = 0
        self.smash_y = 0

    def update(self):
        # if self.tr and self.wall:
        #     self.rect = self.rect.move(self.x, self.y)
        #     Hero.collide(self, event)
        # elif not self.wall and self.tr:
        self.rect = self.rect.move(self.smash_x, self.smash_y)
        if self.collide():
            self.process_event_stop()
            self.smash_x = self.smash_y = 0
        else:
            self.dx += self.smash_x
            self.dy += self.smash_y

    def collide(self):
        for tile in wall_group:
            if pygame.sprite.collide_rect(self, tile):
                return True
        return False

    def process_event_stop(self):
        # self.tr = False
        self.rect.x -= self.dx
        self.rect.y -= self.dy
        self.dx = self.dy = 0

    def process_event_w(self, event):
        # self.tr = True
        if event.type == pygame.KEYDOWN:
            self.smash_y += -10
            self.image = Hero.image_hero_w
        else:
            self.smash_y -= -10

    def process_event_s(self, event):
        # self.tr = True
        if event.type == pygame.KEYDOWN:
            self.smash_y += 10
            self.image = Hero.image_hero_s
        else:
            self.smash_y -= 10

    def process_event_d(self, event):
        # self.tr = True
        if event.type == pygame.KEYDOWN:
            self.smash_x += 10
            self.image = Hero.image_hero_d
        else:
            self.smash_x -= 10

    def process_event_a(self, event):
        # self.tr = True
        if event.type == pygame.KEYDOWN:
            self.smash_x += -10
            self.image = Hero.image_hero_a
        else:
            self.smash_x -= -10

    def process_event_attack(self, event):
        self.image = Hero.image_hero_attack


class HeroGroup(pygame.sprite.Group):
    def collide(self, event):
        for sprite in self.sprites():
            try:
                sprite.collide(event)
            except Exception:
                pass

    def process_event_w(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event_w(event)
            except Exception:
                pass

    def process_event_stop(self):
        for sprite in self.sprites():
            try:
                sprite.process_event_stop()
            except Exception:
                pass

    def process_event_s(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event_s(event)
            except Exception:
                pass

    def process_event_d(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event_d(event)
            except Exception:
                pass

    def process_event_a(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event_a(event)
            except Exception:
                pass

    def process_event_attack(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event_attack(event)
            except Exception:
                pass


class TileGroup(pygame.sprite.Group):
    pass


# platforms = []
all_sprites = pygame.sprite.Group()
hero_group = HeroGroup()
tiles_group = TileGroup()
wall_group = TileGroup()

camera = Camera()
hero, n, m = generate_level(load_level())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                hero_group.process_event_w(event)
            elif event.key == pygame.K_s:
                hero_group.process_event_s(event)
            elif event.key == pygame.K_d:
                hero_group.process_event_d(event)
            elif event.key == pygame.K_a:
                hero_group.process_event_a(event)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                hero_group.process_event_w(event)
            elif event.key == pygame.K_s:
                hero_group.process_event_s(event)
            elif event.key == pygame.K_d:
                hero_group.process_event_d(event)
            elif event.key == pygame.K_a:
                hero_group.process_event_a(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            hero_group.process_event_attack(event)
        # else:
        #     hero_group.process_event_stop(event)
    screen.fill((255, 255, 255))
    print(hero.start_x, hero.start_y)
    print(hero.rect.x, hero.rect.y)
    all_sprites.update()
    print(hero.rect.x, hero.rect.y)
    camera.update(hero)
    print(hero.rect.x, hero.rect.y)
    for sprite in all_sprites:
        camera.apply(sprite)
    print(hero.rect.x, hero.rect.y)
    tiles_group.draw(screen)
    hero_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
