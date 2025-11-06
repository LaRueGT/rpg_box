#Panda Stuff
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
#Python Stuff
import sys
#My Stuff
import slideshow

loadPrcFile("../config/conf.prc")

class MyApp(ShowBase):
    def __init__(self):
        super().__init__(self)
        #setting up the window
        self.disableMouse()

        self.accept('escape', sys.exit)
        slideshow.display_intro_sequence(self)



app = MyApp()
app.run()