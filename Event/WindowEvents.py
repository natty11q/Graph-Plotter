from Event.Event import * 

class WindowResizeEvent(Event):
    def __init__(self):
        super().__init__("WindowResize")
        self.width = 0
        self.height = 0

        self.type = GP_EventType.WindowResize

class WindowMinimisedEvent(Event):
    def __init__(self):
        super().__init__("WindowMinimised")
        self.type = GP_EventType.WindowMinimised

class WindowMaximisedEvent(Event):
    def __init__(self):
        super().__init__("WindowMaximised")
        self.type = GP_EventType.WindowMaximised

class WindowFocusLostEvent(Event):
    def __init__(self):
        super().__init__("WindowFocousLostEvent")
        self.type = GP_EventType.WindowFocusLost

class WindowFocusGainedEvent(Event):
    def __init__(self):
        super().__init__("WindowFocousGainedEvent")
        self.type = GP_EventType.WindowFocusGained

class WindowClosedEvent(Event):
    def __init__(self):
        super().__init__("WindowClose")
        self.type = GP_EventType.WindowClosed

class WindowRestoredEvent(Event):
    def __init__(self):
        super().__init__("WindowRestored")
        self.type = GP_EventType.WindowRestored

class WindowRestoredDownEvent(Event):
    def __init__(self):
        super().__init__("WindowRestoredDown")
        self.type = GP_EventType.WindowRestoredDown

