from operator import truth
import pygame


class AbstractGroup(object):
    _spritegroup = True

    def __init__(self):
        self.spritedict = {}
        self.lostsprites = []

    def sprites(self):
        return list(self.spritedict)

    def add_internal(self, sprite):
        self.spritedict[sprite] = 0

    def remove_internal(self, sprite):
        r = self.spritedict[sprite]
        if r:
            self.lostsprites.append(r)
        del self.spritedict[sprite]

    def has_internal(self, sprite):
        return sprite in self.spritedict

    def copy(self):
        return self.__class__(self.sprites())

    def __iter__(self):
        return iter(self.sprites())

    def __contains__(self, sprite):
        return self.has(sprite)

    def add(self, *sprites):
        for sprite in sprites:
            if isinstance(sprite, pygame.sprite.Sprite):
                if not self.has_internal(sprite):
                    self.add_internal(sprite)
                    sprite.add_internal(self)
            else:
                try:
                    self.add(*sprite)
                except (TypeError, AttributeError):
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if not self.has_internal(spr):
                                self.add_internal(spr)
                                spr.add_internal(self)
                    elif not self.has_internal(sprite):
                        self.add_internal(sprite)
                        sprite.add_internal(self)

    def remove(self, *sprites):
        for sprite in sprites:
            if isinstance(sprite, pygame.sprite.Sprite):
                if self.has_internal(sprite):
                    self.remove_internal(sprite)
                    sprite.remove_internal(self)
            else:
                try:
                    self.remove(*sprite)
                except (TypeError, AttributeError):
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if self.has_internal(spr):
                                self.remove_internal(spr)
                                spr.remove_internal(self)
                    elif self.has_internal(sprite):
                        self.remove_internal(sprite)
                        sprite.remove_internal(self)

    def has(self, *sprites):
        return_value = False

        for sprite in sprites:
            if isinstance(sprite, pygame.sprite.Sprite):
                if self.has_internal(sprite):
                    return_value = True
                else:
                    return False
            else:
                try:
                    if self.has(*sprite):
                        return_value = True
                    else:
                        return False
                except (TypeError, AttributeError):
                    if hasattr(sprite, '_spritegroup'):
                        for spr in sprite.sprites():
                            if self.has_internal(spr):
                                return_value = True
                            else:
                                return False
                    else:
                        if self.has_internal(sprite):
                            return_value = True
                        else:
                            return False

        return return_value

    def update(self, *args):
        for s in self.sprites():
            s.update(*args)

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.transformed_texture, spr.position)
        self.lostsprites = []

    def clear(self, surface, bgd):
        if callable(bgd):
            for r in self.lostsprites:
                bgd(surface, r)
            for r in self.spritedict.values():
                if r:
                    bgd(surface, r)
        else:
            surface_blit = surface.blit
            for r in self.lostsprites:
                surface_blit(bgd, r, r)
            for r in self.spritedict.values():
                if r:
                    surface_blit(bgd, r, r)

    def empty(self):
        for s in self.sprites():
            self.remove_internal(s)
            s.remove_internal(self)

    def __nonzero__(self):
        return truth(self.sprites())

    def __len__(self):
        return len(self.sprites())

    def __repr__(self):
        return "<%s(%d sprites)>" % (self.__class__.__name__, len(self))


class Group(AbstractGroup):
    def __init__(self, *sprites):
        AbstractGroup.__init__(self)
        self.add(*sprites)


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

            if self.frame_time <= self.current_time:  # TODO возможно, оно как-то оптимизируется
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