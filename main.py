from scripts.map import *
import pygame

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

pygame.display.flip()

sprite_lib = SpriteLibrarian()
sprite_lib.load_library('data/sprites', print)

sound_lib = SoundLibrarian()
# sound_lib.load_sound_library('data/sounds')

world = load_map('maps/map.xml', sprite_lib, sound_lib, size, '0.1.Lite', print)
mouse_pos = 0, 0

# world.player.take_out_guns()

fps = 60
frame_time = 0.016

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            world.player.current_weapon.shoot()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        world.player.move((0, -1), frame_time)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        world.player.move((0, 1), frame_time)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        world.player.move((1, 0), frame_time)
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        world.player.move((-1, 0), frame_time)

    world.update(frame_time, mouse_pos)

    screen.fill(pygame.Color('black'))
    screen.blit(world.render(), (world.v_position[0] - world.player.center[0],
                                 world.v_position[1] - world.player.center[1]))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
