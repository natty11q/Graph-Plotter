from Cocoa import NSApplication, NSColorPanel, NSObject #type: ignore
import sys
import threading
import time

class ColorPickerDelegate(NSObject):
    """Receives colour‐changed events and quits the app"""

    def colorPanelColorDidChange_(self, sender):
        c = sender.color()
        rgba = (c.redComponent(), c.greenComponent(), c.blueComponent(), c.alphaComponent())
        print("Selected RGBA:", rgba)
        # NSApplication.sharedApplication().terminate_(self)

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = ColorPickerDelegate.alloc().init()
    panel = NSColorPanel.sharedColorPanel()
    panel.setTarget_(delegate)
    panel.setAction_("colorPanelColorDidChange:")
    panel.makeKeyAndOrderFront_(None)

    # Keep the app running until the user picks a colour
    app.run()