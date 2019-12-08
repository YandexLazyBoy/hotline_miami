import pygame
from math import atan, degrees, cos, sin, radians, sqrt
from random import randint, choice
from scripts.spriteTricks import Group


class Object(pygame.sprite.Sprite):
    def __init__(self, position, rotation, texture):
        super().__init__()
        self.position = position
        self.transformed_position = self.position
        self.rotation = rotation
        self.orig_texture = texture
        self.transformed_texture = self.orig_texture
        self.rect = self.transformed_texture.get_rect()

    def rotate(self, angle):
        self.transformed_texture = pygame.transform.rotate(self.orig_texture, 360 - self.rotation)
        self.rotation = angle
        self.geometryToOrigin()

    def updateRect(self):
        self.rect = self.transformed_texture.get_rect()
        self.rect.move_ip(self.transformed_position)

    def geometryToOrigin(self):
        bound_box = self.transformed_texture.get_bounding_rect()  # достаём рамку текстуры
        x = bound_box.width // 2  # вычисляем сдвиг
        y = bound_box.height // 2  # вычисляем сдвиг
        self.transformed_position = (self.position[0] - x, self.position[1] - y)
        self.updateRect()


class Bullet(Object):
    def __init__(self, velocity, source_id, spawn, rotation, damage=100):
        texture = pygame.Surface((10, 10), pygame.SRCALPHA)
        texture.fill(pygame.Color('red'))
        super().__init__(spawn, rotation, texture)
        self.source_id = source_id  # 0 - player, 1 - enemy
        self.damage = damage  # урон
        self.velocity = velocity  # пикселей в секунду
        self.rotate(self.rotation)  # поворачиваем в точку выстрела
        self.dx = cos(radians(self.rotation - 90)) * self.velocity  # скорость по х
        self.dy = sin(radians(self.rotation - 90)) * self.velocity  # скорость по y

    def update(self, seconds):
        self.position = (self.position[0] + self.dx * seconds, self.position[1] + self.dy * seconds)


class Weapon(Object):
    def __init__(self, carrier_id, rotation, position, dispersion_limit, magazine_limit, bullet_velocity,
                 bullet_damage):
        texture = pygame.Surface((20, 60), pygame.SRCALPHA)
        texture.fill(pygame.Color('gray'))
        super().__init__(position, rotation, texture)
        self.magazine_limit = magazine_limit  # вместимость магазина
        self.magazine = self.magazine_limit  # количество патронов в магазине
        self.bullet_velocity = bullet_velocity  # скорость пуль
        self.bullet_damage = bullet_damage  # урон от каждой пули
        self.carrier_id = carrier_id  # носитель оружия (0 - player, 1 - enemy)
        self.dispersion_limit = dispersion_limit  # максимальный градус отклонения пуль от цели
        self.damage_per_bullet = 100  # дамаг одной пули
        self.barrel_position = (self.position[0], self.position[1])  # точка спавна пуль
        self.transformed_barrel_position = self.barrel_position
        self.geometryToOrigin()

    def syncRotation(self, point, angle):
        self.rotate(angle)
        # ------крутим тело------
        x = abs(self.position[0] - point[0])
        y = abs(self.position[1] - point[1])
        r = sqrt(x ** 2 + y ** 2)
        a = angle - 45
        self.transformed_position = (self.transformed_position[0] - x + cos(radians(a)) * r,
                                     self.transformed_position[1] - y + sin(radians(a)) * r)
        # ------крутим точку спавна пуль------
        x = abs(self.barrel_position[0] - point[0])
        y = abs(self.barrel_position[1] - point[1])
        r = sqrt(x ** 2 + y ** 2)
        self.transformed_barrel_position = (self.barrel_position[0] - x + cos(radians(a)) * r,
                                            self.barrel_position[1] - y + sin(radians(a)) * r)
        self.updateRect()

    def move(self, vec2):
        self.position = (self.position[0] + vec2[0], self.position[1] + vec2[1])
        self.barrel_position = (self.barrel_position[0] + vec2[0], self.barrel_position[1] + vec2[1])

    def generateBullet(self):
        if self.magazine == 0:  # проверка на отсутствие патронов в магазине
            self.magazine = self.magazine_limit
            return None
        return Bullet(self.bullet_velocity, self.carrier_id, self.transformed_barrel_position,
                      self.rotation + randint(-self.dispersion_limit,
                                              self.dispersion_limit), self.bullet_damage)


