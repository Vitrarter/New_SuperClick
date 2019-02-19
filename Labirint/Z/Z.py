import os
import random
import pygame

pygame.init()
size = width, height = 300, 300
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


class End(pygame.sprite.Sprite):
    image = load_image('finish.png')

    def __init__(self, g):
        super().__init__(g)
        self.image = End.image
        self.rect = self.image.get_rect()
        self.rect.x = -479
        self.rect.y = -479

    def update(self):
        if self.rect.x < 0:
            self.rect = self.rect.move(1, 1)


class EndGroup(pygame.sprite.Group):
    pass


end_group = EndGroup()

running = True
end = End(end_group)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    end_group.update()
    end_group.draw(screen)
    pygame.display.flip()

pygame.quit()
