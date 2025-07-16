from Maths.Maths import *
from UI.UICommon import *


class UIElement:

    def __init__(self, id : int):
        self.id : int = id

        # positions handled from the topleft 
        self.relativePosition : Vec2 = Vec2() # <-- normalised position 
        self.absolutePosition : Vec2 = Vec2() # <-- pixel position

        self.active : bool = True
        self.visible : bool = True



    def Update(self, dt):
        if not self.active:
            return
    
    
    def Draw(self):
        if not self.visible:
            return