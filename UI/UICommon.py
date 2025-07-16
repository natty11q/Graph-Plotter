from Maths.Maths import *


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
        ...

    @staticmethod
    def AddMousePosEvent(x : float, y : float) -> None:
        ...
    
    @staticmethod
    def AddMouseButtonEvent(key : int, down : bool) -> None:
        ...
    
    @staticmethod
    def AddMouseWheelEvent(wheel_x : float, wheel_y : float) -> None:
        ...
    
    
    @staticmethod
    def AddFocusEvent(focused : bool) -> None:
        ...
    
    @staticmethod
    def ClearEventsQueue() -> None:
        ...
    
    @staticmethod
    def ClearInputKeys() -> None:
        ...
    
    @staticmethod
    def ClearInputMouse() -> None:
        ...


    MousePos    : Vec2
    MouseDown   : list
    MouseDelta  : Vec2

    MouseWheel  : float


    KeyCtrl     : bool
    KeyShift    : bool
    KeySuper    : bool
    KeyAlt      : bool


    MousePosPrev        : Vec2
    MouseClickedPos     : list[Vec2]    # [5]
    MouseClickedTime    : list[float]   # [5]
    MouseClicked        : list[bool]    # [5]
    MouseDoubleClicked  : list[bool]    # [5]

    MouseClickedCount       : list[int]     # [5]
    MouseClickedLastCount   : list[int]     # [5]

    MouseReleased       : list[bool]    # [5]
    MouseReleasedTime   : list[bool]    # [5]


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
