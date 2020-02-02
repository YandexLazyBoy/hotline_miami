import pygame
from copy import copy, deepcopy
from data.classes.constants import *


class HUD:
    def __init__(self, w_size, lib, font):
        self.image = pygame.Surface(w_size, pygame.SRCALPHA)
        self.font = font
        pts = font.get_surface('0pts')
        ptss = copy(pts)
        self.bg = lib.img_library['sprHUDBackground'][0]
        self.bg_f = pygame.transform.flip(self.bg, True, False)
        self.image.blit(self.bg, (w_size[0] - self.bg.get_width(), 30))
        p = (w_size[0] - pts.get_width() - 30, 30 + (self.bg.get_height() - pts.get_height()) // 2)
        pts.fill((200, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)
        self.image.blit(pts, (p[0] + 5, p[1] + 5))
        ptss.fill((0, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self.image.blit(ptss, p)

    def update(self, pts_c, player, w_size):
        self.image = pygame.Surface(w_size, pygame.SRCALPHA)
        if player.current_flag != 'unarmed':
            ammo = self.font.get_surface(str(player.current_weapon.magazine + player.current_weapon.sklad
                                             if type(player.current_weapon.sklad) == int
                                             else player.current_weapon.magazine))
            ammos = copy(ammo)
            self.image.blit(self.bg_f, (0, w_size[1] - 130))
            p = (30, w_size[1] - 130 + (self.bg_f.get_height() - ammo.get_height()) // 2)

            ammo.fill((200, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)
            self.image.blit(ammo, (p[0] + 5, p[1] + 5))
            ammos.fill((0, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
            self.image.blit(ammos, p)

        pts = self.font.get_surface(str(pts_c) + 'pts')
        ptss = copy(pts)

        self.image.blit(self.bg, (w_size[0] - self.bg.get_width(), 30))
        p = (w_size[0] - pts.get_width() - 30, 30 + (self.bg.get_height() - pts.get_height()) // 2)
        pts.fill((200, 0, 50), special_flags=pygame.BLEND_RGBA_MULT)
        self.image.blit(pts, (p[0] + 5, p[1] + 5))
        ptss.fill((0, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
        self.image.blit(ptss, p)


class CheckBox:
    def __init__(self, pos, imgs, checked=False):
        self.ilib = imgs[0][0], imgs[1][0]
        self.rect = pygame.Rect(pos, (self.ilib[0].get_width(), self.ilib[0].get_height()))
        if checked:
            self.image = self.ilib[1]
            self.flag = True
        else:
            self.image = self.ilib[0]
            self.flag = False

    def check(self, m_pos):
        if self.rect.collidepoint(m_pos[0], m_pos[1]):
            if self.flag:
                self.image = self.ilib[0]
                self.flag = False
            else:
                self.image = self.ilib[1]
                self.flag = True


class RadioButton:
    def __init__(self, pos, imgs):
        self.ilib = imgs[0][0], imgs[1][0]
        self.rect = pygame.Rect(pos, (self.ilib[0].get_width(), self.ilib[0].get_height()))
        self.image = self.ilib[0]
        self.func = print

    def set_image(self, i):
        self.image = self.ilib[i]


class RadioGroup:
    def __init__(self, rads, cur_id=0):
        self.radiobuttons = rads
        self.cur_id = cur_id
        self.radiobuttons[cur_id].set_image(1)

    def check(self, m_pos):
        for rb in range(len(self.radiobuttons)):
            if self.radiobuttons[rb].rect.collidepoint(m_pos[0], m_pos[1]):
                if self.cur_id != rb:
                    self.radiobuttons[self.cur_id].set_image(0)
                    self.radiobuttons[rb].set_image(1)
                    self.radiobuttons[rb].func()
                    self.cur_id = rb

    def render(self, sur):
        sur_blit = sur.blit
        for rb in self.radiobuttons:
            sur_blit(rb.image, (rb.rect.x, rb.rect.y))


class SettingScreen:
    def __init__(self, lib, set_men):
        ilib = (lib.img_library['sprCheckboxUnChecked'], lib.img_library['sprCheckboxChecked'],
                lib.img_library['sprRadioButtonUnChecked'], lib.img_library['sprRadioButtonChecked'])

        def func0():
            set_men.update_DL(0)

        def func1():
            set_men.update_DL(2)

        def func2():
            set_men.update_DL(3)

        def func3():
            set_men.update_DL(4)

        def func4():
            set_men.update_BGRT(0)

        def func5():
            set_men.update_BGRT(1)

        def func6():
            set_men.update_BGRT(2)

        def func7():
            set_men.update_DL(1)

        rg = [RadioButton((10, 10), (ilib[2], ilib[3])), RadioButton((10, 60), (ilib[2], ilib[3])),
              RadioButton((10, 110), (ilib[2], ilib[3])),
              RadioButton((10, 160), (ilib[2], ilib[3])), RadioButton((10, 210), (ilib[2], ilib[3]))]
        rg2 = [RadioButton((548, 10), (ilib[2], ilib[3])), RadioButton((548, 60), (ilib[2], ilib[3])),
               RadioButton((548, 110), (ilib[2], ilib[3]))]
        rg[0].func = func0
        rg[1].func = func7
        rg[2].func = func1
        rg[3].func = func2
        rg[4].func = func3
        rg2[0].func = func4
        rg2[1].func = func5
        rg2[2].func = func6
        self.image = pygame.Surface((600, 400))
        self.rgs = [RadioGroup(rg, cur_id=set_men.DL), RadioGroup(rg2, cur_id=set_men.BGRT)]
        for rg1 in self.rgs:
            rg1.render(self.image)

    def check(self, m_pos):
        self.image = pygame.Surface((600, 400))
        for rg1 in self.rgs:
            rg1.check(m_pos)
            rg1.render(self.image)
