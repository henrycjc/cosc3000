#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from OpenGL.GLUT import *
import math, time

class Main():

    VIDEO_FLAGS = OPENGL|DOUBLEBUF
    goCardX = 0
    goCardY = 0
    machineX = 0
    machineY = -8
    pause = False
    sourceList = []
    showAxes = False
    lastUpdateTime = time.time()
    sim = False
    connected = False
    addConnection = True
    textures = []

    def __init__(self):

        pygame.init()
        pygame.display.set_mode((1024,768), self.VIDEO_FLAGS)
        pygame.display.set_caption("NFC Simulation")

        self.resize((1024,768))

        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        
        self.demandedFps=60.0
        self.done=False

        self.gocardX = -5.0
        self.gocardY = 0.0
        xOffset = 0.1
        self.new_point(WavePoint([-xOffset, 0, 0]))
        clock = pygame.time.Clock()
        while True:
            event = pygame.event.poll()
            if event.type == QUIT or self.done:
                pygame.quit() 
                break
            self.input()
            self.draw()
            
            pygame.display.flip()
            clock.tick(self.demandedFps)

    def resize(self, (width, height)):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-6.0, 6.0, -15.0, 15.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if not self.sim:
             self.draw_gocard()
        else:
             self.draw_gocard_sim()

        if not self.sim:
            self.draw_machine()
        else:
            self.draw_machine_sim()
        self.draw_waves()
        self.update_waves()
        if self.connected:
            if self.addConnection:
                #print self.gocardX
                print ("adding new thing now")
                xOffset = self.gocardX
                yOffset = self.gocardY
                self.new_point(WavePoint([xOffset, yOffset, 0], 2))
                #print self.sourceList
                self.addConnection = False
        self.tidy()
               
    def draw_gocard(self):
        if not self.connected:
            textureSurface = pygame.image.load("textures/card_off.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()
            
            glTranslatef(self.gocardX, self.gocardY, 0.0)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBindTexture(GL_TEXTURE_2D, texID)
            

            glBegin(GL_QUADS)
            glTexCoord2f(0.0,1.0)
            glVertex2f(-1.0, 4.0)
            glTexCoord2f(1.0,1.0)
            glVertex2f(1.0, 4.0)
            glTexCoord2f(1.0,0.0)
            glVertex2f(1.0, -4.0)
            glTexCoord2f(0.0,0.0)
            glVertex2f(-1.0, -4.0)
            glEnd()
            
            glPopMatrix()
        else:
            textureSurface = pygame.image.load("textures/card_on.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()
            
            glTranslatef(self.gocardX, self.gocardY, 0.0)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBindTexture(GL_TEXTURE_2D, texID)
            

            glBegin(GL_QUADS)
            glTexCoord2f(0.0,1.0)
            glVertex2f(-1.0, 4.0)
            glTexCoord2f(1.0,1.0)
            glVertex2f(1.0, 4.0)
            glTexCoord2f(1.0,0.0)
            glVertex2f(1.0, -4.0)
            glTexCoord2f(0.0,0.0)
            glVertex2f(-1.0, -4.0)
            glEnd()
            
            glPopMatrix()

    def draw_gocard_sim(self):
        if not self.connected:
            textureSurface = pygame.image.load("textures/cardsim_off.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()
            
            glTranslatef(self.gocardX, self.gocardY, 0.0)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBindTexture(GL_TEXTURE_2D, texID)
            

            glBegin(GL_QUADS)
            glTexCoord2f(0.0,1.0)
            glVertex2f(-1.0, 4.0)
            glTexCoord2f(1.0,1.0)
            glVertex2f(1.0, 4.0)
            glTexCoord2f(1.0,0.0)
            glVertex2f(1.0, -4.0)
            glTexCoord2f(0.0,0.0)
            glVertex2f(-1.0, -4.0)
            glEnd()
            
            glPopMatrix()
        else:
            textureSurface = pygame.image.load("textures/cardsim_on.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()
            
            glTranslatef(self.gocardX, self.gocardY, 0.0)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glBindTexture(GL_TEXTURE_2D, texID)
            

            glBegin(GL_QUADS)
            glTexCoord2f(0.0,1.0)
            glVertex2f(-1.0, 4.0)
            glTexCoord2f(1.0,1.0)
            glVertex2f(1.0, 4.0)
            glTexCoord2f(1.0,0.0)
            glVertex2f(1.0, -4.0)
            glTexCoord2f(0.0,0.0)
            glVertex2f(-1.0, -4.0)
            glEnd()
            
            glPopMatrix()

    def draw_machine(self):
        if not self.connected:
            textureSurface = pygame.image.load("textures/reader_off.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()

            glBindTexture(GL_TEXTURE_2D, texID)
            glBegin(GL_QUADS)

            vx = 2.0
            vy = 6.0

            glTexCoord2f(0.0,1.0)
            glVertex2f(-1*vx, vy)

            glTexCoord2f(1.0,1.0)
            glVertex2f(vx, vy)

            glTexCoord2f(1.0,0.0)
            glVertex2f(vx, -1*vy)

            glTexCoord2f(0.0,0.0)
            glVertex2f(-1*vx, -1*vy)
            glEnd()
            glPopMatrix()
        else:
            textureSurface = pygame.image.load("textures/reader_on.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()

            glBindTexture(GL_TEXTURE_2D, texID)
            glBegin(GL_QUADS)

            vx = 2.0
            vy = 6.0

            glTexCoord2f(0.0,1.0)
            glVertex2f(-1*vx, vy)

            glTexCoord2f(1.0,1.0)
            glVertex2f(vx, vy)

            glTexCoord2f(1.0,0.0)
            glVertex2f(vx, -1*vy)

            glTexCoord2f(0.0,0.0)
            glVertex2f(-1*vx, -1*vy)
            glEnd()
            glPopMatrix()

    def draw_machine_sim(self):
        if not self.connected:
            textureSurface = pygame.image.load("textures/readersim_off.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()

            glBindTexture(GL_TEXTURE_2D, texID)
            glBegin(GL_QUADS)

            vx = 2.0
            vy = 6.0

            glTexCoord2f(0.0,1.0)
            glVertex2f(-1*vx, vy)

            glTexCoord2f(1.0,1.0)
            glVertex2f(vx, vy)

            glTexCoord2f(1.0,0.0)
            glVertex2f(vx, -1*vy)

            glTexCoord2f(0.0,0.0)
            glVertex2f(-1*vx, -1*vy)
            glEnd()
            glPopMatrix()
        else:
            textureSurface = pygame.image.load("textures/readersim_on.jpg")
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
            texID = glGenTextures(1)
            self.textures.append(texID)
            glBindTexture(GL_TEXTURE_2D, texID)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), 
                textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glPushMatrix()

            glBindTexture(GL_TEXTURE_2D, texID)
            glBegin(GL_QUADS)

            vx = 2.0
            vy = 6.0

            glTexCoord2f(0.0,1.0)
            glVertex2f(-1*vx, vy)

            glTexCoord2f(1.0,1.0)
            glVertex2f(vx, vy)

            glTexCoord2f(1.0,0.0)
            glVertex2f(vx, -1*vy)

            glTexCoord2f(0.0,0.0)
            glVertex2f(-1*vx, -1*vy)
            glEnd()
            glPopMatrix()

    def draw_waves(self):
        for x in self.sourceList:
            x.draw_waves()

    def input(self):
        mpb=pygame.mouse.get_pressed() # mouse pressed buttons
        kpb=pygame.key.get_pressed() # keyboard pressed buttons
        msh=pygame.mouse.get_rel() # mouse shift
        #print self.gocardX 
        #print self.gocardY
        if kpb[K_ESCAPE]:
            print ("Exiting")
            self.done=True
            
        if kpb[K_UP]:
            self.gocardY+=0.1
        if kpb[K_DOWN]:
            self.gocardY-=0.1

        if kpb[K_RIGHT]:
            #print self.gocardX
            if self.gocardX >= -3.0:
                self.connected = True
                if len(self.sourceList) == 2:
                    self.addConnection = False
                else:
                    self.addConnection = True
            else:
                self.connected = False
            self.gocardX += 0.1
        if kpb[K_LEFT]:
            if self.gocardX <= -3.0:
                if self.connected:
                    if len(self.sourceList) == 1:
                        pass
                    else:
                        self.sourceList.pop()
                self.connected = False
                print ("Disconnected")
            self.gocardX-=0.1

        if kpb[K_SPACE]:
            self.sim = not self.sim
            print ("Toggling simulation mode")

    def draw_nfc_field(self):
        ## LOGIC
        pass

    def tidy(self):
        #glutSwapBuffers() # Two buffers: draw with one, fill the other, swap 'em
        time.sleep(1.0 / 30.0) # ~30fps 

    def update_waves(self):
        #if self.pause == True:
         #   self.lastUpdateTime = time.time()
          #  return
        # Get time since last call
        t = time.time()
        timePassed = t - self.lastUpdateTime
        self.lastUpdateTime = t
        # Update waves and clear dead ones
        idx = 0
        #print self.sourceList
        while idx < len(self.sourceList):
            self.sourceList[idx].ripple(timePassed)
            if self.sourceList[idx].dead == True:
                self.sourceList.pop(idx)
            else:
                idx += 1 #this was 180, how did it not error? oh beacuse while loop memes

    def draw_vertices(self, vertexList):
        for i in xrange(len(vertexList)):
            glVertex3fv(vertexList[i])
    
    def new_point(self, source):
        #
        self.sourceList.append(source)

class WavePoint():

    prefade = 0
    delay = 0
    length = 2.0
    speed = 2.0
    timeout = 5
    colour = [0, 1, 0]
    dying = False
    dead = False
    alive = 0
    waveList = []

    def __init__(self, origin, ripplesToDraw=-1):
        self.origin = origin
        self.totalRipples = ripplesToDraw
        self.ripplesToDraw = 1
        self.make_wave()

    def make_wave(self):
        self.waveList.append(Wave(gluNewQuadric(), ((self.length / 10) / 2), self.length / 10))

    def draw_waves(self):
        if self.delay > 0:
            return
        glPushMatrix();
        glTranslated(self.origin[0], self.origin[1], self.origin[2]);
        for wave in self.waveList:
            r = self.colour[0] + (wave.radius/self.timeout)
            g = self.colour[1] + (wave.radius/self.timeout)
            b = self.colour[2] + (wave.radius/self.timeout)
            wave.draw_wave([r, g, b])
        glPopMatrix();

    def ripple(self, time):
        numWaves = len(self.waveList)
        if self.delay > 0:
            self.delay -= time
            return
        self.alive += time
        if numWaves > 0:
            for x in self.waveList:
                x.radius += time * self.speed

        moreTime = time + self.waveList[-1].radius / self.speed
        moreTime -= self.length / 20 / self.speed

        while moreTime - (self.length/self.speed) >= 0 and not self.dying:
            if self.ripplesToDraw == self.totalRipples:
                self.dying = True
                break
            self.ripplesToDraw += 1
            self.make_wave()
            alive = moreTime - (self.length / self.speed)
            self.waveList[-1].radius += alive * self.speed
            moreTime = moreTime - (self.length / self.speed)
        self.cleanup()

    def cleanup(self):
        #1000 iterations seems reasonable
        for i in xrange(0, 999):
            if len(self.waveList) > 0:
                pass
            else:
                break
            if self.waveList[0].radius > self.timeout:
                self.kill_wave(0)
            else:
                break
        if len(self.waveList) == 0 and self.dying == True:
            self.destroy()
            self.dead = True

    def kill_wave(self, idx):
        self.waveList[idx].destroy()
        self.waveList.pop(idx)

    def destroy(self):
        for wave in self.waveList:
            self.kill_wave(0)

class Wave(object):
    quad = None
    raidus = None
    width = None
    def __init__(self, quad, radius, width):
        self.quad = quad
        self.radius = radius
        self.width = width
    def draw_wave(self, colour=[255,0,0]):
        glColor3fv(colour)
        gluDisk(self.quad, self.radius-(self.width/9), self.radius+(self.width/9), 200, 2)
    def destroy(self):
        return None

if __name__ == '__main__':
    print """ <- -> v ^ keys control the GoCard \n
    Spacebar toggles between concealed and normal mode \n
    Escape to quit."""
    Main()