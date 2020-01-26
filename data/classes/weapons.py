from pygame.sprite import Sprite
from pygame import Surface, SRCALPHA
from pygame.transform import rotate, flip
from pygame.draw import circle
from math import radians, sin, cos, atan2, degrees
from data.classes.constants import *
from random import randint


class Bullet(Sprite):
    def __init__(self, texture, spawn, rotation):
        super().__init__()
        texture = rotate(texture, 360 - rotation)
        self.rect = texture.get_rect()
        self.rect.move_ip(spawn[0] - self.rect.width // 2, spawn[1] - self.rect.height // 2)
        self.dx = cos(radians(rotation - 90)) * BULLET_SPEED  # скорость по х
        self.dy = sin(radians(rotation - 90)) * BULLET_SPEED  # скорость по y

    def update(self, seconds):
        self.rect = self.rect.move(self.dx * seconds, self.dy * seconds)


class BearGuns:
    def __init__(self, bt, at):
        self.magazine = 60
        self.dispersion = 5
        self.bullet_texture = bt
        self.arm_textures = at[0]
        self.rotation_right = 0
        self.rotation_left = 0
        self.pos_left = 0, 0
        self.pos_right = 0, 0
        self.image = Surface((336, 164))
        self.shoot_time = 0
        self.shoot = print

    def update(self, angle, player_pos, mouse_pos):
        # angle = 90
        mouse_pos = mouse_pos[0] - 400 + player_pos[0], mouse_pos[1] - 300 + player_pos[1]

        vpp1 = sin(radians(angle)) * 36, cos(radians(angle)) * -36

        print(vpp1)

        pp2 = player_pos[0] - vpp1[0], player_pos[1] - vpp1[1]
        pp1 = player_pos[0] + vpp1[0], player_pos[1] + vpp1[1]

        ang1 = degrees(atan2(pp1[1] - mouse_pos[1], pp1[0] - mouse_pos[0])) - 90
        ang2 = degrees(atan2(pp2[1] - mouse_pos[1], pp2[0] - mouse_pos[0])) - 90

        self.rotation_left = ang1 + 1.5375
        self.rotation_right = ang2 - 1.5375

        self.pos_left = (int(pp1[0] + sin(radians(self.rotation_left)) * 120.0666),
                         int(pp1[1] + cos(radians(self.rotation_left)) * -120.0666))
        self.pos_right = (int(pp2[0] + sin(radians(self.rotation_right)) * 120.0666),
                          int(pp2[1] + cos(radians(self.rotation_right)) * -120.0666))

        pp1 = (vpp1[0] + 168,
               vpp1[1] + 168)
        pp2 = (168 - vpp1[0],
               168 - vpp1[1])

        rt1 = rotate(flip(self.arm_textures, True, True), 270 - ang1)
        rt2 = rotate(flip(self.arm_textures, True, False), 270 - ang2)

        # self.image = rotate(Surface((336, 164), SRCALPHA), 360 - angle)
        self.image = Surface((336, 336), SRCALPHA)

        ps1 = int(56.5685 * cos(radians(ang1 + 81.8699))), int(56.5685 * sin(radians(ang1 + 81.8699)))
        ps2 = int(56.5685 * cos(radians(ang2 + 98.1301))), int(56.5685 * sin(radians(ang2 + 98.1301)))

        self.image.blit(rt1, (pp1[0] - rt1.get_width() // 2 - ps1[0],
                              pp1[1] - rt1.get_height() // 2 - ps1[1]))
        self.image.blit(rt2, (pp2[0] - rt2.get_width() // 2 - ps2[0],
                              pp2[1] - rt2.get_height() // 2 - ps2[1]))

    def shoot(self):
        if self.shoot_time > 0:
            if self.magazine != 'Empty':
                if self.magazine <= 0:
                    self.magazine = 'Empty'
                    return None
                else:
                    self.magazine -= 2
                    self.shoot(Bullet(self.bullet_texture, self.pos_left, self.rotation_left))
                    self.shoot(Bullet(self.bullet_texture, self.pos_right, self.rotation_right))
            else:
                print('There is nothing in magazine')
            return None
