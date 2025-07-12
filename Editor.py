#inputs and disp
import pygame, sys 
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings2 import *
import math
import settings

class Editor:
    
    def __init__(self):
        # main setup 
        self.display_surface = pygame.display.get_surface()

        # navigation
        self.origin = vector()
        self.origin.x = WINDOW_WIDTH/2
        self.origin.y = WINDOW_HEIGHT/2 + (WINDOW_HEIGHT/4)
        self.pan_active = False
        self.pan_offset = vector()
        self.tile = settings.TILE_SIZE
        self.time = 0
        # self.lineON1 = False
        self.lineON1 = True
        # self.lineON2 = False
        self.lineON2 = True
        self.position = 0

        # support lines 
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(100)
    # input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)

    def pan_input(self, event):
        # middle mouse button pressed / released 
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin

        if not mouse_buttons()[0]:
            self.pan_active = False

        # mouse wheel 
        if event.type == pygame.MOUSEWHEEL:
            self.tile = settings.TILE_SIZE
            
            multi = settings.TILE_SIZE // 20
            
            
            if self.tile > 11 and (event.y > 0):
                self.tile += (multi * (event.y))
            else:
                self.tile += (multi * (event.y))
                
            settings.TILE_SIZE = self.tile
        
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE:
                settings.PAUSED = not settings.PAUSED
                
            if event.key == pygame.K_r:
                self.origin.x = WINDOW_WIDTH/2
                self.origin.y = WINDOW_HEIGHT/2 + (WINDOW_HEIGHT/4)
                self.position = 0
            
            if event.key == pygame.K_t:
                settings.TILE_SIZE = 64
                
            if event.key == pygame.K_y:
                self.lineON1 = not self.lineON1
            
            if event.key == pygame.K_u:
                self.lineON2 = not self.lineON2
                
            
            
                
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        
        
            
            


        # panning update
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset
    
    def drawBG(self):
        self.theme_surface = pygame.surface((WINDOW_WIDTH, WINDOW_HEIGHT)) # type: ignore
        self.theme_surface.fill(color = (10,10,20), rect=None, special_flags=0)

    # drawing 
    def draw_tile_lines(self):
        
        multi = int(max(settings.TILE_SIZE / 200 , 1))
        
        cols = WINDOW_WIDTH  // (settings.TILE_SIZE // multi) 
        rows = WINDOW_HEIGHT // (settings.TILE_SIZE // multi)

        origin_offset = vector (
            x = self.origin.x - int(self.origin.x / (settings.TILE_SIZE // multi)) * (settings.TILE_SIZE // multi),
            y = self.origin.y - int(self.origin.y / (settings.TILE_SIZE // multi)) * (settings.TILE_SIZE // multi)
        )

        self.support_line_surf.fill('green')

        for col in range(cols + 1):
            x = origin_offset.x + col * (settings.TILE_SIZE // multi)
            if self.lineON2:
                for i in range (1,5):
                    pygame.draw.line(self.support_line_surf,"grey", (x - (i * (settings.TILE_SIZE/5)),0), 
                                                                    (x - (i * (settings.TILE_SIZE/5)),WINDOW_HEIGHT), width = 1)
            if self.lineON1:
                pygame.draw.line(self.support_line_surf,"white", (x,0), (x,WINDOW_HEIGHT), width = 2)
            
        for row in range(rows + 1):
            y = origin_offset.y + row * (settings.TILE_SIZE // multi)
            if self.lineON2:
                for j in range(1,5):
                    pygame.draw.line(self.support_line_surf,"grey", (0 , y - (j * (settings.TILE_SIZE/5))), 
                                                                    (WINDOW_WIDTH , y - (j * (settings.TILE_SIZE/5))), width = 1)
            
            if self.lineON1:
                pygame.draw.line(self.support_line_surf,"white", (0,y), (WINDOW_WIDTH,y), width = 2)
            
        pygame.draw.line(self.support_line_surf, "white", (self.origin.x,0), (self.origin.x,WINDOW_HEIGHT), width = 3)
        pygame.draw.line(self.support_line_surf, "white", (0,self.origin.y), (WINDOW_WIDTH,self.origin.y) , width = 3)
        
        self.display_surface.blit(self.support_line_surf,(0,0))
        self.display_surface.blit(self.support_line_surf,(0,0))
        
    def run(self, dt):
        
        
        keys = pygame.key.get_pressed()
        
        if pygame.key.get_pressed():
            if keys[pygame.K_LEFT]:
                self.time -= math.pi / 60
            
            if keys[pygame.K_RIGHT]:
                self.time += math.pi / 60
                
            if keys[pygame.K_UP]:
                settings.TILE_SIZE += 1 * int(settings.TILE_SIZE / 64)
                
            if keys[pygame.K_UP]:
                settings.TILE_SIZE -= 1 * int(settings.TILE_SIZE / 64)
            
            if keys[pygame.K_a]:
                self.position -= 2/self.Resolution
            
            if keys[pygame.K_d]:
                self.position += 2/self.Resolution
        
        if not settings.PAUSED:
            self.time += math.pi / 60
        
        if self.tile < 11:
            self.tile = 11
        
        self.event_loop()

        # drawing
        self.display_surface.fill((10,10,20))
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, 'red' , self.origin, 5)
        
        # pygame.draw.circle(self.display_surface, 'blue' , (self.origin.x + settings.TILE_SIZE,self.origin.y + settings.TILE_SIZE), 5)
        # pygame.draw.circle(self.display_surface, 'blue' , (self.origin.x + settings.TILE_SIZE,self.origin.y - settings.TILE_SIZE), 5)
        # pygame.draw.circle(self.display_surface, 'blue' , (self.origin.x - settings.TILE_SIZE,self.origin.y + settings.TILE_SIZE), 5)
        # pygame.draw.circle(self.display_surface, 'blue' , (self.origin.x - settings.TILE_SIZE,self.origin.y - settings.TILE_SIZE), 5)
        # pygame.draw.circle(self.display_surface, 'blue' , (self.origin.x ,self.origin.y - settings.TILE_SIZE), 5)
        # pygame.draw.circle(self.display_surface, 'blue' , (self.origin.x ,self.origin.y + settings.TILE_SIZE), 5)
        
        colorincr = 0
        flipflop = True
        
        for i in range(-314,314):
           
            
            self.Resolution = 50
            self.speed = 0.2
            
            X = (i/self.Resolution)
            X_P = ((i + 1)/self.Resolution)
            
            
        
            a = (( X ** 2 )/ 4)
            
            def funcky (X_in):
                return math.sqrt(abs(((( X_in** 2) / 4) * 9) - (20 * 9)))
            
            def circle(X_in, radius = 1):
                Y_2 = abs(((X_in ** 2) - (radius ** 2)))
                Y_1P = math.sqrt(Y_2)
                Y_1N = -Y_1P
                return Y_1P , Y_1N
            
            def tan_func(X_in , amp = 1, width = 1 , motion = 0):
                return (amp * math.tan( (X_in / width) - (self.speed * motion * self.time) ))
                
            tfunc1 = ( tan_func(X , motion = 0) * settings.TILE_SIZE )
            tfunc1p = ( tan_func(X_P , motion = 0) * settings.TILE_SIZE )
            tfunc2 = ( tan_func(X_P , width = 1.2,  amp = 2 , motion= 2) * settings.TILE_SIZE)
            
            
            
            def H(X_in):
                return X_in ** 2
            
            def cos_func(X_in , amp = 1, width = 1 , motion = 0):
                return amp * math.cos( (X_in / width) - (self.speed * motion * self.time))
            
            
            def lerper(X_in):
                return X_in * X_in * (3 - (2*X_in))
            
            lerpfunc = (lerper(X)  * settings.TILE_SIZE)
            lerpfuncp = (lerper(X_P)  * settings.TILE_SIZE)
            leprfuncshow = (lerper(self.position) * settings.TILE_SIZE)
            
            
            def sine_func(X_in , amp = 1, width = 1 , motion = 0):
                return amp * math.sin( (X_in / width) - (self.speed * motion * self.time))
            
            func1  = (sine_func(X,motion=1) * settings.TILE_SIZE)
            func1p = (sine_func(X_P,motion=1) * settings.TILE_SIZE)
            func2  = (sine_func(X_P , width = 1.2,  amp = 2 , motion= 2) * settings.TILE_SIZE)
            
            # self.xcol = "green"
            def get_difference(params1,params2):
                return sine_func(params2[0] ,width = params2[1],amp = params2[2],motion = params2[3]) - sine_func(params1[0],width = params1[1],amp = params1[2],motion = params1[3])
            
            self.xcol = "green"
            
            
            # if i % 3 == 0:
            #     self.xcol = "red"
            # elif i % 3 != 0 and i % 2 == 0:
            #     self.xcol = "green"
            # else:
            #     self.xcol = "blue"
            
            if func1 > func2:
            
                self.xcol = "dark " + self.xcol
            else:
                
                pass
            
            b = X
            c = math.sin(X - self.time)
            d = math.e ** X
            e = math.sin(0 - self.time)
            f = math.cos(0 - self.time)
            g = 5 * (X ** 2) + 2
            
            # pygame.draw.circle(self.display_surface, 'blue', ((self.origin.x + ( X * settings.TILE_SIZE )),(self.origin.y - (a * settings.TILE_SIZE))), 3)
            # pygame.draw.circle(self.display_surface, 'red', ((self.origin.x + ( X * settings.TILE_SIZE )),(self.origin.y - (b * settings.TILE_SIZE))), 1)
            # pygame.draw.circle(self.display_surface, 'green', ((self.origin.x + ( X * settings.TILE_SIZE )),(self.origin.y - (c * settings.TILE_SIZE))), 3)
            
            
            # pygame.draw.line(self.display_surface, "dark green",  ((self.origin.x + (X * settings.TILE_SIZE)),(self.origin.y - (H(X) * settings.TILE_SIZE))),
            #                                                     ((self.origin.x + (X_P * settings.TILE_SIZE)),(self.origin.y - (H(X_P) * settings.TILE_SIZE))), 3 )
            
            pygame.draw.line(self.display_surface, self.xcol ,  ((self.origin.x + (X * settings.TILE_SIZE)),(self.origin.y - func1)),
                                                                ((self.origin.x + (X_P * settings.TILE_SIZE)),(self.origin.y - func2)), 3 )
            
            # pygame.draw.line(self.display_surface, "blue" ,  ((self.origin.x + (X * settings.TILE_SIZE)),(self.origin.y - tfunc1)),
            #                                                     ((self.origin.x + (X_P * settings.TILE_SIZE)),(self.origin.y - tfunc1p)), 3 )
            
            # pygame.draw.line(self.display_surface, "blue" ,  ((self.origin.x + (X * settings.TILE_SIZE)),(self.origin.y - funcky (X)) * settings.TILE_SIZE),
            #                                                     ((self.origin.x + (X_P * settings.TILE_SIZE)),(self.origin.y - funcky (X_P)) * settings.TILE_SIZE), 3 )
            
            # pygame.draw.line(self.display_surface, "blue" ,  ((self.origin.x + (X * settings.TILE_SIZE)),(self.origin.y - lerpfunc)),
            #                                                     ((self.origin.x + (X_P * settings.TILE_SIZE)),(self.origin.y - lerpfuncp)), 3 )
            
            # pygame.draw.circle(self.display_surface, 'orange', ((self.origin.x + ( self.position * settings.TILE_SIZE )),(self.origin.y - leprfuncshow)), 6)
            
            # for i in range(2):            
            #     pygame.draw.line(self.display_surface, "blue" ,  ((self.origin.x + (X * settings.TILE_SIZE)),(self.origin.y - circle(X)[i])),
            #                                                     ((self.origin.x + (X_P * settings.TILE_SIZE)),(self.origin.y - circle(X_P)[i])), 3 )

            
            
            # pygame.draw.circle(self.display_surface, 'dark red', ((self.origin.x + ( X * settings.TILE_SIZE )),(self.origin.y - (d * settings.TILE_SIZE))), 1)
            # pygame.draw.circle(self.display_surface, 'blue', ((self.origin.x + ( 0 * settings.TILE_SIZE )),(self.origin.y - (e * settings.TILE_SIZE))), 4)
            # pygame.draw.circle(self.display_surface, 'green', ((self.origin.x + ( f * settings.TILE_SIZE )),(self.origin.y - (0 * settings.TILE_SIZE))), 4)
            # pygame.draw.circle(self.display_surface, 'orange', ((self.origin.x + ( X * settings.TILE_SIZE )),(self.origin.y - (g * settings.TILE_SIZE))), 4)