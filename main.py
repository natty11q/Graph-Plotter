import pygame
import GlobalSettings
import sys, os
import time 

from Editor.Editor import Editor
import Utility.Temporal as Temporal
import UI.UICommon as Ucommon
import UI.Keys as Ukeys

from Event.EventHandler import *



from Common import *

class Main:
    def __init__(self):
        absPath = os.path.abspath(__file__)
        absFolder = os.path.dirname(absPath)

        pygame.init()
        GlobalSettings.Settings.Load(os.path.join(absFolder,"settings.json"))


        self.display_surface = pygame.display.set_mode(
                (GlobalSettings.Settings.WindowWidth,
                GlobalSettings.Settings.WindowHeight),
                pygame.DOUBLEBUF | pygame.RESIZABLE
             )
        
        self.clock = pygame.time.Clock()


        self.editor = Editor()
        self.editor.Initialise()

        self.running = False

        self.frameCount = 0

        # Ukeys.Keys.Init()
        Ucommon.IO.Init()

    def run(self):
        self.running = True
        self.display_surface.fill(color = (10,10,20), rect=None, special_flags=0)
        while self.running:
            # self.deltatime = self.clock.tick(GlobalSettings.Settings.FramerateCap) / 1000
            
            
            self.ManageEvents()
            self.Update()
            pygame.display.flip()

    def Save(self):
        print("saving ...")
        self.editor.Save()

    def ManageEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.editor.Quit()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                e : Event   = KeyDownEvent()
                e.keycode   = event.key
                sendEvent(e)

            elif event.type == pygame.KEYUP:
                e : Event   = KeyUpEvent()
                e.keycode   = event.key
                sendEvent(e)

            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                e : Event   = MouseButtonDownEvent()
                e.x = event.pos[0]
                e.y = event.pos[1]
                e.button = event.button
                sendEvent(e)

            elif event.type == pygame.MOUSEBUTTONUP:
                e : Event   = MouseButtonUpEvent()
                e.x = event.pos[0]
                e.y = event.pos[1]
                e.button = event.button
                sendEvent(e)

            elif event.type == pygame.MOUSEMOTION:
                e : Event   = MouseMovedEvent()
                e.x = event.pos[0]
                e.y = event.pos[1]
                sendEvent(e)
                
            elif event.type == pygame.MOUSEWHEEL:
                e : Event   = MouseScrollEvent()
                e.x = event.pos[0]
                e.y = event.pos[1]
                sendEvent(e)

            elif event.type == pygame.WINDOWMINIMIZED:
                ...
            elif event.type == pygame.WINDOWMAXIMIZED:
                ...
            elif event.type == pygame.WINDOWRESIZED:
                ...

            # TODO : COMPLETE EVENTS!!!

    def Update(self):
        Temporal.PlotEngineTime.Update()
        Ucommon.IO.Update()
        if Ucommon.IO.MouseDown[0] or Ucommon.IO.MouseDown[1] or Ucommon.IO.MouseDown[2]:
            print(Ucommon.IO.MouseClicked)
        self.editor.Update(Temporal.PlotEngineTime.DeltaTime())
        self.frameCount += 1
        # print("updating", self.frameCount)

        
if __name__ == '__main__':
    main = Main()
    main.run()
    # try:
    #     main.run()
    # except Exception as e:
    #     if e == KeyboardInterrupt:
    #         print("application interrupted")
    #     else:
    #         print("application Quit unexpectedly : ")
    #         print(e)
    #         # print(e.with_traceback)
    main.Save()
    pygame.quit()
    sys.exit()