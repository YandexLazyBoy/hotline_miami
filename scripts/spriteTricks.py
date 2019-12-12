from operator import truth
from pygame.sprite import Sprite
import pygame, os


def rectcollide(rect, *group):
    return [r for r in group if rect.collide(r)]


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
            if isinstance(sprite, Sprite):
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
            if isinstance(sprite, Sprite):
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
            if isinstance(sprite, Sprite):
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


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Librarian:
    def __init__(self):
        self.img_library = dict()
        self.seq_library = dict()

    def load_image(self, name, color_key=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname).convert()
        except pygame.error:
            return None

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image

    def load_library(self, lib_path):
        success = 0
        errors = 0
        for root, dirs, files in os.walk(lib_path):
            for file in files:
                if file.endswith('.gcf'):
                    with open(os.path.join(root, file), 'r') as conf:
                        contents = [line[:-1].split(': ')[-1] for line in conf.readlines()]
                        f_type = contents[0]
                        lib_name = contents[2]
                        if f_type == 'single image':
                            image = self.load_image(os.path.join(root, contents[1]))
                            if image:
                                if len(contents) > 3:
                                    mask = self.load_image(os.path.join(root,
                                                                        contents[3]))
                                    if mask:
                                        self.img_library[lib_name] = (image, mask)
                                        success += 1
                                    else:
                                        print(os.path.join(root, contents[3]), 'can not be loaded')
                                        errors += 1
                                else:
                                    self.img_library[lib_name] = tuple(image)
                                    success += 1
                            else:
                                print(os.path.join(root, contents[0]), 'can not be loaded')
                                errors += 1
                        elif f_type == 'image sequence':
                            sequence = contents[1].split(', ')
                            image_seq = [self.load_image(os.path.join(root, image),
                                                         color_key=-1) for image in sequence]
                            if not (None in image_seq):
                                try:
                                    frame_time = float(contents[3])
                                except ValueError:
                                    frame_time = None
                                if frame_time:
                                    if len(contents) > 4:
                                        mask = self.load_image(os.path.join(root,contents[2]))
                                        if mask:
                                            self.seq_library[lib_name] = (image_seq, frame_time, mask)
                                            success += 1
                                        else:
                                            print(os.path.join(root, contents[2]), 'can not be loaded')
                                            errors += 1
                                    else:
                                        self.seq_library[lib_name] = (image_seq, frame_time)
                                        success += 1
                                else:
                                    print(os.path.join(root, file), 'has wrong frame time')
                                    errors += 1
                            else:
                                for i in range(len(sequence)):
                                    if image_seq[i] is None:
                                        print(os.path.join(root, sequence[i]), 'can not be loaded')
                                errors += 1
                        else:
                            print(os.path.join(root, file), 'has wrong type')
                            errors += 1
        print('\nSuccess loadings:', str(success) + ', errors:', errors)


class AnimSequence:
    def __init__(self, frame_time, frames, direction=True):
        self.frame_time = frame_time
        self.frames = frames
        self.direction = direction  # True 0-n, False n-0
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.frame_time:
