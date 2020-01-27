import pygame

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))

pygame.display.flip()

frame_size = (108, 64)

frame_time = 0.1

rects = [(0, 0), (108, 0), (220, 0), (324, 0), (432, 0), (540, 0), (648, 0), (756, 0), (864, 0), (972, 0), (1080, 0),
         (1188, 0), (1296, 0), (1404, 0), (1512, 0), (1620, 0), (1728, 0)]

image = pygame.image.load('data/sprites/players/Player_Bear/sprPlayerBearLegs.png')
image.set_colorkey((0, 0, 0))
image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))

image_seq = list()

for rect in rects:
    imag = pygame.Surface(frame_size, pygame.SRCALPHA)
    rect = rect[0] * -1, rect[1] * -1
    imag.blit(image, rect)
    image_seq.append(imag)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(image_seq[3], rects[0])
    pygame.display.flip()
pygame.quit()
