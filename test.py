import pygame

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

pygame.display.flip()

sound = pygame.mixer.Sound('data/sounds/sndCatchFire.ogg')
