from data.classes.players import *


class Group(pygame.sprite.AbstractGroup):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


class LayeredGroup(pygame.sprite.LayeredUpdates):
    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.transformed_texture, spr.transformed_texture.get_rect())
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty


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


class AnimObject(Object):
    def __init__(self, position, rotation, frame_time, frames, direction=True):
        self.frame_time = frame_time
        self.frames = frames
        super().__init__(position, rotation, self.frames[0])
        self.direction = direction  # True 0-n, False n-0
        self.current_time = 0
        self.current_frame = 0

    def update(self, dt):
        self.current_frame += 1
        self.current_time += dt
        lim = self.frame_time * len(self.frames)
        if lim <= self.current_time:
            self.current_time -= lim

            if self.frame_time <= self.current_time:
                if self.direction:
                    self.current_frame += 1
                else:
                    self.current_frame -= 1

                if len(self.frames) - 1 <= self.current_frame:
                    self.current_frame = 0
                elif self.current_frame < 0:
                    self.current_frame = len(self.frames) - 1

            self.orig_texture = self.frames[self.current_frame]
            self.rotate(self.rotation)