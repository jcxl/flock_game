import pygame
from pygame import gfxdraw
import random
import util
import bird

from pygame import locals
from pygame import color

config = {"size": (800, 600),
    "num_birds": 10,
    "FPS": 60}

bird_list = []
util.populate(bird_list, config)

pygame.init()
screen = pygame.display.set_mode(config["size"])
pygame.display.set_caption("Flocking")

screen.fill(color.THECOLORS['black'])

clock = pygame.time.Clock()

done = False

while not done:
    dt = clock.tick(config["FPS"])
    screen.fill(color.THECOLORS['black'])

    for b in bird_list:
        rect = b.get_rect()
        gfxdraw.box(screen, rect, color.THECOLORS['white'])

    pygame.display.update()
    events = pygame.event.get()
    for e in events:
        if( e.type == locals.QUIT ):
            done = True
            break