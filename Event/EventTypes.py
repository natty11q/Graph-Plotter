from enum import Enum, auto


# class EventType: # allow for users to make custom event types
#     ...

class GP_EventType(Enum):
    Default = auto()
    KeyDown = auto()
    KeyUp   = auto()
    MouseMoved      = auto()
    MouseButtonDown = auto()
    MouseButtonUp   = auto()
    MouseScroll     = auto()
    WindowResize    = auto()
    WindowMinimised = auto()
    WindowMaximised = auto()
    WindowRestored  = auto()
    WindowFocusLost = auto()
    WindowFocusGained   = auto()
    WindowClosed        = auto()
    WindowRestoredDown  = auto()