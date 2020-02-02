from data.classes.backgrounds import *
import math
from random import randint, choice


class Bullet(pygame.sprite.Sprite):
    def __init__(self, textures, spawn, rotation, dl):
        super().__init__()
        rotation -= 90
        if dl in (0, 1):
            self.image = pygame.transform.rotate(textures, 360 - rotation)
        elif dl in (2, 3):
            tex = copy(textures)
            self.image = pygame.transform.rotate(tex, 360 - rotation)
        else:
            self.image = pygame.Surface(pygame.transform.rotate(textures, 360 - rotation).get_size(), pygame.SRCALPHA)
            pygame.draw.rect(self.image, DEBUG_BOUNDING_BOX_COLOR, self.image.get_rect(), 1)
        self.rect = self.image.get_rect()
        self.rect.move_ip(spawn[0] - self.rect.width // 2, spawn[1] - self.rect.height // 2)
        self.dx = math.cos(math.radians(rotation)) * BULLET_SPEED  # скорость по х
        self.dy = math.sin(math.radians(rotation)) * BULLET_SPEED  # скорость по y

    def update(self, seconds):
        self.rect = self.rect.move(self.dx * seconds, self.dy * seconds)


class BearGuns:
    def __init__(self, bt, at, details):
        self.det = details[0]
        self.maglim = 60
        self.magazine = self.maglim
        self.dispersion = 5
        self.bullet_texture = bt
        self.arm_textures = at[0]
        self.rotation_right = 0
        self.rotation_left = 0
        self.pos_left = 0, 0
        self.pos_right = 0, 0
        self.image = pygame.Surface((336, 164))
        self.sklad = 10
        self.current_time = 0
        self.shoot_time = 0.1
        self.shoot = print
        self.launch_anim = print
        self.holster = print
        self.is_reload = False
        self.reload_time = 0
        self.is_anim = False
        self.s_lib = dict()
        self.dl = 0

    def load_sounds(self, lib):
        self.s_lib['shoot'] = lib['sndUzi']

    def update(self, angle, player_pos, mouse_pos, dt, is_anim, v_pos, devl, dbc):
        self.dl = devl
        self.current_time += dt
        mouse_pos = mouse_pos[0] - v_pos[0] + player_pos[0], mouse_pos[1] - v_pos[1] + player_pos[1]

        vpp1 = math.sin(math.radians(angle)) * 36, math.cos(math.radians(angle)) * -36

        pp2 = player_pos[0] - vpp1[0], player_pos[1] - vpp1[1]
        pp1 = player_pos[0] + vpp1[0], player_pos[1] + vpp1[1]

        ang1 = math.degrees(math.atan2(pp1[1] - mouse_pos[1], pp1[0] - mouse_pos[0])) - 90
        ang2 = math.degrees(math.atan2(pp2[1] - mouse_pos[1], pp2[0] - mouse_pos[0])) - 90

        self.rotation_left = ang1 + 1.5375
        self.rotation_right = ang2 - 1.5375

        self.pos_left = (int(pp1[0] + math.sin(math.radians(self.rotation_left)) * 120.0666),
                         int(pp1[1] + math.cos(math.radians(self.rotation_left)) * -120.0666))
        self.pos_right = (int(pp2[0] + math.sin(math.radians(self.rotation_right)) * 120.0666),
                          int(pp2[1] + math.cos(math.radians(self.rotation_right)) * -120.0666))

        pp1 = (vpp1[0] + 168, vpp1[1] + 168)
        pp2 = (168 - vpp1[0], 168 - vpp1[1])

        rt1 = pygame.transform.rotate(pygame.transform.flip(self.arm_textures, True, True), 270 - ang1)
        rt2 = pygame.transform.rotate(pygame.transform.flip(self.arm_textures, True, False), 270 - ang2)

        self.image = pygame.Surface((336, 336), pygame.SRCALPHA)
        self.is_anim = is_anim

        ps1 = (int(56.5685 * math.cos(math.radians(ang1 + 81.8699))),
               int(56.5685 * math.sin(math.radians(ang1 + 81.8699))))
        ps2 = (int(56.5685 * math.cos(math.radians(ang2 + 98.1301))),
               int(56.5685 * math.sin(math.radians(ang2 + 98.1301))))

        det = list()

        det.append(pygame.transform.rotate(self.det[0], 360 - angle))
        det.append(pygame.transform.rotate(self.det[1], 360 - angle))
        if devl in (0, 1):
            self.image.blit(det[0], (168 - det[0].get_width() // 2, 168 - det[0].get_height() // 2))
            self.image.blit(rt1, (pp1[0] - rt1.get_width() // 2 - ps1[0], pp1[1] - rt1.get_height() // 2 - ps1[1]))
            self.image.blit(rt2, (pp2[0] - rt2.get_width() // 2 - ps2[0], pp2[1] - rt2.get_height() // 2 - ps2[1]))
            self.image.blit(det[1], (168 - det[1].get_width() // 2, 168 - det[1].get_height() // 2))
        elif devl in (2, 3):
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        else:
            b_r = det[0].get_rect()
            b_r.move_ip((168 - b_r.w // 2, 168 - b_r.h // 2))
            pygame.draw.rect(self.image, dbc, b_r, 1)
            b_r = rt1.get_rect()
            b_r.move_ip((pp1[0] - b_r.w // 2 - ps1[0], pp1[1] - b_r.h // 2 - ps1[1]))
            pygame.draw.rect(self.image, dbc, b_r, 1)
            b_r = rt2.get_rect()
            b_r.move_ip((pp1[0] - b_r.w // 2 - ps1[0], pp1[1] - b_r.h // 2 - ps1[1]))
            pygame.draw.rect(self.image, dbc, b_r, 1)
            b_r = det[1].get_rect()
            b_r.move_ip((168 - b_r.w // 2, 168 - b_r.h // 2))
            pygame.draw.rect(self.image, dbc, b_r, 1)

    def shootb(self, dt):
        if self.is_anim:
            if self.is_reload and self.reload_time < self.current_time:
                self.current_time = self.shoot_time + dt
                self.is_reload = False
            elif not self.is_reload and self.shoot_time < self.current_time:
                self.current_time = 0
                # ВНИМАНИЕ!!! в self.sklad и self.magazine бывают разные по типу значения (int, str)
                if not(self.sklad == 'Empty' and self.magazine <= 0):
                    if self.magazine <= 0:
                        if self.sklad >= self.maglim:
                            self.magazine = self.maglim
                            self.sklad -= self.maglim
                        elif self.sklad <= 0:
                            self.sklad = 'Empty'
                            return None
                        else:
                            self.magazine = self.sklad
                            self.sklad = 'Empty'
                        self.launch_anim('reloadWeapons')
                        self.is_reload = True
                        self.current_time = 0
                    else:
                        self.magazine -= 2
                        self.s_lib['shoot'].play()
                        self.shoot(Bullet(self.bullet_texture, self.pos_left,
                                          self.rotation_left + randint(self.dispersion * -1, self.dispersion), self.dl))
                        self.shoot(Bullet(self.bullet_texture, self.pos_right,
                                          self.rotation_right + randint(self.dispersion * -1, self.dispersion),
                                   self.dl))
                else:
                    print('There is nothing in magazine')
                    self.holster()
                return 1
            return 0