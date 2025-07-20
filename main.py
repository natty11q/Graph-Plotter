import pygame
import GlobalSettings
import sys, os
import time 

from Editor.Editor import Editor



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

        self.deltatime : float = sys.float_info.min  # avoid potential div by 0 errors on stuartup

        self.frameCount = 0

    def run(self):
        self.running = True
        self.display_surface.fill(color = (10,10,20), rect=None, special_flags=0)
        while self.running:
            self.deltatime = self.clock.tick(GlobalSettings.Settings.FramerateCap) / 1000
            
            
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

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("picker om")
                    self.editor.BackgroundColourPicker()


    def Update(self):
        self.editor.Update(self.deltatime)
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