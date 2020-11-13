# Imports
import pygame,math,random,time

import pygame
import random
import math
from pygame import gfxdraw

pygame.init()

particles = []

def add(seed_x,seed_y,color,offset,force,size,window): particles.append(Particle(seed_x,seed_y,color,offset,force,size,window))
def addCP(surface,x,y,color,offset,radius): particles.append(CirculatingParticle(x,y,color,offset,radius,surface))
def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

class Particle:
    def __init__(self,seed_x,seed_y,color,offset,force,size,window):
        self.win = window
        self.x = seed_x
        self.y = seed_y
        self.offset = offset
        self.seed_x = seed_x
        self.seed_y = seed_y
        self.dir = random.randint(-5,5)
        if(self.dir==0): self.dir+=1
        self.color = color
        self.radius = abs(self.dir)+size
        self.velocity = 10
        self.height = -force+5
    def show(self):
        self.fly()
        draw_circle(self.win, int(self.x + self.offset[0] + self.radius / 4), int(self.y + self.offset[1] + self.radius / 4),int(self.radius), subtract(self.color, [20,20,20]))
        draw_circle(self.win, int(self.x + self.offset[0]), int(self.y + self.offset[1]), int(self.radius), self.color)
    def fly(self):
        if(self.velocity>0):
            self.velocity -= 1
        self.height += 0.25
        self.y += self.height*0.1
        self.x += (self.dir*self.velocity)*0.08
        self.radius -= 0.3
        if(self.radius<=0):
            self.remove()
    def remove(self):
        particles.pop(particles.index(self))

class CirculatingParticle(Particle):
    def __init__(self,seed_x,seed_y,color,offset,radius,window):
        self.seed_x = seed_x
        self.seed_y = seed_y
        self.offset = offset
        self.color = color
        self.radius = radius+random.randint(-30,30)
        self.r = radius
        self.pos = random.randint(1,360)
        self.dir = random.choice([-0.05,0.05])
        self.win = window
    def show(self):
        self.fly()
        x = self.seed_x + self.offset[0] + math.cos(self.pos) * self.r
        y = self.seed_y + self.offset[1] + math.sin(self.pos) * self.r
        pygame.draw.rect(self.win, self.color, (x, y, 5, 5))
    def fly(self):
        self.pos += self.dir/(self.radius/50)

fps = 60
movement_speed = 1

od = {
    "up": "down",
    "down": "up",
    "right": "left",
    "left": "right"
}

map_jumps = [
    [3,4,12],
    [5,6,3],
    [15,15,15],
    [100,100,100],
    [100,100,100],
    [100,100,100],
    [100,100,100],
    [100,100,100],
]

class Dirs:
    def __init__(self):
        self.up = "up"
        self.down = "down"
        self.left = "left"
        self.right = "right"
Directions = Dirs()

def subtract(arr1,arr2):
    return [e - arr2[c] for c, e in enumerate(arr1)]

pygame.init()
win = pygame.display.set_mode((900, 600), pygame.DOUBLEBUF)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
win.set_alpha(None)
w, h = pygame.display.get_surface().get_size()
clock = pygame.time.Clock()

EntityPool = []
Timeouts = []
run = True
px = 30

maps = ["map1.txt", "map2.txt", "map3.txt","map4.txt", "map5.txt", "map6.txt"]
current_map = 0

walkSound = pygame.mixer.Sound("sounds/walk.ogg")
jumpSound = pygame.mixer.Sound("sounds/jump.ogg")
portalSound = pygame.mixer.Sound("sounds/portal.ogg")
checkpointSound = pygame.mixer.Sound("sounds/checkpoint.ogg")

pygame.mixer.music.load("sounds/music.ogg")
pygame.mixer.music.play(-1)

textFont = pygame.font.Font("fonts/I-pixel-u.ttf", 20)
pygame.display.set_caption("Keybreaker build-0.3")
background = pygame.image.load("images/bg.png").convert_alpha()