class Player(Object):
    def __init__(self, position, v_position, collision_geometry, angle=0):
        texture = pygame.Surface((40, 40), pygame.SRCALPHA)
        texture.fill((255, 255, 255))
        super().__init__(position, angle, texture)
        self.speed = 500
        self.viewport_position = v_position
        self.collision_geometry = collision_geometry
        self.geometryToOrigin()
        self.weapon = Weapon(0, self.rotation,
                             (self.position[0] + 30, self.position[1] + 30), 5, 30, 1000, 100)
        self.vector = (0, 0)

    def rotate(self, angle):
        super().rotate(angle)
        self.weapon.syncRotation(self.position, angle)
        if self.collision_geometry:
            self.collideandmove()

    def collideandmove(self):
        # Внимание - говнокод! Не лесб, оно тебя сожрёт
        dpos = (self.position[0] - self.transformed_position[0],
                self.position[1] - self.transformed_position[1])
        x = self.weapon.position[0] - self.position[0] - 30
        y = self.weapon.position[1] - self.position[1] - 30
        for corect in self.collision_geometry:
            if self.rect.colliderect(corect):
                if self.vector[1] > 0:
                    self.weapon.move((0, -y))
                    self.transformed_position = (self.transformed_position[0],
                                                 corect.top - self.rect.size[1] + 1)
                    self.position = (self.position[0],
                                     self.transformed_position[1] + dpos[1])

                if self.vector[1] < 0:
                    self.weapon.move((0, -y))
                    self.transformed_position = (self.transformed_position[0],
                                                 corect.bottom)
                    self.position = (self.position[0],
                                     self.transformed_position[1] + dpos[1])

                if self.vector[0] > 0:
                    self.weapon.move((-x, 0))
                    self.transformed_position = (corect.left - self.rect.size[0] + 1,
                                                 self.transformed_position[1])
                    self.position = (self.transformed_position[0] - dpos[0],
                                     self.position[1])

                if self.vector[0] < 0:
                    self.weapon.move((-x, 0))
                    self.transformed_position = (corect.right, self.transformed_position[1])
                    self.position = (self.transformed_position[0] + dpos[0],
                                     self.position[1])

    def move(self, vec2, seconds):
        x = self.speed * seconds * vec2[0]
        y = self.speed * seconds * vec2[1]
        self.vector = vec2
        self.position = (self.position[0] + x, self.position[1] + y)
        self.weapon.move((x, y))
        self.rotate(self.rotation)

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

    def shoot(self, add):
        add(self.weapon.generateBullet())


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.transformed_texture = pygame.Surface(size, pygame.SRCALPHA)
        self.transformed_texture.fill((230, 230, 255))
        self.position = position


class Map:
    def __init__(self, map_size, window_size):
        self.map_size = map_size
        self.gg_spawns = [(100, 100)]
        self.orig_canvas = pygame.Surface(self.map_size)
        self.orig_canvas.fill((50, 50, 50))
        self.render_canvas = self.orig_canvas
        self.bullets = Group()
        self.camera_size = window_size
        self.static_geometry = Group(StaticSprite((200, 100), (400, 32)))
        self.collision_geometry = [pygame.Rect((200, 100), (400, 32))]
        v_position = (window_size[0] // 2, window_size[1] // 2)
        self.player = Player(choice(self.gg_spawns), v_position, self.collision_geometry)

    def checkCollision(self):
        for bullet in self.bullets:
            for rect in self.collision_geometry:
                if rect.collidepoint(bullet.position):
                    bullet.kill()
            if (0 > bullet.position[0] or bullet.position[0] > self.map_size[0] or
                    0 > bullet.position[1] or bullet.position[1] > self.map_size[1]):
                bullet.kill()

    def render(self, seconds):
        self.render_canvas = self.orig_canvas.copy()
        self.bullets.update(seconds)
        self.checkCollision()
        self.bullets.draw(self.render_canvas)
        self.static_geometry.draw(self.render_canvas)
        self.render_canvas.blit(world.player.transformed_texture, world.player.transformed_position)
        self.render_canvas.blit(world.player.weapon.transformed_texture, world.player.weapon.transformed_position)


size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

world = Map((1000, 1000), size)

fps = 60
# frame_time = 1 / fps
frame_time = 0.016

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            world.player.trackTo(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            world.player.shoot(world.bullets.add)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        world.player.move((0, -1), frame_time)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        world.player.move((0, 1), frame_time)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        world.player.move((1, 0), frame_time)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        world.player.move((-1, 0), frame_time)

    screen.fill(pygame.Color('black'))
    world.render(frame_time)
    screen.blit(world.render_canvas, (world.player.viewport_position[0] - world.player.position[0],
                                      world.player.viewport_position[1] - world.player.position[1]))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
