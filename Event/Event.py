from typing import Callable

from Event.EventTypes import *

class Event:
    def __init__(self, name : str):
        self._m_name : str = name
        self._m_handled : bool = False

        self.x : float
        self.y : float

        self.button : int

        self.width : int
        self.height : int

        self.keycode : int

        self.type : GP_EventType = GP_EventType.Default

    def GetName(self):
        return self._m_name
    
    def GetType(self):
        return self.type
    
    def Handled(self):
        return self._m_handled


class EventDispatcher:
   

    def __init__(self):
        self.__m_EventListeners : list[Callable[[Event], None]] = []
        self.__m_NextListenerID = 0
    
    def AddEventListener(self, listener : Callable[[Event], None]) -> int:
        self.__m_EventListeners.append(listener)

        handle = self.__m_NextListenerID
        self.__m_NextListenerID += 1

        return handle


    def RemoveEventListener(self, handle : int):
        if handle < len(self.__m_EventListeners):
            self.__m_EventListeners.pop(handle)
            self.__m_NextListenerID -= 1
    
    def SendEvent(self, event : Event):
        for listener in self.__m_EventListeners:
            if not event.Handled():
                listener(event)