from scripts.map import *

librarian = Librarian()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

world = Map((1000, 1000), size)

fps = 60
frame_time = 0.016  # frame_time = 1 / fps

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            world.player.trackTo(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            world.player.shoot(world.bullets.add)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        world.player.move((0, -1), frame_time)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        world.player.move((0, 1), frame_time)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        world.player.move((1, 0), frame_time)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        world.player.move((-1, 0), frame_time)

    screen.fill(pygame.Color('black'))
    world.render(frame_time)
    screen.blit(world.render_canvas, (world.player.viewport_position[0] - world.player.position[0],
                                      world.player.viewport_position[1] - world.player.position[1]))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
