from Maths.Maths import *
from Event.EventHandler import *

import Utility.Temporal as Temporal
import UI.Keys as Keys

def IsMouseButtonDown(button : int) -> bool:
    ... 

def IsMouseButtonClicked(button : int) -> bool:
    ...

def IsMouseButtonReleased(button : int) -> bool:
    ...

def IsMouseDoubleClicked(button : int) -> bool:
    ...


def IsMouseHoveringRect(rectMin : Vec2, rectMax : Vec2, clip : bool) -> bool:
    ...

def GetClipboardText() -> str:
    ...

def SetClipboardText(text : str) -> None:
    ...



def LoadIniSettingsFromDisk(iniFilename : str) -> None:
    ...

def LoadIniSettingsFromMemory(iniData : str) -> None:
    ...

def LoadIniSettingsToDisk(iniFilename : str) -> None:
    ...

def LoadIniSettingsToMemory() -> str:
    ...

# class Global:
#     Time : float = 0.0
#     Deltatime : float = 0.0




class IO:

    Deltatime       : float
    IniSavingRate   : float
    
    IniFilename : str


    MouseDoubleClickTime    : float
    MouseDoubleClickMaxDist : float
    MouseDragTheshold       : float
    KeyRepeatDelay  : float
    KeyRepeatRate   : float

    BackendPlatformName : str
    BackendRendererName : str

    @staticmethod
    def AddKeyEvent(key : int, down : bool) -> None:
        e : Event
        if down:
            e = KeyDownEvent()
            e.keycode = key
        else:
            e = KeyUpEvent()
            e.keycode = key
        sendEvent(e)

    @staticmethod
    def AddMousePosEvent(x : float, y : float) -> None:
        e = MouseMovedEvent()
        e.x = x
        e.y = y
        sendEvent(e)
    
    @staticmethod
    def AddMouseButtonEvent(key : int, x : float, y : float, down : bool) -> None:
        e = MouseButtonDownEvent()
        e.button = key

        e.x = x
        e.y = y

        sendEvent(e)
    
    @staticmethod
    def AddMouseWheelEvent(wheel_x : float, wheel_y : float) -> None:
        e = MouseScrollEvent()

        e.x = wheel_x
        e.y = wheel_y
    
    @staticmethod
    def AddFocusEvent(focused : bool) -> None:
        e = WindowFocusGainedEvent()
    
    @staticmethod
    def ClearEventsQueue() -> None:
        ...
    
    @staticmethod
    def ClearInputKeys() -> None:
        ...
    
    @staticmethod
    def ClearInputMouse() -> None:
        ...
    

    @staticmethod
    def HandleEvents(e : Event) -> None:
        match e.type:
            case GP_EventType.MouseMoved:
                IO.MousePosPrev.x   = IO.MousePos.x
                IO.MousePosPrev.y   = IO.MousePos.y

                IO.MousePos.x       = e.x
                IO.MousePos.y       = e.y

            case GP_EventType.MouseButtonDown:
                IO.MouseDown[e.button]      = True
                IO.MouseClickedCount[e.button] += 1

            case GP_EventType.MouseButtonUp:
                IO.MouseDown[e.button]      = False
    

    @staticmethod
    def UpdateMouse() -> None:

        IO.MouseDelta       = IO.MousePos - IO.MousePosPrev
        for button in range(len(IO.MouseClicked)):

            IO.MouseClicked[button]             = IO.MouseDown[button] and IO.MouseDownDuration[button] < 0.0
            IO.MouseClickedCount[button]        = 0
            IO.MouseReleased[button]            = (not IO.MouseDown[button]) and IO.MouseDownDuration[button] >= 0.0
            IO.MouseDownDurationPrev[button]    = IO.MouseDownDuration[button]
            
            if IO.MouseDown[button]:
                if IO.MouseDownDuration[button] < 0.0:  IO.MouseDownDuration[button] = 0.0
                else:  IO.MouseDownDuration[button] += Temporal.PlotEngineTime.DeltaTime()
            else:
                IO.MouseDownDuration[button] = -1

            if IO.MouseDown[button]:
                isRepeatedClick : bool = False
                if Temporal.PlotEngineTime.Time() - IO.MouseClickedTime[button] < IO.MouseDoubleClickTime:
                    deltaFromClickPos : Vec2 = IO.MousePos - IO.MouseClickedPos[button]
                    if deltaFromClickPos.length_squared() < (IO.MouseDoubleClickMaxDist ** 2):
                        isRepeatedClick = True

                if isRepeatedClick:
                    IO.MouseClickedLastCount[button] += 1
                else:
                    IO.MouseClickedLastCount[button] = 1;

                IO.MouseDoubleClickTime         = Temporal.PlotEngineTime.Time()
                IO.MouseClickedPos[button]      = IO.MousePos
                IO.MouseClickedCount[button]    = IO.MouseClickedLastCount[button]
                IO.MouseDragMaxDistanceAbs[button]  = Vec2()
                IO.MouseDragMaxDistanceSqr[button]  = 0.0
            
            elif IO.MouseDown[button]:
                deltaFromClickPos = IO.MousePos - IO.MouseClickedPos[button]
                IO.MouseDragMaxDistanceSqr[button] = max(IO.MouseDragMaxDistanceSqr[button],deltaFromClickPos.length_squared())
                IO.MouseDragMaxDistanceAbs[button].x = max(IO.MouseDragMaxDistanceAbs[button].x,abs(deltaFromClickPos.x))
                IO.MouseDragMaxDistanceAbs[button].y = max(IO.MouseDragMaxDistanceAbs[button].y,abs(deltaFromClickPos.y))


            IO.MouseDoubleClicked[button] = (IO.MouseClickedCount[button] == 2)

    @classmethod
    def Init(cls) -> None:
        Keys.Keys.Init()
        AddEventListener(cls.HandleEvents)

    @staticmethod
    def Update() -> None:
        IO.UpdateMouse()
        Keys.Keys.Update()

        




    MousePos        : Vec2  = Vec2()
    MousePosPrev    : Vec2  = Vec2()

    MouseDown       : list  = [False, False, False, False, False]  # [5]
    MouseDownDuration       : list[float] = [0.0,0.0,0.0,0.0,0.0]
    MouseDownDurationPrev   : list[float] = [0.0,0.0,0.0,0.0,0.0]
    MouseDelta      : Vec2  = Vec2()

    MouseWheel  : float     = 0

    MouseDoubleClickTime : float = 0.3

    KeyCtrl     : bool = False
    KeyShift    : bool = False
    KeySuper    : bool = False
    KeyAlt      : bool = False

    KeyMap : dict [str , int] = Keys.KEY_MAP

    MousePosPrev        : Vec2 = Vec2()
    
    MouseClicked        : list[bool]    = [False, False, False, False, False]  # [5]
    MouseClickedPrev    : list[bool]    = [False, False, False, False, False]  # [5]
    MouseClickedPos     : list[Vec2]    = [Vec2(),Vec2(),Vec2(),Vec2(),Vec2()] # [5]
    MouseClickedTime    : list[float]   = [False, False, False, False, False]  # [5]

    MouseDoubleClicked  : list[bool]    = [False, False, False, False, False]  # [5]

    MouseClickedCount       : list[int] = [0,0,0,0,0]  # [5]
    MouseClickedLastCount   : list[int] = [0,0,0,0,0]  # [5]

    MouseDragMaxDistanceAbs : list[Vec2] = [Vec2(),Vec2(),Vec2(),Vec2(),Vec2()]
    MouseDragMaxDistanceSqr : list[float] = [0,0,0,0,0]

    
    MouseReleased       : list[bool]    = [False, False, False, False, False]  # [5]
    MouseReleasedTime   : list[bool]    = [False, False, False, False, False]  # [5]



class GuiContext:
    Initialised     : bool = False
    DebugEnabled    : bool = False


    Time            : float = 0.0
    FrameCount      : int   = 0

    WindowsActiveCount      : int = 0
    CurrentWindow = None # type not defined yet
    HoveredWindow = None # type not defined yet

    ActiveId        : int = 0
    ActiveIdIsAlive : int = 0
    ActiveIdTimer   : int = 0

    ActiveIdIsJustActivated : bool = False
    ActiveIdAllowOverlap    : bool = False

    ActiveIdWindow  = None # type not defined yet

    LastActiveId            : int   = 0
    LastActiveIdTimer       : float = 0.0



    LogEnabled : bool = False
    LogFlags   : int  = 0