keys = [pygame.image.load("images/ui/left0.png"),pygame.image.load("images/ui/right0.png"),pygame.image.load("images/ui/up0.png"),pygame.image.load("images/ui/left1.png"),pygame.image.load("images/ui/right1.png"),pygame.image.load("images/ui/up1.png")]

class Cube:
    def __init__(self, posx, posy, color, width, height, collidable, type):
        self.x = posx
        self.y = posy
        self.color = color
        self.defaultcolor = color
        self.width = width
        self.offset = [w/3, h/3]
        self.height = height
        self.type = type
        self.kinematic = False
        self.surface = pygame.Surface((self.width, self.height))
        self.collidable = collidable
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((self.color[0], self.color[1], self.color[2]))
        self.window_x = self.x + self.offset[0]
        self.window_y = self.y + self.offset[1]
        win.blit(self.surface, (self.window_x, self.window_y))
    def is_collided_with(self, rectangle):
        return self.rect.colliderect(rectangle)
    def will_collide_with(self, sprite, facing, length):
        if (facing == Directions.up):
            nrect = pygame.Rect(sprite.x, sprite.y + length, sprite.width, sprite.height)
        if (facing == Directions.down):
            nrect = pygame.Rect(sprite.x, sprite.y - length, sprite.width, sprite.height)
        if (facing == Directions.right):
            nrect = pygame.Rect(sprite.x - length, sprite.y, sprite.width, sprite.height)
        if (facing == Directions.left):
            nrect = pygame.Rect(sprite.x + length, sprite.y, sprite.width, sprite.height)
        return self.is_collided_with(nrect)
    def move(self, dir, speed):
        for entity in EntityPool:
            if(entity==LocalPlayer): continue
            if (self.will_collide_with(entity, dir, speed) and not self.is_collided_with(entity.rect) and entity.collidable):
                if(entity.type=="moveable"):
                    entity.move(dir,speed)
                if(entity.type=="kill_cube" and self==LocalPlayer):
                    LocalPlayer.kill()
                return dir
        if (dir == Directions.up):
            self.y -= speed
        elif (dir == Directions.down):
            self.y += speed
        elif (dir == Directions.left):
            self.x -= speed
        elif (dir == Directions.right):
            self.x += speed
        if(self==LocalPlayer):
            pass
        return True
    def getMid(self):
        return [int(self.x+self.width/2), int(self.y+self.height/2)]
class SpriteObject(Cube):
    def __init__(self, posx, posy, color,image, width, height, collidable, type):
        super().__init__(posx, posy, color, width, height, collidable, type)
        self.image = pygame.image.load(image).convert_alpha()
    def draw(self):
        if (self.type == "moveable"):
            self.move(Directions.down, 2)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        win.blit(pygame.transform.smoothscale(self.image, (self.width, self.height)),(self.x + self.offset[0], self.y + self.offset[1]))
        self.window_x = self.x + self.offset[0]
        self.window_y = self.y + self.offset[1]

class Animation:
    def __init__(self, frames, timing):
        self.frames = []
        self.timing = timing
        for frame in frames:
            self.frames.append(pygame.image.load(frame).convert_alpha())
        self.index = 0
        self.count = 0
        self.maxindex = len(frames) - 1
    def get(self):
        self.img = self.frames[self.index]
        self.count += 1
        if(self.count>self.timing):
            self.count = 0
            self.index += 1
        if(self.index>self.maxindex): self.index = 0
        return self.img

