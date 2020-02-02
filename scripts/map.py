import os
import xml.etree.ElementTree as ET
from scripts.game_objects import *
from scripts.collision import *
import pytweening as tween


class SoundLibrarian:
    def __init__(self):
        self.sound_library = dict()

    def load_music(self, name):
        try:
            pygame.mixer.music.load(os.path.join('data/music', name + '.mp3'))
        except pygame.error:
            print(name, 'can not be loaded')

    def load_sound_library(self, lib_path):
        success = 0
        errors = 0
        for root, dirs, files in os.walk(lib_path):
            for file in files:
                if file.endswith('.ogg'):
                    try:
                        sound = pygame.mixer.Sound(os.path.join(root, file))
                    except pygame.error:
                        sound = None
                    if sound:
                        self.sound_library[file[:-4]] = sound
                        success += 1
                    else:
                        print(os.path.join(root, file), 'can not be loaded')
                        errors += 1
        print('\nSounds - success loadings:', str(success) + ', errors:', errors)


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
        return pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))

    def load_library(self, lib_path, err_func):
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
                                            self.img_library[lib_name] = image, mask
                                            success += 1
                                        else:
                                            print(os.path.join(root, contents[-1]), 'can not be loaded')
                                            errors += 1
                                    else:
                                        self.img_library[lib_name] = image,
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
                                        frame_size = tuple(map(lambda x: int(x) * 4, contents[3].split('x')))
                                    except ValueError:
                                        frame_size = None
                                    if frame_size:
                                        try:
                                            frame_time = float(contents[4])
                                        except ValueError:
                                            frame_time = None
                                        rects = [tuple(map(lambda x: int(x) * 4, rect.split('x')))
                                                 for rect in contents[5].split(', ')]
                                        if frame_time is not None:
                                            if rects:
                                                image_seq = list()

                                                for rec in rects:
                                                    imag = pygame.Surface(frame_size, pygame.SRCALPHA)
                                                    rect = rec[0] * -1, rec[1] * -1
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
                                        frame_size = tuple(map(lambda x: int(x) * 4, contents[3].split('x')))
                                    except ValueError:
                                        frame_size = None
                                    if frame_size:
                                        rects = [tuple(map(lambda x: int(x) * 4, rect.split('x')))
                                                 for rect in contents[4].split(', ')]
                                        if rects:
                                            image_seq = list()

                                            for rec in rects:
                                                imag = pygame.Surface(frame_size, pygame.SRCALPHA)
                                                rect = rec[0] * -1, rec[1] * -1
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
                                                        self.img_library[lib_name[i]] = image_seq[i],
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
        if errors:
            err_func()


# памятка разрабу:
# елемент seq_library состоит из ([картинки], время кадра, иногда маска коллизии)
# img_library выглядит проще - (картинка, +- маска)


