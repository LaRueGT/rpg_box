#Panda Stuff
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
#My Stuff
import master_fsm

loadPrcFile("../config/conf.prc")

class RPGBox(ShowBase):
    def __init__(self):
        super().__init__(self)
        #setting up the window
        self.disableMouse()
        myFSM = master_fsm.MasterFSM(self)

world = RPGBox()
world.run()