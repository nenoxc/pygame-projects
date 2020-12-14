import pygame
import math
import random
import time
 
pygame.init()
w = 1280
h = 720
win = pygame.display.set_mode((w,h))
f = pygame.font.SysFont('Calibri', 30)
pygame.display.set_caption("Physiksimulation")
Objects = []
BorderLines = []
timer = 0
interval = 0.01
bounceStrength = 0.7
run = True
pos = [0,0]
a = -0.981
clock = pygame.time.Clock()

def getDist(x0,y0,x1,y1):
	return abs(math.sqrt((x0-x1)**2+(y0-y1)**2))

class Object:
	def __init__(self,x,y,mass,color,radius, startspeed=[0,0]):
		self.x = x
		self.y = y
		self.color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
		self.velocity = startspeed
		self.r = 580
		self.mass = mass
		self.radius = radius
	def move(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]
		v = self.velocity[1] + a * interval
		self.velocity[1] = v
	def draw(self):
		self.checkColliders()
		self.move()
		pygame.draw.circle(win, self.color, (int(self.x),h-int(self.y)), self.radius)
	def addForce(self, dir, n):
		self.velocity = [self.velocity[0] + math.cos(dir)*n,self.velocity[1] + math.sin(dir)*n]
	def checkColliders(self):
		for border in BorderLines:
			if(border.isCollided([self.x,self.y], self.radius)):
				self.bounce(border.p1, border.p2)
				return
	def bounce(self, p1, p2):
		wallAngle = abs(math.atan2(p1[1]-p2[1], p1[0]-p2[0]))
		lastPos = [self.x-self.velocity[0]*2,self.y-self.velocity[1]*2]
		ballAngle = math.atan2(lastPos[1]-self.y,lastPos[0]-self.x)
		angle = abs((ballAngle) - 2*wallAngle-math.pi)
		ov = (abs(self.velocity[0])+abs(self.velocity[1]))*bounceStrength
		self.velocity = [math.cos(angle)*ov,math.sin(angle)*ov]
		self.x += self.velocity[0]
		self.y += self.velocity[1]
class Border:
	def __init__(self, p1, p2, color):
		if(p1[1]>=p2[1]):
			self.p1 = p1
			self.p2 = p2
		else:
			self.p1 = p2
			self.p2 = p1
		self.color = color
	def isCollided(self,circle, radius):
		dist1 = getDist(circle[0], circle[1],self.p1[0],self.p1[1])
		dist2 = getDist(circle[0], circle[1],self.p2[0],self.p2[1])
		length = getDist(self.p1[0],self.p1[1],self.p2[0],self.p2[1])
		if(int((dist1+dist2)-length)==0):
			return True
		return False
	def draw(self):
		pygame.draw.line(win, self.color, [self.p1[0], 720-self.p1[1]], [self.p2[0], 720-self.p2[1]], 3)

BorderLines.append(Border([0,20], [1280,20], [255,255,255]))
mouseSpeed = [0,0]
oldMousepos = [0,0]
while run:
	clock.tick(165)
	mb = pygame.mouse.get_pressed()
	k = pygame.key.get_pressed()
	mouse = pygame.mouse.get_pos()
	mouseSpeed = [mouse[0]-oldMousepos[0],(700-mouse[1])-(700-oldMousepos[1])]
	oldMousepos = mouse
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			mb = pygame.mouse.get_pressed()
			if(mb[0]): pos = [mouse[0], h-mouse[1]]
			if(mb[2]): BorderLines.append(Border(pos, [mouse[0], h-mouse[1]], [255,255,255]))
	win.fill((0,0,0))
	if(mb[1]):Objects.append(Object(mouse[0],720-mouse[1], 10, [255,0,0], 5, startspeed=mouseSpeed))
	mouse = pygame.mouse.get_pos()
	timer+=interval
	win.blit(f.render(str(int(clock.get_fps())), True, [255,255,255]), (50,50))
	win.blit(f.render(str(len(Objects)), True, [255,255,255]), (200,50))
	for o1 in Objects:
		o1.draw()
	for border in BorderLines:
		border.draw()
	#win.blit(f.render(str(o2.velocity), True, (255, 255, 255)), (10,10))
	pygame.display.update()
pygame.quit()