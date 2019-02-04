import os
import pygame

pygame.init()
size = width, height = 101, 600
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
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Bomb(pygame.sprite.Sprite):
    image_bomb = load_image("sprite.png")

    def __init__(self, group, y):
        super().__init__(group)
        self.image = Bomb.image_bomb
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0 + y * 200
        self.tr = False

    def update(self):
        if self.tr:
            self.rect = self.rect.move(-1, 0)

    def process_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.tr = True


class BombGroup(pygame.sprite.Group):
    def process_event(self, event):
        for sprite in self.sprites():
            try:
                sprite.process_event(event)
            except Exception:
                pass


all_sprites = BombGroup()

bomb = Bomb(all_sprites, 0)
bomb_1 = Bomb(all_sprites, 1)
bomb_2 = Bomb(all_sprites, 2)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_sprites.process_event(event)
    screen.fill((255, 255, 255))
    x += v / fps
    clock.tick(fps)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