class Map:
    def __init__(self, map_size, window_size, angeom, stgeom, colgeom, player, backgrpund, has_music, devl):
        self.map_size = map_size
        self.orig_canvas = pygame.Surface(self.map_size, pygame.SRCALPHA)
        self.background = backgrpund
        self.bullets = Group()
        self.camera_size = window_size
        self.animated_geometry = angeom
        self.static_geometry = stgeom
        self.collision_geometry = colgeom
        self.wS = window_size
        self.DL = devl
        if self.DL in (2, 3):
            for msk in colgeom:
                pygame.draw.polygon(self.orig_canvas, (255, 255, 255),
                                    [(msk.rect.x + point[0], msk.rect.y + point[1]) for point in msk.mask.outline()])
        elif self.DL == 4:
            for spr in angeom:
                pygame.draw.rect(self.orig_canvas, DEBUG_BOUNDING_BOX_COLOR, spr.rect, 1)
            for spr in stgeom:
                pygame.draw.rect(self.orig_canvas, DEBUG_BOUNDING_BOX_COLOR, spr.rect, 1)
        else:
            self.static_geometry.draw(self.orig_canvas)
        self.v_position = (window_size[0] // 2, window_size[1] // 2)
        self.player = player
        self.player.setup_shooting(self.bullets.add)
        self.overlap_img = StaticSprite(pygame.Surface((1, 1), pygame.SRCALPHA), (0, 0), 0)
        self.image = self.orig_canvas.copy()
        if has_music:
            pygame.mixer.music.play()

    def checkCollision(self):
        for geom in self.collision_geometry:
            for bullet in self.bullets:
                if (geom.rect.colliderect(bullet.rect) or 0 > bullet.rect[0] or
                        bullet.rect[0] > self.map_size[0] or 0 > bullet.rect[1] or
                        bullet.rect[1] > self.map_size[1]):
                    bullet.kill()

            overlap = pygame.sprite.collide_mask(self.player, geom)
            if overlap:
                overlap = maskcollide(self.player, geom)
                overlist = [(self.player.rect.x + point[0], self.player.rect.y + point[1]) for point in
                            overlap.outline(PHYSICS_QUALITY)]
                if self.DL == 3:
                    overlap = copy(overlist)
                min_point = min(overlist,
                                key=lambda x: math.sqrt((x[0] - self.player.center[0]) ** 2 +
                                                        (x[1] - self.player.center[1]) ** 2))
                indexes = list()

                # ---------------------This can be deleted to speed up collision-------------------------
                olist1 = [(self.player.rect.x + point[0],
                           self.player.rect.y + point[1]) for point in self.player.mask.outline(PHYSICS_QUALITY)]
                olist2 = [(geom.rect.x + point[0],
                           geom.rect.y + point[1]) for point in geom.mask.outline(PHYSICS_QUALITY)]

                for i in range(len(overlist)):
                    if overlist[i] in olist2 and overlist[i] not in olist1:
                        indexes.append(i)

                for index in sorted(indexes, reverse=True):
                    del overlist[index]
                # ----------------------------------------------------------------------------------------

                cf = abs(zerodiv(self.player.center[0] - min_point[0], self.player.center[1] - min_point[1]))
                if overlist:
                    max_point = min(overlist, key=lambda x: abs(cf - abs(zerodiv(self.player.center[0] - x[0],
                                                                                 self.player.center[1] - x[1]))))
                else:
                    max_point = min_point
                if self.DL == 3:
                    return overlap, min_point, max_point
                if abs(max_point[0] - min_point[0]) > PHYSICS_QUALITY or abs(
                        max_point[1] - min_point[1]) > PHYSICS_QUALITY:
                    offsetx = min_point[0] - max_point[0]
                    offsety = min_point[1] - max_point[1]
                    if offsetx < 0:
                        self.player.teleport((offsetx + 1, 0))
                    else:
                        self.player.teleport((offsetx - 1, 0))
                    if offsety < 0:
                        self.player.teleport((0, offsety + 1))
                    else:
                        self.player.teleport((0, offsety - 1))
                    self.player.legs.reset()

    def update(self, dt, mouse_pos, w_s, devl, dbc):
        self.dbc = dbc
        if self.DL != devl:
            self.DL = devl
            self.orig_canvas = pygame.Surface(self.map_size, pygame.SRCALPHA)
            if self.DL in (2, 3):
                for msk in self.collision_geometry:
                    pygame.draw.polygon(self.orig_canvas, (255, 255, 255),
                                        [(msk.rect.x + point[0], msk.rect.y + point[1]) for point in
                                         msk.mask.outline()])
            elif self.DL == 4:
                for spr in self.static_geometry:
                    pygame.draw.rect(self.orig_canvas, dbc, spr.rect, 1)
                for spr in self.animated_geometry:
                    pygame.draw.rect(self.orig_canvas, dbc, spr.rect, 1)
            else:
                self.static_geometry.draw(self.orig_canvas)
        if w_s != self.wS:
            self.v_position = (w_s[0] // 2, w_s[1] // 2)
            self.background.resize(w_s)
            self.wS = w_s
        self.player.rotation = math.degrees(math.atan2(mouse_pos[1] - self.v_position[1],
                                            mouse_pos[0] - self.v_position[0]))
        self.player.update(mouse_pos, dt, self.v_position, devl, dbc)
        self.animated_geometry.update(dt)
        self.bullets.update(dt)

    def render(self, rm):
        self.image = self.orig_canvas.copy()
        self.bullets.draw(self.image)
        if rm in (0, 1):
            self.animated_geometry.draw(self.image)
        overlap = self.checkCollision()
        self.image.blit(self.player.image, self.player.o_rect)
        r = math.degrees(math.atan2(abs(self.map_size[1] // 2 - self.player.center[1]),
                                    abs(self.map_size[0] // 2 - self.player.center[0])))
        if r > 45:
            r = 90 - r
        r = tween.easeInOutSine(r / 45)
        if overlap:
            if len(overlap[0]) > 2:
                pygame.draw.polygon(self.image, (255, 120, 120), overlap[0], 0)
                pygame.draw.line(self.image, (120, 130, 130), overlap[1], overlap[2], 2)
        self.image = pygame.transform.rotate(self.image, r)
        if self.DL == 4:
            pygame.draw.rect(self.image, self.dbc, self.image.get_rect(), 2)


def get_p_fxml(prop: ET.Element):
    prop_position = prop.find('position')
    prop_position = int(prop_position.find('x').text), int(prop_position.find('y').text)
    return prop_position


def load_map(name, sprite_lib, sound_lib, win_size, version, err_func, devl, brt):
    tree = ET.parse(os.path.join('data', name))
    root = tree.getroot()
    size = list(map(int, root.attrib['size'].split('x')))
    static_geometry = pygame.sprite.LayeredUpdates()
    animated_geometry = pygame.sprite.LayeredUpdates()
    collision_geometry = list()

    has_music = False
    gg = list()
    if version == root.attrib['version']:
        for ex in root.find('background'):
            if ex.tag == 'music':
                sound_lib.load_music(ex.text)
                pygame.mixer.music.set_volume(float(ex.attrib['volume']) / 100)
                has_music = True
        background = BACKGROUND_DB[int(root.findall('background')[0].attrib['id'])](sprite_lib, win_size, brt)
        for prop in root.find('static-geometry'):
            img_package = sprite_lib.img_library.get(prop.attrib['name'], None)
            seq_package = sprite_lib.seq_library.get(prop.attrib['name'], None)
            if img_package or seq_package:
                if prop.attrib['lib'] == 'static':
                    layer = prop.find('layer').text
                    pos = get_p_fxml(prop)
                    tiled = prop.attrib.get('tiled', None)
                    if tiled:
                        tiled = list(map(int, tiled.split('x')))
                        for y in range(tiled[1]):
                            for x in range(tiled[0]):
                                static_geometry.add(StaticSprite(img_package[0], (pos[0] +
                                                                                  img_package[0].get_width() * x,
                                                                                  pos[1] +
                                                                                  img_package[0].get_height() * y),
                                                                 int(layer)))
                    else:
                        static_geometry.add(StaticSprite(img_package[0], pos, int(layer)))
                elif prop.attrib['lib'] == 'animated':
                    layer = prop.find('layer').text
                    rot = prop.attrib.get('rotation', None)
                    if rot:
                        rot = int(rot)
                        animated_geometry.add(AnimatedSprite(seq_package[0], get_p_fxml(prop), seq_package[1],
                                                             int(layer), rot))
                else:
                    print(prop.attrib['lib'], 'is not a library')
            else:
                print(prop.attrib['name'], 'was not found in libraries')

        for geom in root.find('collision-geometry'):
            if geom.tag == 'collision-rect':
                rect_size = geom.find('size')
                rect_size = int(rect_size.find('width').text), int(rect_size.find('height').text)
                tiled = geom.attrib.get('tiled', None)
                pos = get_p_fxml(geom)
                if tiled:
                    tiled = list(map(int, tiled.split('x')))
                    for y in range(tiled[1]):
                        for x in range(tiled[0]):
                            collision_geometry.append(ColGeom(pygame.mask.Mask(rect_size, fill=True), (pos[0] +
                                                                                                       rect_size[0] * x,
                                                                                                       pos[1] +
                                                                                                       rect_size[1] * y)
                                                              ))
                else:
                    collision_geometry.append(ColGeom(pygame.mask.Mask(rect_size, fill=True), pos))
            elif geom.tag == 'collision-mask':
                if geom.attrib['lib'] == 'static':
                    collision_geometry.append(ColGeom(
                        pygame.mask.from_surface(sprite_lib.img_library[geom.attrib['name']][-1]), get_p_fxml(geom)))
                elif geom.attrib['lib'] == 'animated':
                    collision_geometry.append(ColGeom(
                        pygame.mask.from_surface(sprite_lib.seq_library[geom.attrib['name']][-1]), get_p_fxml(geom)))
        for spawn in root.find('spawn-points'):
            pos = get_p_fxml(spawn)
            rot = int(spawn.find('rotation').text)
            if spawn.attrib['type'] == 'player spawn':
                gg.append(PLAYERS_DB[int(spawn.attrib['id'])](sound_lib, sprite_lib, pos, rot, err_func))
            elif spawn.attrib['type'] == 'enemy spawn':
                pass
            else:
                print(spawn.attrib['type'], 'is not a type of spawn points')
        gg = choice(gg)
        return Map(list(size), win_size, animated_geometry, static_geometry,
                   collision_geometry, gg, background, has_music, devl)
    else:
        print('Selected map is not compatible with the current version of program')
        return None
