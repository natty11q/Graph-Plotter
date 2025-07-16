__PYHAME_ONLY = True


#inputs and disp
import pygame, sys, os
import math
from enum import Enum, auto

from Common import *
from Maths.Maths import *


DEFAULT_ZOOM = 100.0

DEFAULT_BACGROUND_COL  = Vec3(255,255,255)

DEFAULT_MAJOR_RULE_LINE_COL     = Vec3(200,200,200)
DEFAULT_MAJOR_RULE_LINE_OPACITY = 0.8

DEFAULT_MINOR_RULE_LINE_COL     = Vec3(25,25,25)
DEFAULT_MINOR_RULE_LINE_OPACITY = 1.0

DEFAULT_GRAPH_DENSITY   = 5
CALC_CYCLES_PER_SECOND  = 120



class __EDITOR_SETTINGS:
    class GRAPHICS:
        Zoom : float            = DEFAULT_ZOOM
        BackGroundColour : Vec3 = DEFAULT_BACGROUND_COL
        
        MajorRuleLineCol     : Vec3     = DEFAULT_MAJOR_RULE_LINE_COL
        MajorRuleLineOpacity : float    = DEFAULT_MAJOR_RULE_LINE_OPACITY


        MinorRuleLineCol     : Vec3     = DEFAULT_MINOR_RULE_LINE_COL
        MinorRuleLineOpacity : float    = DEFAULT_MINOR_RULE_LINE_OPACITY

    class GENERAL:
        GraphDensity        = DEFAULT_GRAPH_DENSITY # points per major rule
        CalcCyclesPerSecond = CALC_CYCLES_PER_SECOND # how many times the calculation thread runs per second
    
    class TEMPORAL:
        Time : float            = 0.0
        AnimationSpeed : float  = 0.0


class EditorState(Enum):
    Playing = 0
    Paused  = auto()




class Editor:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() # modify in future for more general impl to increase speeds using gpu accel. dont lock to pygame

        self.__settingsFilePathCache : str | None = None

        self.__originPos  = Vec2()
        self.__panActive  = False
        self.__panOffset  = Vec2()


        self.__settings : __EDITOR_SETTINGS = __EDITOR_SETTINGS()


    def Load(self, settingsPath : str | None = None):
        if not settingsPath:
            return
        
        if not os.path.exists(settingsPath):
            return
        

        settingsData = {}
                
        with open(settingsPath, "r") as data:
            settingsData = json.load(data)
        

        self.__settingsFilePathCache = settingsPath



    def Update(self, dt : float):
        ...

    def MathsUpdate(self, ts): # handle calcs on a different thread
        ...

    def Draw(self):

        col : tuple[float, ...] = self.__settings.GRAPHICS.BackGroundColour.get_p()
        self.display_surface.fill(col) # type: ignore