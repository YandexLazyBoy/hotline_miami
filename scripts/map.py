from scripts.game_objects import *
import os
import xml.etree.ElementTree as ET
from random import choice


class SoundLibrarian:
    def __init__(self):
        self.music_library = list()
        self.sound_library = list()

    def load_music(self, name):
        pass

    def load_sound_library(self, lib_path):
        success = 0
        errors = 0
        for root, dirs, files in os.walk(lib_path):
            for file in files:
                if file.endswith('.wav') or file.endswith('.ogg'):
                    try:
                        sound = pygame.mixer.Sound(os.path.join(root, file))
                    except pygame.error:
                        sound = None
                    if sound:
                        self.sound_library.append(sound)
                        success += 1
                    else:
                        print(os.path.join(root, file), 'can not be loaded')
                        errors += 1
        print('\nSounds - success loadings:', str(success) + ', errors:', errors)


class EnemyLibrarian:
    def __init__(self):
        self.library = list()

    def load_library(self):
        pass


class SpriteLibrarian:
    def __init__(self):
        self.img_library = dict()
        self.seq_library = dict()

    def load_image(self, name, color_key=None):
        try:
            image = pygame.image.load(name)
        except pygame.error:
            return None

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image

    def load_library(self, lib_path):  # TODO снести всё к хренам и построить нормально
        success = 0
        errors = 0
        for root, dirs, files in os.walk(lib_path):
            for file in files:
                if file.endswith('.gcf'):
                    with open(os.path.join(root, file), 'r') as conf:
                        contents = [line[:-1].split(': ')[-1] for line in conf.readlines() if line != '\n']
                        f_type = contents[0]
                        lib_name = contents[2]
                        if f_type == 'single image':
                            if lib_name not in self.img_library.keys():
                                image = self.load_image(os.path.join(root, contents[1]), color_key=-1)
                                if image:
                                    if len(contents) > 3:
                                        mask = self.load_image(os.path.join(root,
                                                                            contents[-1]))
                                        if mask:
                                            self.img_library[lib_name] = image,  mask
                                            success += 1
                                        else:
                                            print(os.path.join(root, contents[-1]), 'can not be loaded')
                                            errors += 1
                                    else:
                                        self.img_library[lib_name] = tuple(image)
                                        success += 1
                                else:
                                    print(os.path.join(root, contents[1]), 'can not be loaded')
                                    errors += 1
                            else:
                                print(os.path.join(root, file), 'has non-unique lib name')
                                errors += 1
                        elif f_type == 'image sequence':
                            if lib_name not in self.seq_library.keys():
                                sequence = contents[1].split(', ')
                                if len(set(sequence)) == len(sequence):
                                    image_seq = [self.load_image(os.path.join(root, image),
                                                                 color_key=-1) for image in sequence]
                                    if not (None in image_seq):
                                        try:
                                            frame_time = float(contents[3])
                                        except ValueError:
                                            frame_time = None
                                        if frame_time and 0 < frame_time:
                                            if len(contents) > 4:
                                                mask = self.load_image(os.path.join(root, contents[-1]))
                                                if mask:
                                                    self.seq_library[lib_name] = image_seq, frame_time, mask
                                                    success += 1
                                                else:
                                                    print(os.path.join(root, contents[-1]), 'can not be loaded')
                                                    errors += 1
                                            else:
                                                self.seq_library[lib_name] = image_seq, frame_time
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
                                    print(os.path.join(root, file), 'has non-unique frames')
                                    errors += 1
                            else:
                                print(os.path.join(root, file), 'has non-unique lib name')
                                errors += 1
                        elif f_type == 'sequence atlas':
                            if lib_name not in self.seq_library.keys():
                                image = self.load_image(os.path.join(root, contents[1]), color_key=-1)
                                if image:
                                    try:
                                        frame_size = tuple(map(int, contents[3].split('x')))
                                    except ValueError:
                                        frame_size = None
                                    if frame_size:
                                        try:
                                            frame_time = float(contents[4])
                                        except ValueError:
                                            frame_time = None
                                        rects = [tuple(map(int, rect.split('x'))) for rect in contents[5].split(', ')]
                                        if frame_time:
                                            if rects:
                                                image_seq = list()

                                                for rect in rects:
                                                    imag = pygame.Surface(frame_size)
                                                    imag.blit(image, rect)
                                                    image_seq.append(imag)
                                                if len(contents) > 6:
                                                    mask = self.load_image(os.path.join(root, contents[-1]))
                                                    if mask:
                                                        self.seq_library[lib_name] = image_seq, frame_time, mask
                                                        success += 1
                                                    else:
                                                        print(os.path.join(root, contents[-1]), 'can not be loaded')
                                                        errors += 1
                                                else:
                                                    self.seq_library[lib_name] = image_seq, frame_time
                                                    success += 1
                                            else:
                                                print(os.path.join(root, file), 'has wrong frame positions')
                                                errors += 1
                                        else:
                                            print(os.path.join(root, file), 'has wrong frame time')
                                            errors += 1
                                    else:
                                        print(os.path.join(root, file), 'has wrong frame size')
                                        errors += 1
                                else:
                                    print(os.path.join(root, contents[1]), 'can not be loaded')
                                    errors += 1
                            else:
                                print(os.path.join(root, file), 'has non-unique lib name')
                                errors += 1
                        elif f_type == 'image atlas':
                            lib_name = contents[2].split(', ')
                            keys = self.img_library.keys()
                            lkey = True
                            for lname in lib_name:
                                if lname in keys:
                                    lkey = False
                                    break
                            del keys
                            if lkey and len(set(lib_name)) == len(lib_name):
                                image = self.load_image(os.path.join(root, contents[1]), color_key=-1)
                                if image:
                                    try:
                                        frame_size = tuple(map(int, contents[3].split('x')))
                                    except ValueError:
                                        frame_size = None
                                    if frame_size:
                                        rects = [tuple(map(int, rect.split('x')))
                                                 for rect in contents[4].split(', ')]
                                        if rects:
                                            image_seq = list()

                                            for rect in rects:
                                                imag = pygame.Surface(frame_size)
                                                imag.blit(image, rect)
                                                image_seq.append(imag)
                                            if len(lib_name) == len(image_seq):
                                                if len(contents) > 5:
                                                    mask = self.load_image(os.path.join(root, contents[-1]))
                                                    if mask:
                                                        for i in range(len(lib_name)):
                                                            self.img_library[lib_name[i]] = image_seq[i], mask
                                                        success += 1
                                                    else:
                                                        print(os.path.join(root, contents[-1]), 'can not be loaded')
                                                        errors += 1
                                                else:
                                                    for i in range(len(lib_name)):
                                                        self.img_library[lib_name[i]] = (image_seq[i])
                                                    success += 1
                                            else:
                                                print(os.path.join(root, file), 'has wrong number of lib name(s)')
                                                errors += 1
                                        else:
                                            print(os.path.join(root, file), 'has wrong frame positions')
                                            errors += 1
                                    else:
                                        print(os.path.join(root, file), 'has wrong frame size')
                                        errors += 1
                                else:
                                    print(os.path.join(root, contents[1]), 'can not be loaded')
                                    errors += 1
                            else:
                                print(os.path.join(root, file), 'has non-unique lib name(s)')
                                errors += 1
                        else:
                            print(os.path.join(root, file), 'has wrong type')
                            errors += 1
        print('\nSprites - success loadings:', str(success) + ', errors:', errors)