class Player(Cube):
    def __init__(self, posx, posy, color, width, height):
        super().__init__(posx, posy, color, width, height, True, "player")
        self.steps = 0
        self.horizontal = False
        self.speed = 1
        self.jumping = False
        self.jumpPower = 2
        self.jumps = self.jumpPower*15
        self.currentCheckpoint = None
        self.moving = False
        leastx = 999
        cp = None
        for e in EntityPool:
            if(e.type=="checkpoint"):
                if(e.x<leastx): cp = e
        self.currentCheckpoint = cp
        self.anim_frame = PlayerAnimation.get()
        self.presses_left = map_jumps[0]
        self.checkpointPressesLeft = subtract(map_jumps[0],[0,0,0])
    def draw(self):
        self.window_x = self.x + self.offset[0]
        self.window_y = self.y + self.offset[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(win, [255,0,0], (self.window_x,self.window_y, self.width,self.height))
        win.blit(pygame.transform.smoothscale(pygame.transform.flip(self.anim_frame, self.horizontal, False), (self.width,self.height)), (self.window_x, self.window_y))
        dif = self.x+self.offset[0]
        dif1 = self.y+self.offset[1]
        if(dif1<200):
            moveCamera(Directions.up, round(abs(dif1 - 200) / 20,3))
        elif(dif1>300):
            moveCamera(Directions.down, round(abs(dif1 - 300) / 20,3))
        if(dif<420):
            moveCamera(Directions.left,round(abs(dif-420)/20,3))
        elif(dif>480):
            moveCamera(Directions.right,round(abs(dif-479)/20,3))
        if(not self.moving):
            self.anim_frame = IdleAnimation.get()
    def move(self, dir, speed):
        super().move(dir, speed)
        self.lastMovement = dir
        if(dir==Directions.right):
            self.horizontal = False
            self.steps += 1
        elif(dir==Directions.left):
            self.horizontal = True
            self.steps += 1
        if(self.steps>8):
            self.steps = 0
            if(self.isStanding()):
                walkSound.play()
            if(not self.jumping):
                self.anim_frame = PlayerAnimation.get()
    def drop(self):
        if(not self.jumping):
            self.move(Directions.down, int((self.jumps/10)*movement_speed))
        else:
            self.jumps -= 1
            if(self.jumps>0):
                self.move(Directions.up, int((self.jumps/5)*movement_speed))
            else:
                self.jumping = False
                self.jumps = self.jumpPower*15
    def jump(self):
        s = self.isStanding()
        if(s==False): return
        LocalPlayer.presses_left[2] -= 1
        jumpSound.play()
        self.jumping = True
        self.jumps = self.jumpPower*14
        for i in range(3): add(LocalPlayer.getMid()[0], LocalPlayer.y + LocalPlayer.height, s.color, LocalPlayer.offset, 30, 10, win)
    def isStanding(self):
        for entity in EntityPool:
            if(entity==self or not entity.collidable or entity.type=="kill_cube"): continue
            if(entity.will_collide_with(self.rect, Directions.up, 4)):
                return entity
        return False
    def interact(self):
        for entity in EntityPool:
            if(getDistance(entity.x,entity.y,self.getMid()[0],self.getMid()[1])<64):
                if (entity.type == "portal"):
                    entity.enter()
                    break
                elif (entity.type == "checkpoint"):
                    self.currentCheckpoint = entity
                    self.checkpointPressesLeft = subtract(self.presses_left,[0,0,0])
                    checkpointSound.play()
                    sendNotification("Checkpoint erreicht!")
                    break
                elif (entity.type == "final"):
                    entity.pickUp()
                    break
    def kill(self):
        if(self.currentCheckpoint is not None):
            self.x = self.currentCheckpoint.x
            self.y = self.currentCheckpoint.y-self.height-20
            self.presses_left = subtract(self.checkpointPressesLeft, [0,0,0])

class Final(SpriteObject):
    def __init__(self, posx, posy):
        super().__init__(posx, posy-px+2, [255,255,255], "images/blocks/stone.png", px*2, px*2, False, "final")
        self.up = False
        self.count = 0
    def draw(self):
        self.image = FlagAnimation.get()
        super().draw()
    def pickUp(self):
        for i in range(10): add(LocalPlayer.getMid()[0], LocalPlayer.getMid()[1], [200,200,200], LocalPlayer.offset, 30, 50, win)
        del EntityPool[EntityPool.index(self)]
        nextmap()

class Portal(SpriteObject):
    def __init__(self, posx, posy, img, otherPortal):
        super().__init__(posx, posy, [20,20,20], img, px, px, False, "portal")
        self.other_portal = otherPortal
    def enter(self):
        LocalPlayer.x = self.other_portal.x - LocalPlayer.width/2
        LocalPlayer.y = self.other_portal.y - LocalPlayer.height
        portalSound.play()

class Alert:
    def __init__(self, text):
        self.time_left = 300
        self.x = random.randint(50,800)
        self.y = -10
        self.offset = random.randint(20,40)
        self.start_offset = self.offset
        self.text = text
        self.font = pygame.font.Font("fonts/I-pixel-u.ttf", 20)
    def count(self):
        if(self.time_left>0):
            self.time_left -= 1
            if(self.offset>-self.start_offset):
                self.offset-=0.25
            self.y+=self.offset/50
            drawText(self.text,self.x,self.y,[200,200,200],self.font)
        else:
            del Timeouts[Timeouts.index(self)]

def getDistance(x0, y0, x1, y1):
    return abs(math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2))


