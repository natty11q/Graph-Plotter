from Event.Event import * 

class MouseMovedEvent(Event):
    def __init__(self):
        super().__init__("MouseMoved")
        # New Mouse Position in screen coordinates under the current window.
        self.x : float = 0
        self.y : float = 0

        self.type = GP_EventType.MouseMoved


class MouseButtonDownEvent(Event):
    def __init__(self):
        super().__init__("MouseButtonDown")
        self.button : int = -1 # Mouse Button that was Down, 1 - LMB, 2 - MMB, 3 - RMB

        self.x : float = -1
        self.y : float = -1

        self.type = GP_EventType.MouseButtonDown
# class MouseButtonHeldEvent(Event):
#     def __init__(self):
#         super().__init__("MouseButtonHeld")
#         self.button : int = -1 # Mouse Button that is Held, 1 - LMB, 2 - MMB, 3 - RMB

class MouseButtonUpEvent(Event):
    def __init__(self):
        super().__init__("MouseButtonUp")
        self.button : int = -1 # Mouse Button that is Held, 1 - LMB, 2 - MMB, 3 - RMB

        self.x : float = -1
        self.y : float = -1

        self.type = GP_EventType.MouseButtonUp
class MouseScrollEvent(Event):
    def __init__(self):
        super().__init__("MouseScroll")
        self.x : float = -1
        self.y : float = -1

        self.type = GP_EventType.MouseScroll
        # Mouse Button that was Up, 1 - LMB, 2 - MMB, 3 - RMB
