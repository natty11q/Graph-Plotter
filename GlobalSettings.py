import os, json

class Settings:
    settingsPath        : str   | None = None

    EditorSettingsPath  : str   | None = None

    FramerateCap        : float = 0
    VsyncEnabled        : bool  = False
    FramerateUncapped   : bool  = False
    
    GraphicsEngine      : str   | None = None

    
    DebugEnabled        : bool  | None = None


    WindowWidth         : float = 900
    WindowHeight        : float = 600

    WindowMinWidth      : float = 450
    WindowMinHeight     : float = 300

    @staticmethod
    def Load(settingsPath : str):
        Settings.settingsPath = settingsPath
        if not Settings.settingsPath:
            print("failed to load save settings")
            return

        with open(Settings.settingsPath, "r") as settings:
            data : dict = json.load(settings)
            
            
            Settings.EditorSettingsPath     = data.get("EditorSettingsPath", None)
            Settings.FramerateCap           = data.get("FramerateCap", 60)
            Settings.VsyncEnabled           = data.get("VsyncEnabled", False)
            Settings.FramerateUncapped      = data.get("FramerateUncapped", False)

            Settings.GraphicsEngine         = data.get("GraphicsEngine", "None")

            Settings.DebugEnabled           = data.get("DebugEnabled", False)
            

            windowDims                      = data.get("WindowDimensions", [10,10])
            windowMinDims                   = data.get("WindowMinDimensions", [10,10])

            Settings.WindowWidth            = windowDims[0]
            Settings.WindowHeight           = windowDims[1]
            Settings.WindowMinWidth         = windowMinDims[0]
            Settings.WindowMinHeight        = windowMinDims[1]





    @staticmethod
    def Save():
        if not Settings.settingsPath:
            print("failed to save settings")
            return
        
        with open(Settings.settingsPath, "r+") as settings:
            data : dict = json.load(settings)

            if Settings.EditorSettingsPath is not None:
                data["EditorSettingsPath"] = Settings.EditorSettingsPath
            if Settings.FramerateCap is not None:
                data["FramerateCap"] = Settings.FramerateCap
            if Settings.VsyncEnabled is not None:
                data["VsyncEnabled"] = Settings.VsyncEnabled
            if Settings.FramerateUncapped is not None:
                data["FramerateUncapped"] = Settings.FramerateUncapped
            if Settings.GraphicsEngine is not None:
                data["GraphicsEngine"] = Settings.GraphicsEngine
            if Settings.DebugEnabled is not None:
                data["DebugEnabled"] = Settings.DebugEnabled

            json.dump(data, settings)
