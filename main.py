import pygame
from pygame import gfxdraw
import util
import config

import unit

from pygame import locals
from pygame import color

config = config.config;

prey_list = []
predator_list = []
util.populate_prey(prey_list, config)
util.populate_predator(predator_list,config)

pygame.init()
screen = pygame.display.set_mode(config["size"])
pygame.display.set_caption("The Birds")

screen.fill(color.THECOLORS['lightslategray'])

clock = pygame.time.Clock()

prey_sprites = pygame.sprite.RenderPlain()
for b in prey_list:
	new_sprite = unit.Unit(b, 'prey')
	prey_sprites.add(new_sprite)

predator_sprites = pygame.sprite.RenderPlain()
for p in predator_list:
    new_sprite = unit.Unit(p, 'predator')
    predator_sprites.add(new_sprite)

done = False
while not done:
    dt = clock.tick(config["FPS"])
	
    screen.fill(color.THECOLORS['lightslategray'])
	
    prey_sprites.update()
    prey_sprites.draw(screen)

    predator_sprites.update()
    predator_sprites.draw(screen)

    for b in prey_list:
        b.tick(prey_list, predator_list)
        rect = b.get_rect()

    for p in predator_list:
        p.tick(prey_list, predator_list)
        rect = p.get_rect()

    pygame.display.update()
    events = pygame.event.get()
    for e in events:
        if( e.type == locals.QUIT ):
            done = True
            break
