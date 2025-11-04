from  panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.gui.DirectGui import *

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

app = MyApp()
app.run()