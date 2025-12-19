#Panda Stuff
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

#My Stuff
import master_fsm

loadPrcFile("../config/conf.prc")

class RPGBox(ShowBase):
    def __init__(self):
        super().__init__()
        #setting up the window
        self.disableMouse()
        game_state = master_fsm.MasterFSM(self)

world = RPGBox()
ShowBase.run(world)