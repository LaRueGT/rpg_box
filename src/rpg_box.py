from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.gui.DirectGui import *
import sys

loadPrcFile("../config/conf.prc")

class MyApp(ShowBase):
    def __init__(self):
        super().__init__(self)
        #setting up the window
        self.disableMouse()
        properties = WindowProperties()
        #properties.setSize(1280, 720)
        #properties.setTitle("GUI experiments")
        self.win.requestProperties(properties)

        self.accept('escape', sys.exit)

    def intro_sequence(self):
        color_sequence = [(0, 0, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (0, 1, 0, 1)]
        sequence_position = 0
        # intro panel
        base_frame = DirectFrame(frameColor=(1, 0, 0, 1),
                                 frameSize=(-1.778, 1.778, -1, 1),
                                 pos=(0, 0, 0))
        art_frame = DirectFrame(parent=base_frame,
                                frameColor=(0, 0, 0, 1),
                                frameSize=(-1.715, 1.715, -.88, .94),
                                pos=(0, 0, 0))

app = MyApp()
app.run()