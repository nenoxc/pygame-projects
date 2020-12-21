import pygame
import math
import random
import time
 
pygame.init()
w = 1920
h = 1080
win = pygame.display.set_mode((w,h))
f = pygame.font.SysFont('Calibri', 30)
pygame.display.set_caption("Physiksimulation")
Objects = []
timer = 0
interval = 0.1
run = True
G = 6.67*(10**-11)

def getGForce(m1,m2, dist):
	return G*(m1*m2)/dist**2

def getDist(x0,y0,x1,y1):
	return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Object:
	def __init__(self,x,y,mass,color,radius):
		self.x = x
		self.y = y
		self.color = color
		self.velocity = [0,-1]
		self.r = 580
		self.mass = mass
		self.radius = radius
		self.lastPos = [x, y]
	def move(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]
		#if(getDist(self.x,self.y,Objects[0].x,Objects[0].y)<=15 and self!=Objects[0]): Objects.pop(Objects.index(self))
		return
	def draw(self):
		pygame.draw.circle(win, self.color, (int(self.x),h-int(self.y)), self.radius)
		self.move()
	def addForce(self, dir, n):
		self.velocity = [self.velocity[0] + math.cos(dir)*n,self.velocity[1] + math.sin(dir)*n]

Objects.append(Object(w/2,h/2, 1000000000, [255,255,0], 10))
for i in range(10000): Objects.append(Object(random.randint(0, w),random.randint(0, h), 10000000/1000, [255,0,0], 1))
Objects[0].velocity = [0,0]


while run:
	pygame.time.delay(1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#if event.type == pygame.MOUSEBUTTONDOWN:
		#Objects[0].x, Objects[0].y = pygame.mouse.get_pos()[0], 720-pygame.mouse.get_pos()[1]
	win.fill((0,0,0))
	mouse = pygame.mouse.get_pos()
	k = pygame.key.get_pressed()
	if(k[pygame.K_w]): Objects[0].y+=1
	if(k[pygame.K_a]): Objects[0].x-=1
	if(k[pygame.K_s]): Objects[0].y-=1
	if(k[pygame.K_d]): Objects[0].x+=1
	mouse = pygame.mouse.get_pos()
	timer+=interval
	for o1 in Objects:
		o1.draw()
	o1 = Objects[0]
	for o in Objects:
		if(o!=o1):
			force = getGForce(o1.mass, o.mass, getDist(o1.x,o1.y,o.x,o.y))
			o.addForce(math.atan2(o1.y-o.y,o1.x-o.x), force)
	#win.blit(f.render(str(o2.velocity), True, (255, 255, 255)), (10,10))
	pygame.display.update()
pygame.quit()