def pointIsCollidedWithEntity(x,y):
    for entity in EntityPool:
        if(entity.rect.collidepoint(x,y)):
            return entity
    return False

def load_map(path):
    portals = [["abc",()]]
    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    for i in range(len(data)):
        for n in range(len(data[i])):
            e = None
            if (data[i][n] == "G"):
                e = SpriteObject(n * px, i * px, [200,200,200], "images/blocks/stone.png", px, px, True, "object")
            elif (data[i][n] == "M"):
                e = SpriteObject(n * px, i * px, [180,180,210], "images/blocks/moveable_stone.png", px, px, True, "moveable")
            elif (data[i][n] == "K"):
                e = SpriteObject(n * px, i * px, [100,20,20], "images/blocks/kill_cube.png", px, px, True, "kill_cube")
            elif (data[i][n] == "?"):
                e = SpriteObject(n * px-px, i * px + px, [45,53,71], "images/blocks/checkpoint.png", px, px, False, "checkpoint")
                addCP(win, e.x+int(px/2), e.y+int(px/2), [200, 200, 200], e.offset, 50)
                addCP(win, e.x + int(px / 2), e.y + int(px / 2), [200, 200, 200], e.offset, 50)
            elif (data[i][n] == "!"):
                e = Final(n * px, i * px)
            elif (data[i][n] != " "):
                for ps in portals:
                    if(ps[0].lower()==data[i][n]):
                        p1 = Portal(ps[1][0], ps[1][1],"images/blocks/portal1.png", None)
                        p2 = Portal(n * px, i * px,"images/blocks/portal2.png", None)
                        p2.other_portal = p1
                        p1.other_portal = p2
                        EntityPool.append(p1)
                        EntityPool.append(p2)
                        break
                    else:
                        try:
                            portals.index([data[i][n], (n * px, i * px)])
                        except: portals.append([data[i][n], (n * px, i * px)])
            if(e is not None):
                EntityPool.append(e)

def nextmap():
    global current_map
    global EntityPool
    for entity in EntityPool:
        if(entity!=LocalPlayer): del EntityPool[EntityPool.index(entity)]
    EntityPool = []
    EntityPool.append(LocalPlayer)
    LocalPlayer.offset = [w/3, h/3]
    current_map+=1
    LocalPlayer.presses_left = map_jumps[current_map]
    load_map(maps[current_map])
    LocalPlayer.x, LocalPlayer.y = 30, 40

def moveCamera(dir, speed):
    d = None
    if (dir == Directions.right):
        d = [0, -speed]
    elif (dir == Directions.left):
        d = [0, speed]
    elif (dir == Directions.up):
        d = [1, speed]
    elif (dir == Directions.down):
        d = [1, -speed]
    for entity in EntityPool:
        entity.offset[d[0]] += d[1]

