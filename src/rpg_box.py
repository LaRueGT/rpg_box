#Panda Stuff
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
#Python Stuff
import sys
#My Stuff
import slideshow
import gui

loadPrcFile("../config/conf.prc")

class MyApp(ShowBase):
    def __init__(self):
        super().__init__(self)
        #setting up the window
        self.disableMouse()
        ui = gui.gui(self)
        intro = slideshow.slideshow(self, ui)
        intro.display_intro_sequence()

app = MyApp()
app.run()