import pygame
from pygame.locals import *

from screen import Screen
from cube import Cube

FOV = 60
A = 100
enableVerts = False
enableAA = True

class App(object):
    def __init__(self,size,title="pygame window",icon=None):
        self.running = False
        self.size = size
        self.title = title
        self.icon = icon
        pygame.init()

    def init(self):
        """Commands to be processed before the application starts"""
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.title)
        if self.icon != None:
            self.icon = pygame.image.load(self.icon)
            pygame.display.set_icon(self.icon)
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | DOUBLEBUF)

        self.screen = Screen(self.size, FOV)
        self.cube = Cube(A)
        self.a = self.cube.a
        self.top_left = [self.size[0]/4 - self.a/2, self.size[1]/4 - self.a/2, self.a/2]
        #self.top_left = [self.size[0]/2 - self.a/2, self.size[1]/2 - self.a/2, self.a/2]
        self.centraliser = [self.size[0]/2, self.size[1]/2, 0]
        self.dir = 0
        self.speed = 100

        self.zdir = 0
        self.zspeed = self.a*2

        self.lineFunc = pygame.draw.aaline if enableAA else pygame.draw.line

        # Load fonts
        self.small_font = pygame.font.SysFont("sans-serif",15)
        self.medium_font = pygame.font.SysFont("sans-serif",22)

        return True

    def __loop__(self):
        """Commands processed every frame"""
        clock_factor = (self.clock.get_time()/1000)
        to_move = self.speed*clock_factor
        if self.dir == 0: #going right
            self.top_left[0] += to_move
            if self.top_left[0] >= 3*self.size[0]/4 - self.a/2:
                self.top_left[0] = 3*self.size[0]/4 - self.a/2
                self.dir = 1
        elif self.dir == 1: #going down
            self.top_left[1] += to_move
            if self.top_left[1] >= 3*self.size[1]/4 - self.a/2:
                self.top_left[1] = 3*self.size[1]/4 - self.a/2
                self.dir = 2
        elif self.dir == 2: #going left
            self.top_left[0] -= to_move
            if self.top_left[0] <= self.size[0]/4 - self.a/2:
                self.top_left[0] = self.size[0]/4 - self.a/2
                self.dir = 3
        elif self.dir == 3:
            self.top_left[1] -= to_move
            if self.top_left[1] <= self.size[1]/4 - self.a/2:
                self.top_left[1] = self.size[1]/4 - self.a/2
                self.dir = 0

        to_zmove = self.zspeed*clock_factor
        if self.zdir == 0: # going back
            self.top_left[2] += to_zmove
            if self.top_left[2] >= 10*self.a:
                self.top_left[2] = 10*self.a
                self.zdir = 1
        elif self.zdir == 1: # going forward
            self.top_left[2] -= to_zmove
            if self.top_left[2] <= -self.a*5:
                self.top_left[2] = -self.a*5
                self.zdir = 0

    def __events__(self, event):
        """Event Handling"""
        if event.type == pygame.QUIT:
            self.running = False

    def __render__(self):
        """Rendering"""
        self.display.fill((255,255,255))
        coords = self.top_left[:]
        coords[0] += self.a/2
        coords[1] += self.a/2
        coords[2] += self.a/2
        cube_points = self.screen.transform_coords(self.cube.vert+self.top_left-self.centraliser)+self.centraliser
        flat_points = cube_points[:,:2]

        # draw vertices
        if enableVerts:
            for c in flat_points:
                pygame.draw.circle(self.display, (0,0,0), c.astype(int), 3)

        # draw edges
        for edge in self.cube.edge:
            if cube_points[edge[0], 2] > 0 and cube_points[edge[1], 2] > 0:
                self.lineFunc(self.display, (0,0,0), flat_points[edge[0]], flat_points[edge[1]])

        # draw texts
        fps_text = self.small_font.render(f"FPS: {self.clock.get_fps():.1f}", 1, (0,0,0))
        self.display.blit(fps_text, (0,0))

        fov_text = self.small_font.render(f"FOV: {FOV}   a: {self.a}", 1, (0,0,0))
        self.display.blit(fov_text, (0,10))

        coord_text = self.medium_font.render(f"Position: ({coords[0]:.0f}, {coords[1]:.0f}, {coords[2]:.0f})", 1, (0,0,0))
        self.display.blit(coord_text, (0,20))
        
        pygame.display.flip()

    def __cleanup__(self,e=None):
        """Commands to be processed when quiiting"""
        pygame.quit()
        if e != None:
            raise e

    def start(self,fps_limit=0):
        """Start the application"""
        self.fps_limit = fps_limit #This way fps can be dynamically adjusted
        ex = None
        try:
            self.running = self.init()
        except Exception as e:
            self.running = False
            ex = e
        
        while self.running == True:
            try:
                for event in pygame.event.get():
                    self.__events__(event)

                self.__loop__()
                self.__render__()
                self.clock.tick(self.fps_limit)
            except Exception as e:
                self.running = False
                ex = e
    

        self.__cleanup__(ex)
