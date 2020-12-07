import pygame
import math
import random
import time
 
pygame.init()
win = pygame.display.set_mode((1280,720))
f = pygame.font.SysFont('Calibri', 30)
pygame.display.set_caption("Physiksimulation")
Objects = []
BorderLines = []
timer = 0
interval = 0.01
run = True

def interceptOnCircle(p1, p2,c, r):
	p3 = [p1[0]-c[0], p1[1]-c[1]]
	p4 = [p2[0]-c[0], p2[1]-c[1]]
	m = (p4[1] - p3[1]) / (p4[0] - p3[0])
	b = p3[1] - m * p3[0]
	underRadical = math.pow(r,2)*math.pow(m,2) + math.pow(r,2) - math.pow(b,2)
	if (underRadical < 0):return False
	else:
		t1 = (-2*m*b+2*math.sqrt(underRadical)) / (2 * math.pow(m,2) + 2)
		t2 = (-2*m*b-2*math.sqrt(underRadical)) / (2 * math.pow(m,2) + 2)
		i1 = [t1+c[0], m * t1 + b + c[1]]
		i2 = [t2+c[0], m * t2 + b + c[1]]
		if p1[0] > p2[0]:
			if (i1[0] < p1[0]) and (i1[0] > p2[0]):
				if p1[1] > p2[1]:
					if (i1[1] < p1[1]) and (i1[1] > p2[1]):return True
				if p1[1] < p2[1]:
					if (i1[1] > p1[1]) and (i1[1] < p2[1]):return True
def getDist(x0,y0,x1,y1):
	return math.sqrt((x0-x1)**2+(y0-y1)**2)

class Object:
	def __init__(self,x,y,mass,color,radius):
		self.x = x
		self.y = y
		self.color = color
		self.velocity = [random.randint(1,5),0]
		self.r = 580
		self.mass = mass
		self.radius = radius
	def move(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]
		a = -9.81
		r = self.y + 0.5 * (self.velocity[1]+self.velocity[1])*interval
		v = self.velocity[1] + a * interval
		self.y = r
		self.velocity[1] = v
	def draw(self):
		self.checkColliders()
		self.move()
		pygame.draw.circle(win, self.color, (int(self.x),720-int(self.y)), self.radius)
	def addForce(self, dir, n):
		self.velocity = [self.velocity[0] + math.cos(dir)*n,self.velocity[1] + math.sin(dir)*n]
	def checkColliders(self):
		for border in BorderLines:
			if(border.isCollided([self.x,self.y], self.radius)):
				self.bounce(border.p1, border.p2)
				return
	def bounce(self, p1, p2):
		wallAngle = abs(math.atan2(p2[1]-p1[1], p2[0]-p1[0]))
		lastPos = [self.x-self.velocity[0]*2,self.y-self.velocity[1]*2]
		ballAngle = math.atan2(lastPos[1]-self.y,lastPos[0]-self.x)
		newVelocity = self.velocity
		self.x, self.y = self.x + math.cos(ballAngle)*2 , self.y + math.sin(ballAngle)*3
		if((wallAngle>math.pi/4 and abs(wallAngle)<(math.pi*3)/4) or (wallAngle>(math.pi*5)/4 and wallAngle<(math.pi*7)/4 )):
			newVelocity = [-self.velocity[0]+math.cos((wallAngle-math.pi)*ballAngle),self.velocity[1]+math.sin((wallAngle-math.pi)*ballAngle)]
		else:
			newVelocity = [self.velocity[0]+math.cos((wallAngle-math.pi)*ballAngle),-self.velocity[1]+math.sin((wallAngle-math.pi)*ballAngle)]
		self.velocity = [round(newVelocity[0]*0.7, 2), round(newVelocity[1]*0.7, 2)]
class Border:
	def __init__(self, p1, p2, color):
		self.p1 = p1
		self.p2 = p2
		self.color = color
	def isCollided(self,circle, radius):
		return interceptOnCircle(self.p1, self.p2, circle, radius)!=False
	def draw(self):
		pygame.draw.line(win, self.color, [self.p1[0], 720-self.p1[1]], [self.p2[0], 720-self.p2[1]], 3)

for i in range(30): Objects.append(Object(random.randint(0,1280),random.randint(0,720), 10, [255,0,0], 15))
BorderLines.append(Border([700,20], [400,600], [255,255,255]))
BorderLines.append(Border([1,20], [1280,20], [255,255,255]))
BorderLines.append(Border([3,720], [10,10], [255,255,255]))

while run:
	pygame.time.delay(10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	win.fill((0,0,0))
	mouse = pygame.mouse.get_pos()
	k = pygame.key.get_pressed()
	if(k[pygame.K_d]): Objects[0].velocity[0]+=0.005
	if(k[pygame.K_a]): Objects[0].velocity[0]-=0.005
	mouse = pygame.mouse.get_pos()
	timer+=interval
	for o1 in Objects:
		o1.draw()
	for border in BorderLines:
		border.draw()
	#win.blit(f.render(str(o2.velocity), True, (255, 255, 255)), (10,10))
	pygame.display.update()
pygame.quit()