import pygame
from math import atan, degrees, cos, sin, radians
from random import randint


class Bullet:
    def __init__(self, velocity, source, damage=100):
        self.source = source  # источник
        self.damage = damage  # урон
        self.rotation = self.source.rotation  # поворот
        self.velocity = velocity  # пикселей в секунду
        self.orig_texture = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.orig_texture.fill(pygame.Color('red'))
        self.transformed_texture = self.orig_texture
        self.rotate(self.source.rotation)
        self.dx = cos(radians(self.source.rotation)) * self.velocity  # скорость по х
        self.dy = sin(radians(self.source.rotation)) * self.velocity  # скорость по y
        self.position = self.source.position
        self.geometryToOrigin()

    def rotate(self, angle):
        self.transformed_texture = pygame.transform.rotate(self.orig_texture, 360 - self.rotation)
        self.rotation = angle

    def geometryToOrigin(self):
        bound_box = self.transformed_texture.get_bounding_rect()  # достаём рамку текстуры
        x = bound_box.width // 2  # вычисляем сдвиг
        y = bound_box.height // 2  # вычисляем сдвиг
        self.position = (self.position[0] - x, self.position[1] - y)

    def update(self, seconds):
        self.position = (self.position[0] + self.dx * seconds, self.position[1] + self.dy * seconds)


class Weapon:
    def __init__(self, carrier, dispersion_limit):
        self.carrier = carrier  # носитель оружия
        self.dispersion_limit = dispersion_limit  # максимальный градус отклонения пуль от цели
        self.damage_per_bullet = 100  # дамаг одной пули

    def syncRotation(self):
        pass

    def generateBullet(self):
        pass

class Player:
    def __init__(self, angle=0, v_position=(400, 300)):
        self.rotation = angle
        self.viewport_position = v_position
        self.position = self.viewport_position  # TODO координаты для карты
        self.orig_texture = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.orig_texture.fill((255, 255, 255))
        self.transformed_texture = self.orig_texture
        self.geometryToOrigin()

    def rotate(self, angle):
        # Поскольку мы расчитывали поворот по часовой стрелке,
        # а пайгейм крутит против часовой, вычитаем из 360 получившийся градус
        self.transformed_texture = pygame.transform.rotate(self.orig_texture, 360 - angle)
        self.rotation = angle
        # ------Сдвигаем перса так, чтобы точка позиции на карте была в середине
        self.geometryToOrigin()

    def geometryToOrigin(self):
        bound_box = self.transformed_texture.get_bounding_rect()  # достаём рамку текстуры
        x = bound_box.width // 2  # вычисляем сдвиг
        y = bound_box.height // 2  # вычисляем сдвиг
        self.viewport_position = (self.position[0] - x, self.position[1] - y)

    def trackTo(self, point):
        x = point[0] - self.viewport_position[0]  # разница между точками по x
        y = point[1] - self.viewport_position[1]  # разница между точками по у
        angle = 0
        # ------Вычисляем поворот при ненулевых значениях х и y------
        if y < 0 < x:
            angle = degrees(atan(x / abs(y)))
        elif y > 0 and x > 0:
            angle = 180 - degrees(atan(x / y))
        elif x < 0 < y:
            angle = 180 + degrees(atan(abs(x) / y))
        elif y < 0 and x < 0:
            angle = 360 - degrees(atan(x / y))
        # ------Проверка для нулевых значений х и y------
        if y == 0 and x < 0:
            angle = 270
        elif y > 0 and x == 0:
            angle = 180
        elif y == 0 and x > 0:
            angle = 90
        # ------Собсна, поворачиваем перса------
        self.rotate(angle)

    def shoot(self):
        return Bullet(2000, self)


class Map:
    def __init__(self, map_size, *objects):
        self.orig_canvas = pygame.Surface(map_size)
        self.orig_canvas.fill(pygame.Color('black'))
        self.render_canvas = self.orig_canvas
        self.bullets = list()

    def checkCollision(self):
        pass

    def render(self, seconds):
        self.render_canvas = pygame.Surface((1000, 1000))
        for i in range(len(self.bullets)):
            self.bullets[i].update(seconds)
            self.render_canvas.blit(self.bullets[i].transformed_texture, self.bullets[i].position)

    def killBulletsInOffset(self):
        pass


player = Player()
world = Map((1000, 1000))
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
fps = 60
frame_time = 1 / fps
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            player.trackTo(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            world.bullets.append(player.shoot())

    screen.fill(pygame.Color('black'))
    world.render(frame_time)
    screen.blit(world.render_canvas, (0, 0))
    screen.blit(player.transformed_texture, player.viewport_position)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
