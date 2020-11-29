# Imports

import pygame
import math
import random
import time

pygame.init()
win = pygame.display.set_mode((600,600))
f = pygame.font.SysFont('Calibri', 30)
pygame.display.set_caption("Physiksimulation nach Newton")
Objects = []
timer = 0
run = True
G = 6.67*(10**-11)

def getGForce(m1,m2, dist):
	return G*(m1*m2)/dist**2

def getDist(x0,y0,x1,y1):
	return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Object:
	def __init__(self,x,y,mass,color):
		self.x = x
		self.y = y
		self.mass = mass
		self.velocity = [0.0,0.0]
		self.color = color
	def move(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]
	def draw(self):
		pygame.draw.circle(win, self.color, (self.x,self.y), 20)
	def addForce(self, dir, n):
		self.velocity = [math.cos(dir)*n,math.sin(dir)*n]
for i in range(50):
	Objects.append(Object(random.randint(0,600), random.randint(0,600), 10000000, [random.randint(50,255),0,0]))
while run:
	pygame.time.delay(2)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	win.fill((0,0,0))
	k = pygame.key.get_pressed()
	mouse = pygame.mouse.get_pos()
	if(k[pygame.K_SPACE]):timer+=0.01
	for o1 in Objects:
		o1.draw()
		if not(k[pygame.K_SPACE]): continue
		o1.move()
		for o2 in Objects:
			if(o1!=o2):
				force = getGForce(o1.mass, o2.mass, getDist(o1.x,o1.y,o2.x,o2.y))
				if(force>10): force = 0
				o1.addForce(math.atan2(o2.y-o1.y,o2.x-o1.x), force)
	win.blit(f.render(str(round(timer, 3)), True, (255, 255, 255)), (10,10))
	pygame.display.update()
pygame.quit()
