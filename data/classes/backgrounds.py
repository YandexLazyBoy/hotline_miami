import pygame
from data.classes.constants import *


class AGBackground:
    def __init__(self, lib, camera_size):
        self.frames = []
        self.mult_color = [255, 0, 50]
        self.load_data(lib, camera_size)
        self.image = self.frames[0]
        self.loop_flag = False
        self.current_time = 0
        self.current_frame = 0
        self.rotation = 0

    def reset(self):
        self.image = self.frames[0]
        self.current_time = 0
        self.current_frame = 0
        self.loop_flag = False

    def update(self, dt):
        self.current_time += dt
        # бродим по hue
        if BACKGROUND_RENDER_TYPE in (0, 1):
            if self.mult_color[0] == 255 and self.mult_color[1] == 0 and self.mult_color[2] < 255:
                self.mult_color[2] += 1
            if self.mult_color[0] != 0 and self.mult_color[1] == 0 and self.mult_color[2] == 255:
                self.mult_color[0] -= 1
            if self.mult_color[0] == 0 and self.mult_color[1] < 255 and self.mult_color[2] == 255:
                self.mult_color[1] += 1
            if self.mult_color[0] == 0 and self.mult_color[1] == 255 and self.mult_color[2] != 0:
                self.mult_color[2] -= 1
            if self.mult_color[0] < 255 and self.mult_color[1] == 255 and self.mult_color[2] == 0:
                self.mult_color[0] += 1
            if self.mult_color[0] == 255 and self.mult_color[1] != 0 and self.mult_color[2] == 0:
                self.mult_color[1] -= 1

        if self.frame_time <= self.current_time:
            self.current_frame += 1
            if len(self.frames) - 1 <= self.current_frame:
                self.current_frame = 0
                self.loop_flag = True
            self.current_time -= self.frame_time

        self.image = self.frames[self.current_frame].copy()
        if BACKGROUND_RENDER_TYPE == 0:
            self.image.fill(self.mult_color, special_flags=pygame.BLEND_RGB_MIN)
        elif BACKGROUND_RENDER_TYPE == 1:
            self.image.fill(self.mult_color)

    def load_data(self, lib, cs):
        back = lib.seq_library.get('sprSpread', None)
        if back:
            self.frame_time = back[1]
        else:
            print('sprSpread cannot be loaded')
            return 1
        grad = lib.img_library.get('AGGradient', None)
        if grad:
            self.frame_time = back[1]
            for sp in back[0]:
                g = grad[0].copy()
                g.blit(sp, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
                if BACKGROUND_RENDER_TYPE == 2:
                    g.fill(self.mult_color, special_flags=pygame.BLEND_RGB_MIN)
                if cs[0] > cs[1]:
                    g = pygame.transform.scale(g, (cs[0], cs[0]))
                    scr_t = pygame.Surface(cs)
                    scr_t.blit(g, (0, (cs[1] - cs[0]) // 2))
                else:
                    g = pygame.transform.scale(g, (cs[1], cs[1]))
                    scr_t = pygame.Surface(cs)
                    scr_t.blit(g, (cs[1] - g.get_width() // 2, 0))
                self.frames.append(scr_t)
        else:
            print('AGGradient cannot be loaded')


BACKGROUND_DB = [AGBackground]
