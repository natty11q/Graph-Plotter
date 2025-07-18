__PYGAME_ONLY = True


#inputs and disp
import pygame, sys, os
import math
from enum import Enum, auto

from Common import *
from Maths.Maths import *

import GlobalSettings


DEFAULT_ZOOM = 100.0

DEFAULT_BACGROUND_COL  = Vec3(255,255,255)

DEFAULT_MAJOR_RULE_LINE_COL     = Vec3(200,200,200)
DEFAULT_MAJOR_RULE_LINE_OPACITY = 0.8

DEFAULT_MINOR_RULE_LINE_COL     = Vec3(25,25,25)
DEFAULT_MINOR_RULE_LINE_OPACITY = 1.0

DEFAULT_GRAPH_DENSITY   = 5
DEFAULT_CALC_CYCLES_PER_SECOND  = 120

DEFAULT_SCROLL_SPEED    = 1
DEFAULT_ZOOM_SPEED      = 1
DEFAULT_PAN_SPEED       = 1



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
        CalcCyclesPerSecond = DEFAULT_CALC_CYCLES_PER_SECOND # how many times the calculation thread runs per second

        ScrollSpeed     = DEFAULT_SCROLL_SPEED
        PanSpeed        = DEFAULT_PAN_SPEED
        ZoomSpeed       = DEFAULT_ZOOM_SPEED
    
    class TEMPORAL:
        Time : float            = 0.0
        AnimationSpeed : float  = 0.0


class EditorState(Enum):
    Initialisig = 0
    Playing     = 1
    Paused      = auto()
    Quit        = auto()




class Editor:
    def __init__(self):
        self.display_surface : pygame.Surface | None = None # modify in future for more general impl to increase speeds using gpu accel. dont lock to pygame
        if __PYGAME_ONLY:
            self.display_surface = pygame.display.get_surface() # modify in future for more general impl to increase speeds using gpu accel. dont lock to pygame

        self.__originPos    = Vec2()

        self.__panActive    = False
        self.__panOffset    = Vec2()
        self.__currentPanVelocity  = Vec2()
        self.__panDampingMax    = Vec2() # the largest counter vector that can be applied to panning velocity 


        self.__settings : __EDITOR_SETTINGS = __EDITOR_SETTINGS()

        self.Init   : bool  = False
        self.state  : EditorState   = EditorState.Initialisig

    def Initialise(self):

        self.Load()
        self.state  = EditorState.Playing
        self.Init   = True

    def Load(self):
        settingsPath = GlobalSettings.Settings.EditorSettingsPath
        if not settingsPath:    return
        if not os.path.exists(settingsPath):    return
        
        settingsData = {}
        with open(settingsPath, "r") as data:
            settingsData = json.load(data)

            self.__settings.GENERAL.CalcCyclesPerSecond     = settingsData["CALC_CYCLES_PER_SECOND"]
            self.__settings.GENERAL.GraphDensity            = settingsData["GRAPH_DENSITY"]
            self.__settings.GENERAL.PanSpeed                = settingsData["PAN_SPEED"]
            self.__settings.GENERAL.ScrollSpeed             = settingsData["SCROLL_SPEED"]
            self.__settings.GENERAL.ZoomSpeed               = settingsData["ZOOM_SPEED"]

            self.__settings.GRAPHICS.MinorRuleLineCol       = Vec3(*settingsData["MINOR_RULE_LINE_COL"])
            self.__settings.GRAPHICS.MinorRuleLineOpacity   = settingsData["MINOR_RULE_LINE_OPACITY"]

            self.__settings.GRAPHICS.MajorRuleLineCol       = Vec3(*settingsData["MAJOR_RULE_LINE_COL"])
            self.__settings.GRAPHICS.MajorRuleLineOpacity   = settingsData["MAJOR_RULE_LINE_OPACITY"]

            self.__settings.GRAPHICS.BackGroundColour       = Vec3(*settingsData["BACGROUND_COL"])
            self.__settings.GRAPHICS.Zoom                   = settingsData["ZOOM"]
            
            self.__settings.TEMPORAL.AnimationSpeed         = 1.0


    def Save(self):
        settingsPath = GlobalSettings.Settings.EditorSettingsPath
        if not settingsPath:    return
        if not os.path.exists(settingsPath):    return

        
        with open(settingsPath, "r") as data:
            settingsData = json.load(data)

            settingsData["CALC_CYCLES_PER_SECOND"]  = self.__settings.GENERAL.CalcCyclesPerSecond
            settingsData["GRAPH_DENSITY"]           = self.__settings.GENERAL.GraphDensity
            settingsData["PAN_SPEED"]               = self.__settings.GENERAL.PanSpeed
            settingsData["SCROLL_SPEED"]            = self.__settings.GENERAL.ScrollSpeed
            settingsData["ZOOM_SPEED"]              = self.__settings.GENERAL.ZoomSpeed

            settingsData["MINOR_RULE_LINE_COL"]     = list(self.__settings.GRAPHICS.MinorRuleLineCol.get_p())
            settingsData["MINOR_RULE_LINE_OPACITY"] = self.__settings.GRAPHICS.MinorRuleLineOpacity

            settingsData["MAJOR_RULE_LINE_COL"]     = list(self.__settings.GRAPHICS.MajorRuleLineCol.get_p())
            settingsData["MAJOR_RULE_LINE_OPACITY"] = self.__settings.GRAPHICS.MajorRuleLineOpacity

            settingsData["BACGROUND_COL"]           = list(self.__settings.GRAPHICS.BackGroundColour.get_p())
            settingsData["ZOOM"]                    = self.__settings.GRAPHICS.Zoom

            json.dump(settingsData, data, indent=4)
        





    def Pan(self, mouseDelta : Vec2):
        self.__originPos -= mouseDelta





    def Update(self, dt : float):
        ...

    def MathsUpdate(self, ts): # handle calcs on a different thread
        ...

    def Draw(self):

        col : tuple[float, ...] = self.__settings.GRAPHICS.BackGroundColour.get_p()
        self.display_surface.fill(col) # type: ignore