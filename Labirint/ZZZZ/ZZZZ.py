import os
import random
import pygame

pygame.init()
size = width, height = 479, 320
screen = pygame.display.set_mode(size)


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


class Mouse(pygame.sprite.Sprite):
    image = load_image('arrow.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Mouse.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def activ(self, a):
        self.rect.x = a[0]
        self.rect.y = a[1]


class MouseGroup(pygame.sprite.Group):
    pass


running = True
mg = MouseGroup()
mouse = Mouse(mg)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse.activ(pygame.mouse.get_pos())
            pygame.mouse.set_visible(False)
    screen.fill((255, 255, 255))
    mg.draw(screen)
    pygame.display.flip()

pygame.quit()
