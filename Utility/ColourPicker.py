from Cocoa import NSApplication, NSColorPanel,NSBundle,  NSColor, NSObject, NSNotificationCenter, NSWindowWillCloseNotification #type: ignore
import objc
import sys , os
import threading
from multiprocessing import Process, Manager
import time

from Maths.Maths import *


# array_lock = threading.Lock()

# def getMutex():
#     return array_lock

class ColorPickerDelegate(NSObject):
    data = objc.ivar()# type: ignore


    def initWithData_(self, data):
        self = objc.super(ColorPickerDelegate, self).init()# type: ignore
        if self is None:
            return None
        self.data = data
        return self

    def colorPanelColorDidChange_(self, sender):
        if self.data["shouldClose"]:
            NSApplication.sharedApplication().terminate_(self)
        c = sender.color()
        self.data["colour"] = [c.redComponent() * 255,c.greenComponent() * 255,c.blueComponent() * 255]
    
    def windowWillClose_(self, notification):
        print("Color panel closed.")
        NSApplication.sharedApplication().terminate_(self)
        os._exit(0)

def RunWheel(data: dict):
    with objc.autorelease_pool():
        info = NSBundle.mainBundle().infoDictionary()
        info["LSUIElement"] = "1"
        
        app = NSApplication.sharedApplication()
        app.activateIgnoringOtherApps_(True)

        delegate = ColorPickerDelegate.alloc().initWithData_(data)

        panel = NSColorPanel.sharedColorPanel()
        

        firstcol = data["colour"]
        panel.setColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(firstcol[0] / 255, firstcol[1] / 255, firstcol[2] / 255, 1.0))
        panel.setTarget_(delegate)
        notification_center = NSNotificationCenter.defaultCenter() #type: ignore
        notification_center.addObserver_selector_name_object_(
            delegate,
            b"windowWillClose:",
            NSWindowWillCloseNotification,#type: ignore
            panel
        )
        panel.setAction_("colorPanelColorDidChange:")
        panel.makeKeyAndOrderFront_(None)

    app.run()