def drawText(text,x,y,color,font):
    win.blit(font.render(text, True, color), [x,y])
def sendNotification(text):
    Timeouts.append(Alert(text))

def render_fps():
    fps = round(clock.get_fps()) + 1
    win.blit(textFont.render(str(fps), True, (round(255/fps), 200, 200)), [10, 10])

def render_keys(keylist):
    ksize = 50
    if (keylist[pygame.K_a]): win.blit(pygame.transform.smoothscale(keys[3], (ksize, ksize)), (15,15*4+50))
    else: win.blit(pygame.transform.smoothscale(keys[0], (ksize, ksize)), (15,15*4+50))
    if (keylist[pygame.K_d]): win.blit(pygame.transform.smoothscale(keys[4], (ksize, ksize)), (15*7, 15*4+50))
    else: win.blit(pygame.transform.smoothscale(keys[1], (ksize, ksize)), (15*7, 15*4+50))
    if (keylist[pygame.K_w]): win.blit(pygame.transform.smoothscale(keys[5], (ksize, ksize)), (15*4, 15+50))
    else: win.blit(pygame.transform.smoothscale(keys[2], (ksize, ksize)), (15*4, 15+50))
    drawText(str(LocalPlayer.presses_left[0]), 17,15*4+25, [200, 200, 200], textFont)
    drawText(str(LocalPlayer.presses_left[1]), 17*7, 15*4+25, [200, 200, 200], textFont)
    drawText(str(LocalPlayer.presses_left[2]), 17*4, 15+25, [200, 200, 200], textFont)
load_map("map1.txt")
FlagAnimation = Animation(["images/flag/flag-1.png","images/flag/flag-2.png","images/flag/flag-3.png","images/flag/flag-4.png","images/flag/flag-5.png"],30)
PlayerAnimation = Animation(["images/player/walk-1.png","images/player/walk-2.png","images/player/walk-3.png","images/player/walk-4.png"],0)
IdleAnimation = Animation(["images/player/idle/0.png","images/player/idle/1.png","images/player/idle/2.png","images/player/idle/3.png","images/player/idle/4.png","images/player/idle/5.png"],20)
LocalPlayer = Player(30, 40, [212, 169, 0], 28, 28)

EntityPool.append(LocalPlayer)

while run:
    win.fill((200, 210, 220))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and LocalPlayer.presses_left[2]>0:
                LocalPlayer.jump()
            elif event.key == pygame.K_e:
                LocalPlayer.interact()
            elif event.key == pygame.K_BACKSPACE:
                LocalPlayer.kill()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a and LocalPlayer.presses_left[0]>0:
                LocalPlayer.presses_left[0] -= 1
            elif event.key == pygame.K_d  and LocalPlayer.presses_left[1]>0:
                LocalPlayer.presses_left[1] -= 1
    k = pygame.key.get_pressed()
    if k[pygame.K_a] and LocalPlayer.presses_left[0]>0:
        LocalPlayer.move(Directions.left, LocalPlayer.speed)
        LocalPlayer.moving = True

    elif k[pygame.K_d] and LocalPlayer.presses_left[1]>0:
        LocalPlayer.move(Directions.right, LocalPlayer.speed)
        LocalPlayer.moving = True
    else:
        LocalPlayer.moving = False
    LocalPlayer.drop()
    for particle in particles:
        particle.show()
    for entity in EntityPool:
        entity.draw()
        if(entity==LocalPlayer): continue
        if(LocalPlayer.is_collided_with(entity.rect) and entity.collidable):
            LocalPlayer.move(od[LocalPlayer.lastMovement],3)
    win.blit(pygame.transform.smoothscale(background, (w,h)), (0,0))
    for timer in Timeouts:
        timer.count()
    render_fps()
    render_keys(k)
    clock.tick(fps)
    pygame.display.update()
pygame.quit()