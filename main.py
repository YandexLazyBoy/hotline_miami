from scripts.map import *
import pygame

fps = 60
frame_time = 0.016

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

pygame.display.flip()

pygame.mouse.set_visible(False)

sprite_lib = SpriteLibrarian()
sprite_lib.load_library('data/sprites', print)

cur_spr = sprite_lib.seq_library.get('sprCursor', None)
if not cur_spr:
    print('Cursor is broken')
    t = pygame.Surface((1, 1))
    t.set_colorkey((0, 0, 0))
    cur_spr = [t, t], 1

cursor = AnimSeq(cur_spr[0], cur_spr[1])
print(cursor.image)

sound_lib = SoundLibrarian()
# sound_lib.load_sound_library('data/sounds')

world = load_map('maps/map.xml', sprite_lib, sound_lib, size, '0.1.Lite', print)
world.player.set_weapon('BearGuns')
mouse_pos = 0, 0

world.player.take_out_guns()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

    keys = pygame.key.get_pressed()
    mbut = pygame.mouse.get_pressed()
    vec = [0, 0]
    if mbut[0]:
        world.player.current_weapon.shootb(frame_time)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        vec[1] = -1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        vec[1] = 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vec[0] = 1
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vec[0] = -1

    cursor.update(frame_time)

    world.player.move(vec, frame_time)
    world.update(frame_time, mouse_pos)

    screen.fill(pygame.Color('black'))
    screen.blit(world.render(), (world.v_position[0] - world.player.center[0],
                                 world.v_position[1] - world.player.center[1]))
    screen.blit(cursor.image, (mouse_pos[0] - 28, mouse_pos[1] - 28))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
