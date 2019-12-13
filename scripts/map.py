from scripts.game_objects import *
import os
import xml.etree.ElementTree as ET
from random import choice


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

    def load_library(self, lib_path):  # TODO снести всё к хренам и построить нормально
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
                                        mask = self.load_image(os.path.join(root, contents[2]))
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


def load_map(name, libs: Librarian, version):
    tree = ET.parse(os.path.join('maps', name))
    root = tree.getroot()
    size = map(int, root.attrib['size'].split('x'))
    static_geometry = list()
    animated_geometry = list()
    collision_geometry = list()
    if version == root.attrib['version']:
        for prop in root.find('static-geometry'):
            if prop.attrib['lib'] == 'static':
                img = libs.img_library.get(prop.attrib['name'], 1)
                if img is not None:
                    prop_position = prop.find('position')
                    prop_position = int(prop_position.find('x').text), int(prop_position.find('y').text)
                    static_geometry.append(StaticSprite(img, prop_position, prop.find('rotation').text))
                else:
                    print(prop.attrib[prop.attrib['name']], 'not found in library')
            elif prop.attrib['lib'] == 'animated':
                img_seq = libs.seq_library.get(prop.attrib['name'], None)
                if img_seq is not None:
                    prop_position = prop.find('position')
                    prop_position = int(prop_position.find('x').text), int(prop_position.find('y').text)

            print(prop.attrib)
    else:
        print('Selected map not compatible with current version of program')


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
        self.render_canvas.blit(self.player.transformed_texture, self.player.transformed_position)
        self.render_canvas.blit(self.player.weapon.transformed_texture, self.player.weapon.transformed_position)