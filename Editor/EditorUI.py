from UI.UIBase import *
from Utility.CoreUtility import *


class EditorUI(UIManager):

    def __init__(self) -> None:
        super().__init__()
        self.Elements : list [UIElement] = []

        self.Load()
    

    def Load(self, iniFilepat : str = "./"):
        ...

    def Update(self):
        ...
    
    