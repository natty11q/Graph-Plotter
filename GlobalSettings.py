import os, json

class Settings:
    settingsPath        : str   | None = None

    EditorSettingsPath  : str   | None = None

    FramerateCap        : float | None = None
    VsyncEnabled        : bool  | None = None
    FramerateUncapped   : bool  | None = None
    
    GraphicsEngine      : str   | None = None

    
    DebugEnabled        : bool  | None = None

    @staticmethod
    def Load(settingsPath : str):
        Settings.settingsPath = settingsPath
        if not Settings.settingsPath:
            print("failed to load save settings")
            return

        with open(Settings.settingsPath, "r") as settings:
            data : dict = json.load(settings)
            
            
            EditorSettingsPath  = data.get("EditorSettingsPath", None)
            FramerateCap        = data.get("FramerateCap", 60)
            VsyncEnabled        = data.get("VsyncEnabled", False)
            FramerateUncapped   = data.get("FramerateUncapped", False)

            GraphicsEngine      = data.get("GraphicsEngine", "None")
            
            DebugEnabled        = data.get("DebugEnabled", False)





    @staticmethod
    def Save():
        if not Settings.settingsPath:
            print("failed to save settings")
            return
        
        with open(Settings.settingsPath, "r") as settings:
            data : dict = json.load(settings)

            if Settings.EditorSettingsPath:
                data["EditorSettingsPath"] = Settings.EditorSettingsPath
            if Settings.FramerateCap:
                data["FramerateCap"] = Settings.FramerateCap
            if Settings.VsyncEnabled:
                data["VsyncEnabled"] = Settings.VsyncEnabled
            if Settings.FramerateUncapped:
                data["FramerateUncapped"] = Settings.FramerateUncapped
            if Settings.GraphicsEngine:
                data["GraphicsEngine"] = Settings.GraphicsEngine
            if Settings.DebugEnabled:
                data["DebugEnabled"] = Settings.DebugEnabled
