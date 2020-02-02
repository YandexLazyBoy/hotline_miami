from scripts.important_classes import *


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, img, position, layer):
        super().__init__()
        self.image = img
        self.rect = img.get_rect()
        self.rect.move_ip(position)
        self._layer = layer


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, img_seq, position, frame_time, layer, rotation=0):
        super().__init__()
        self.image = pygame.transform.rotate(img_seq[0], 360 - rotation)
        self.frames = img_seq
        self._layer = layer
        self.frame_time = frame_time
        self.current_time = 0
        self.current_frame = 0
        self.rect = self.image.get_rect()
        self.rect.move_ip(position)
        self.rotation = rotation

    def update(self, dt):
        self.current_time += dt
        if self.frame_time <= self.current_time:
            self.current_frame += 1
            if len(self.frames) - 1 <= self.current_frame:
                self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.current_time -= self.frame_time
            if self.rotation:
                self.image = pygame.transform.rotate(self.image, 360 - self.rotation)

'''
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
    def __init__(self, position, viewport_position, angle):
        texture = pygame.Surface((40, 40), pygame.SRCALPHA)
        texture.fill((255, 255, 255))
        super().__init__(position, angle, texture)
        self.speed = PLAYER_SPEED
        self.viewport_position = viewport_position
        self.mask = None
        self.geometryToOrigin()
        self.weapon = Weapon(0, self.rotation,
                             (self.position[0] + 30, self.position[1] + 30), 5, 30, 1000, 100)

    def rotate(self, angle):
        super().rotate(angle)
        self.weapon.syncRotation(self.position, angle)

    def load_images(self, sprite_lib, **kwargs):
        default_names = [
            '': ''
        ]

    def teleport(self, vec2):
        self.position = (self.position[0] + vec2, self.position[1] + y)

    def move(self, vec2, seconds):
        x = self.speed * seconds * vec2[0]
        y = self.speed * seconds * vec2[1]
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
'''