import pygame
from math import sqrt
from scripts.collision import maskcollide, zerodiv
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

fps = 60
frame_time = 0.016
physics_quality = 1  # 1 - the best quality, <... worse

running = True
clock = pygame.time.Clock()


class ColGeom:
    def __init__(self, mask, position):
        self.mask = mask
        self.rect = mask.get_bounding_rects()[0]
        self.move(position)

    def move(self, pos):
        self.rect = self.rect.move(pos[0], pos[1])
        self.center = self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2


def load_mask(name, color_key=None):
    try:
        image = pygame.image.load(name)
    except pygame.error:
        return None

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


img1 = ColGeom(pygame.mask.from_surface(load_mask('test_mask1.png', color_key=-1)), (0, 0))
img2 = ColGeom(pygame.mask.from_surface(load_mask('test_mask2.png', color_key=-1)), (200, 200))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        img1.move((0, -1))
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        img1.move((0, 1))
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        img1.move((1, 0))
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        img1.move((-1, 0))

    screen.fill(pygame.Color('black'))
    overlap = pygame.sprite.collide_mask(img1, img2)
    olist1 = [(img1.rect.x + point[0], img1.rect.y + point[1]) for point in img1.mask.outline()]
    olist2 = [(img2.rect.x + point[0], img2.rect.y + point[1]) for point in img2.mask.outline()]
    pygame.draw.lines(screen, (255, 255, 255), 2, olist1)
    pygame.draw.lines(screen, (255, 255, 255), 2, olist2)
    pygame.draw.circle(screen, pygame.color.Color('white'), img1.center, 2, 0)
    pygame.draw.circle(screen, pygame.color.Color('white'), img2.center, 2, 0)
    if overlap:
        overlap = maskcollide(img1, img2)
        overlap_rect = overlap.get_bounding_rects()[0]
        overlist = [(img1.rect.x + point[0], img1.rect.y + point[1]) for point in overlap.outline(physics_quality)]
        # max_point = max(overlist, key=lambda x: sqrt((x[0] - img1.center[0]) ** 2 + (x[1] - img1.center[1]) ** 2))
        min_point = min(overlist, key=lambda x: sqrt((x[0] - img1.center[0]) ** 2 + (x[1] - img1.center[1]) ** 2))
        if len(overlist) > 1:
            del overlist[overlist.index(min_point)]
            cf = abs(zerodiv(img1.center[0] - min_point[0], img1.center[1] - min_point[1]))
            max_point = min(overlist, key=lambda x: abs(cf - abs(zerodiv(img1.center[0] - x[0],
                                                                         img1.center[1] - x[1]))))
            if abs(max_point[0] - min_point[0]) > physics_quality or abs(max_point[1] - min_point[1]) > physics_quality:
                img1.move((min_point[0] - max_point[0], min_point[1] - max_point[1]))
            pygame.draw.line(screen, pygame.color.Color('red'), max_point, min_point, 1)
            pygame.draw.circle(screen, pygame.color.Color('green'), min_point, 2, 0)
            pygame.draw.circle(screen, pygame.color.Color('yellow'), max_point, 2, 0)
        else:
            pygame.draw.circle(screen, pygame.color.Color('green'), min_point, 2, 0)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
