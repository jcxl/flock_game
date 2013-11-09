import math
import os
import pygame

wd = os.path.split(os.path.abspath(__file__))[0]

#functions to create our resources
def load_image(name, colorkey=None):
	image = pygame.image.load(os.path.join(wd, name))
	image = image.convert_alpha()

	if colorkey != None:
		if colorkey == -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey)

	return image, image.get_rect()


class Unit(pygame.sprite.Sprite):

	def __init__(self, entity):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		
		self.entity = entity
		init_position = self.entity.get_rect().center

		self.image0, self.rect0 = load_image('birdie.png')
		self.image = self.image0
		self.rect = self.rect0.move(init_position)

		screen = pygame.display.get_surface()
		self.area = screen.get_rect()

	def update(self):
		self.image, self.rect = self.do_yaw(self.rect, self.entity.velocity)
	
		self.rect = self.rect.move(self.entity.velocity[0], self.entity.velocity[1])

	def do_yaw(self, rect, velocity):	
		angle = math.atan2(velocity[1], velocity[0])
		print str(math.degrees(angle))
		oldcent = rect.center
		newsurf = pygame.transform.rotate(self.image0, 270-math.degrees(angle))
		newrect = newsurf.get_rect()
		newrect.center = oldcent
		return newsurf, newrect

	def calcnewpos(self, rect, vector):
		(angle, z) = vector
		(dx, dy) = (z*math.sin(-angle), z*math.cos(angle))
		return rect.move(dx, dy)


