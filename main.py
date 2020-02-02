from scripts.user_interface import *
import sqlite3


class SettingsManager:
    def __init__(self, name):
        self.name = name
        sql_con = sqlite3.connect(self.name)
        cur = sql_con.cursor()

        sql_update_query = 'SELECT * FROM settings'
        dat = cur.execute(sql_update_query).fetchall()
        sql_con.commit()
        cur.close()
        self.DL = dat[0][1]
        self.BGRT = dat[0][2]
        self.DBBC = tuple(map(int, dat[0][3].split('.')))

    def update_DL(self, DL):
        sql_con = sqlite3.connect(self.name)
        cur = sql_con.cursor()

        sql_update_query = 'UPDATE settings SET DEBUG_LEVEL = ? WHERE id = 0'
        cur.execute(sql_update_query, (DL, ))
        sql_con.commit()
        cur.close()
        self.DL = DL

    def update_BGRT(self, BGRT):
        sql_con = sqlite3.connect(self.name)
        cur = sql_con.cursor()

        sql_update_query = 'UPDATE settings SET BG_RENDER_TYPE = ? WHERE id = 0'
        cur.execute(sql_update_query, (BGRT, ))
        sql_con.commit()
        cur.close()
        self.BGRT = BGRT

    def update_DBBC(self, DBBC):
        sql_con = sqlite3.connect(self.name)
        cur = sql_con.cursor()

        sql_update_query = 'UPDATE settings SET DEBUG_BB_COLOR = ? WHERE id = 0'
        cur.execute(sql_update_query, (str(DBBC[0]) + "." + str(DBBC[1]) + "." + str(DBBC[2]), ))
        sql_con.commit()
        cur.close()
        self.DBBC = DBBC


set_manager = SettingsManager('sys.db')

set_manager.update_DBBC((0, 255, 0))

text = Font('fntScore.fnt')
debtext = Font('fntRestart.fnt')

fps = 60
frame_time = 0.016

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
screen.fill(pygame.Color('black'))

pygame.display.set_caption('Hotline NN')

pygame.display.flip()

pygame.mouse.set_visible(False)

sprite_lib = SpriteLibrarian()
sprite_lib.load_library('data/sprites', print)

hud = HUD(size, sprite_lib, text)

pygame.display.set_icon(sprite_lib.img_library['TitleIcon32'][0])

cur_spr = sprite_lib.seq_library.get('sprCursor', None)
if not cur_spr:
    print('Cursor is broken')
    t = pygame.Surface((1, 1))
    t.set_colorkey((0, 0, 0))
    cur_spr = [t, t], 1

cursor = AnimSeq(cur_spr[0], cur_spr[1])

sound_lib = SoundLibrarian()
sound_lib.load_sound_library('data/sounds')

world = load_map('maps/map.xml', sprite_lib, sound_lib, size, '0.1.Lite', print, set_manager.DL, set_manager.BGRT)
world.player.set_weapon('BearGuns')

paused_bg = None
pause_screen = SettingScreen(sprite_lib, set_manager)

mouse_pos = 0, 0
poff = 0, 0

world.player.take_out_guns()

running = True
paused = False
clock = pygame.time.Clock()

while running:
    s = clock.get_fps()
    s = frame_time if s < 10 else zerodiv(1, s)  # стабилизация fps после смены размеров окна

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            size = event.dict['size']
            resize_flag = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = False if paused else True
                pygame.mouse.set_visible(paused)
                if paused:
                    pygame.display.set_mode(size)
                else:
                    pygame.display.set_mode(size, pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN and paused:
            pause_screen.check((mouse_pos[0] - poff[0], mouse_pos[1] - poff[1]))
    if paused:
        if not paused_bg:
            paused_bg = pygame.Surface(size)
            paused_bg.blit(world.background.image, (0, 0))
            paused_bg.blit(world.image, (world.v_position[0] - world.player.center[0],
                                         world.v_position[1] - world.player.center[1]))
            black_bg = pygame.Surface(size, pygame.SRCALPHA)
            black_bg.fill((0, 0, 0, 128))
            paused_bg.blit(black_bg, (0, 0))
        screen.blit(paused_bg, (0, 0))
        poff = (size[0] - pause_screen.image.get_width()) // 2, (size[1] - pause_screen.image.get_height()) // 2
        screen.blit(pause_screen.image, poff)

    else:
        paused_bg = None
        keys = pygame.key.get_pressed()
        mbut = pygame.mouse.get_pressed()
        vec = [0, 0]
        if mbut[0]:
            world.player.current_weapon.shootb(s)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            vec[1] = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            vec[1] = 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vec[0] = 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vec[0] = -1

        cursor.update(s)

        world.player.move(vec, s)
        world.update(s, mouse_pos, size, set_manager.DL, set_manager.DBBC)
        world.render(set_manager.DL)

        screen.blit(world.background.image, (0, 0))
        world.background.update(s, set_manager.BGRT)
        screen.blit(world.image, (world.v_position[0] - world.player.center[0],
                                  world.v_position[1] - world.player.center[1]))
        screen.blit(cursor.image, (mouse_pos[0] - 28, mouse_pos[1] - 28))
        hud.update(0, world.player, size)
        screen.blit(hud.image, (0, 0))
    if set_manager.DL == 1:
        fps_screen = Font('fntRestart.fnt').get_surface('Current fps:   ' + str(round(clock.get_fps(), 2)), alpha=False)
        screen.blit(fps_screen, ((size[0] - fps_screen.get_width()) // 2, 0))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
