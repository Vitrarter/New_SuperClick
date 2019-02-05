import os
import pygame

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
x = 0
v = 10  # пикселей в секунду
fps = 60
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
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
                new_hero = Hero(0, 0)
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
    image_hero_d = load_image("hero_1.png")
    image_hero_a = load_image("hero_2.png")
    image_hero_w = load_image("hero_3.png")
    image_hero_s = load_image("hero_4.png")
    image_hero_attack = load_image("hero_5.png")

    def __init__(self,  pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = Hero.image_hero_d
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 100
        self.tr = False
        self.x = 0
        self.y = 0

    def update(self):
        if self.tr:
            self.rect = self.rect.move(self.x, self.y)

    def process_event_w(self, event):
        self.tr = True
        self.y = -1
        self.image = Hero.image_hero_w

    def process_event_stop(self, event):
        self.tr = False
        self.x = 0
        self.y = 0

    def process_event_s(self, event):
        self.tr = True
        self.y = 1
        self.image = Hero.image_hero_s

    def process_event_d(self, event):
        self.tr = True
        self.x = 1
        self.image = Hero.image_hero_d

    def process_event_a(self, event):
        self.tr = True
        self.x = -1
        self.image = Hero.image_hero_a

    def process_event_attack(self, event):
        self.image = Hero.image_hero_attack


class HeroGroup(pygame.sprite.Group):
    def process_event_w(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event_w(event)
            except Exception:
                pass

    def process_event_stop(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event_stop(event)
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


hero_group = pygame.sprite.Group()
all_sprites = HeroGroup()
tiles_group = pygame.sprite.Group()
camera = Camera()
hero, n, m = generate_level(load_level())
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                all_sprites.process_event_w(event)
            elif event.key == pygame.K_s:
                all_sprites.process_event_s(event)
            elif event.key == pygame.K_d:
                all_sprites.process_event_d(event)
            elif event.key == pygame.K_a:
                all_sprites.process_event_a(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            all_sprites.process_event_attack(event)
        else:
            all_sprites.process_event_stop(event)
    screen.fill((255, 255, 255))
    camera.update(hero)
    for sprite in all_sprites:
        camera.apply(sprite)
    x += v / fps
    clock.tick(fps)
    all_sprites.update()   
    tiles_group.draw(screen)
    hero_group.draw(screen)
    pygame.display.flip()

pygame.quit()
