import pygame
from math import atan, degrees, cos, sin, radians, sqrt
from random import randint


class Bullet:
    def __init__(self, velocity, source_id, spawn, rotation, damage=100):
        self.source_id = source_id  # 0 - player, 1 - enemy
        self.damage = damage  # урон
        self.rotation = rotation  # поворот
        self.velocity = velocity  # пикселей в секунду
        self.orig_texture = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.orig_texture.fill(pygame.Color('red'))
        self.transformed_texture = self.orig_texture
        self.rotate(self.rotation)
        self.dx = cos(radians(self.rotation)) * self.velocity  # скорость по х
        self.dy = sin(radians(self.rotation)) * self.velocity  # скорость по y
        self.position = spawn
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
    def __init__(self, carrier_id, position, dispersion_limit, magazine_limit, bullet_velocity,
                 bullet_damage):
        self.magazine_limit = magazine_limit
        self.magazine = self.magazine_limit
        self.bullet_velocity = bullet_velocity
        self.bullet_damage = bullet_damage
        self.carrier_id = carrier_id  # носитель оружия (0 - player, 1 - enemy)
        self.dispersion_limit = dispersion_limit  # максимальный градус отклонения пуль от цели
        self.damage_per_bullet = 100  # дамаг одной пули
        self.orig_texture = pygame.Surface((20, 60), pygame.SRCALPHA)
        self.orig_texture.fill(pygame.Color('gray'))
        self.transformed_texture = self.orig_texture
        self.position = position
        self.barrel_position = (self.position[0] + 10, self.position[1])
        self.rotation = 0

    def syncRotation(self, point, angle):
        self.rotate(angle)
        # ------крутим тело------
        x = abs(self.position[0] - point[0])
        y = abs(self.position[1] - point[1])
        r = sqrt(x ** 2 + y ** 2)
        self.position = (cos(radians(self.rotation)) * r, sin(radians(self.rotation)) * r)
        # ------крутим точку спавна пуль------
        x = abs(self.barrel_position[0] - point[0])
        y = abs(self.barrel_position[1] - point[1])
        r = sqrt(x ** 2 + y ** 2)
        self.barrel_position = (cos(radians(self.rotation)) * r, sin(radians(self.rotation)) * r)

    def rotate(self, angle):
        self.transformed_texture = pygame.transform.rotate(self.orig_texture, 360 - self.rotation)
        self.rotation = angle

    def generateBullet(self):
        if self.magazine == 0:
            self.magazine = self.magazine_limit
            return None
        return Bullet(self.bullet_velocity, self.carrier_id, self.barrel_position,
                      self.rotation + randint(-self.dispersion_limit,
                                              self.dispersion_limit), self.bullet_damage)


class Player:
    def __init__(self, angle=0, v_position=(400, 300)):
        self.rotation = angle
        self.viewport_position = v_position
        self.position = self.viewport_position  # TODO координаты для карты
        self.orig_texture = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.orig_texture.fill((255, 255, 255))
        self.transformed_texture = self.orig_texture
        self.geometryToOrigin()
        self.weapon = Weapon(0, (self.position[0] + 20, self.position[1] - 30), 5, 30, 500, 100)

    def rotate(self, angle):
        # Поскольку мы расчитывали поворот по часовой стрелке,
        # а пайгейм крутит против, вычитаем из 360 получившийся градус
        self.transformed_texture = pygame.transform.rotate(self.orig_texture, 360 - angle)
        self.rotation = angle
        # ------Сдвигаем перса так, чтобы точка позиции на карте была в середине------
        self.geometryToOrigin()
        self.weapon.syncRotation(self.position, angle)

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
        return self.weapon.generateBullet()


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
