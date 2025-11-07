#Panda Stuff
from panda3d.core import loadPrcFile
from direct.showbase.ShowBase import ShowBase
#Python Stuff
import sys
#My Stuff
import slideshow, narrative
import gui

loadPrcFile("../config/conf.prc")

class MyApp(ShowBase):
    def __init__(self):
        super().__init__(self)
        #setting up the window
        self.disableMouse()
        ui = gui.Gui(self)
        #intro
        slide_frame = ui.centerfold_frame()
        intro = slideshow.Slideshow(self, slide_frame)
        intro.display_intro_sequence()
        #test narrative panels
        ui.clear_gui()
        narrative_frame, text_label = ui.narrative_frame()
        narrative_test = narrative.Narrative(self, narrative_frame, text_label)
        narrative_test.display_dummy_narrative()

app = MyApp()
app.run()