# памятка разрабу:
# елемент seq_library состоит из ([картинки], время кадра, иногда маска коллизии)
# img_library выглядит проще - (картинка, +- маска)


class Map:
    def __init__(self, map_size, window_size, angeom, stgeom, colgeom, gg_spawn, angle):
        self.map_size = map_size
        self.gg_spawn = gg_spawn
        self.orig_canvas = pygame.Surface(self.map_size)
        self.orig_canvas.fill((50, 50, 50))
        self.render_canvas = self.orig_canvas
        self.bullets = Group()
        self.camera_size = window_size
        self.animated_geometry = angeom
        self.static_geometry = stgeom
        self.collision_geometry = colgeom
        v_position = (window_size[0] // 2, window_size[1] // 2)
        self.player = Player(self.gg_spawn, v_position, angle)

    def checkCollision(self):
        for geom in self.collision_geometry:
            for bullet in self.bullets:
                if (geom.rect.collidepoint(bullet.position) or 0 > bullet.position[0] or
                    bullet.position[0] > self.map_size[0] or 0 > bullet.position[1] or
                        bullet.position[1] > self.map_size[1]):
                    bullet.kill()

            overlap = pygame.sprite.collide_mask(self.player, geom)

            if overlap:

                


    def update(self, seconds):
        pass

    def render(self, seconds):
        self.render_canvas = self.orig_canvas.copy()
        self.bullets.update(seconds)
        self.checkCollision()
        self.bullets.draw(self.render_canvas)
        self.static_geometry.draw(self.render_canvas)
        self.render_canvas.blit(self.player.transformed_texture, self.player.transformed_position)
        self.render_canvas.blit(self.player.weapon.transformed_texture, self.player.weapon.transformed_position)


def get_p_fxml(prop: ET.Element):
    prop_position = prop.find('position')
    prop_position = int(prop_position.find('x').text), int(prop_position.find('y').text)
    return prop_position


def load_map(name, sprite_lib: SpriteLibrarian, sound_lib: SoundLibrarian, enemy_lib: EnemyLibrarian, win_size, version):
    tree = ET.parse(os.path.join('maps', name))
    root = tree.getroot()
    size = map(int, root.attrib['size'].split('x'))
    static_geometry = pygame.sprite.LayeredUpdates()
    animated_geometry = pygame.sprite.LayeredUpdates()
    collision_geometry = list()
    gg_spawn = list()
    enomies = list()
    if version == root.attrib['version']:
        for prop in root.find('static-geometry'):
            img_package = sprite_lib.img_library.get(prop.attrib['name'], None)
            if img_package:
                if prop.attrib['lib'] == 'static':
                    layer = prop.find('layer').text
                    static_geometry.add(StaticSprite(img_package[0], get_p_fxml(prop), int(layer)))
                elif prop.attrib['lib'] == 'animated':
                    layer = prop.find('layer').text
                    animated_geometry.add(AnimatedSprite(img_package[0], get_p_fxml(prop), img_package[1], int(layer)))
                else:
                    print(prop.attrib['lib'], 'is not a library')
            else:
                print(prop.attrib['name'], 'was not found in libraries')

        for geom in root.find('collision-geometry'):
            if geom.tag == 'collision-rect':
                rect_size = geom.find('size')
                rect_size = int(rect_size.find('width').text), int(rect_size.find('height').text)
                collision_geometry.append(ColGeom(pygame.mask.Mask(rect_size), get_p_fxml(geom)))
            elif geom.tag == 'collision-mask':
                if geom.attrib['lib'] == 'static':
                    collision_geometry.append(pygame.mask.from_surface(sprite_lib.img_library[geom.attrib['name']][-1]))
                elif geom.attrib['lib'] == 'animated':
                    collision_geometry.append(pygame.mask.from_surface(sprite_lib.seq_library[geom.attrib['name']][-1]))

        for spawn in root.find('spawn-points'):
            pos = get_p_fxml(spawn)
            rot = int(spawn.find('rotation').text)
            if spawn.attrib['type'] == 'player spawn':
                gg_spawn.append((pos, rot))
            elif spawn.attrib['type'] == 'enemy spawn':
                # TODO срочно классы бандитов мне накидали!
                enomies.append(enemy_lib.library[int(spawn.attrib('id'))](pos, rot))
            else:
                print(spawn.attrib['type'], 'is not a type of spawn points')
        gg_spawn = choice(gg_spawn)
        return Map(list(size), win_size, animated_geometry, static_geometry,
                   collision_geometry, gg_spawn[0], gg_spawn[1])
    else:
        print('Selected map is not compatible with the current version of program')
        return None
