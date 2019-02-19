import os
import random
import pygame

size = width, height = 400, 300
screen = pygame.display.set_mode(size)
pygame.init()

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


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(ball_sprite)
        self.radius = radius
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
        self.k = False

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Missile(pygame.sprite.Sprite):
    mimage = load_image('bomb.png')

    def __init__(self, group, pos):
        pygame.sprite.Sprite.__init__(self, group, all_sprites)
        self.image = Missile.mimage
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos

    def update(self):
        for x in pygame.sprite.spritecollide(self, ball_sprite, True):
            print(x)
            score.inc()

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.score = 0
        self.font = pygame.font.Font(None, 50)
        text = self.font.render(str(self.score), 1, (100, 255, 100))
        self.image = text
        self.rect = self.image.get_rect()
        self.pos = 370, 30
        self.rect.center = self.pos

    def inc(self):
        self.score += 1

    def update(self):
        text = self.font.render(str(self.score), 1, (100, 255, 100))
        self.image = text
        self.rect = self.image.get_rect()
        self.pos = 370, 30
        self.rect.center = self.pos


# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()

ball_sprite = pygame.sprite.Group()
arrow_sprite = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

sp = pygame.sprite.Group()
score = Score()

Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

for i in range(10):
    Ball(20, 100, 100)

# добавлем объект стрелка и  загружаем для него изображение

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            missile = Missile(sp, event.pos)
    screen.fill(pygame.Color("white"))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()