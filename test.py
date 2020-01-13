from math import atan2, degrees
import pygame
from data.classes.weapons import BearGuns
from scripts.map import SpriteLibrarian
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))
print(degrees(atan2(2, 14)))
fps = 60
frame_time = 0.016

running = True
clock = pygame.time.Clock()

libs = SpriteLibrarian()
libs.load_library('data/sprites')
bear_guns = BearGuns(libs.img_library['sprBullet'][0], libs.seq_library['sprPlayerBearArm'][0])
player_pos = (400, 300)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            bear_guns.update(45, player_pos, event.pos)
    screen.fill(pygame.Color('black'))
    screen.blit(bear_guns.mt, (400 - 353 // 2, 300 - 353 // 2))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
