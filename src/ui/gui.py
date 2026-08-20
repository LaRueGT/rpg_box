from direct.gui.DirectGui import DirectFrame
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from panda3d.core import NodePath, TextureStage
from panda3d.core import TextProperties, TextPropertiesManager


class GuiRoot:
    """Shared UI context and reusable screen-level visual components."""

    def __init__(self, base):
        self.base_window = base
        self.label_font = base.loader.loadFont('../fonts/EBGaramond-VariableFont_wght.ttf')
        self.configure_text_colors()
        self.base_frame = DirectFrame(
            frameColor=(1, 1, 1, 1), frameSize=(-1.778, 1.778, -1, 1),
            pos=(0, 0, 0), frameTexture='../assets/wood_table_tex.jpg',
        )
        self.base_frame.guiItem.get_state_def(0).set_tex_scale(
            TextureStage.getDefault(), 1, 0.562
        )

    @staticmethod
    def configure_text_colors():
        tpm = TextPropertiesManager.getGlobalPtr()
        for name, color in (
            ('red', (1.0, 0.0, 0.0, 1.0)),
            ('green', (0.0, 1.0, 0.0, 1.0)),
            ('blue', (0.0, 0.0, 1.0, 1.0)),
        ):
            properties = TextProperties()
            properties.setTextColor(*color)
            tpm.setProperties(name, properties)

    def clear_gui(self):
        self.base_frame.node().removeAllChildren()

    def make_full_page_frame(self) -> NodePath:
        return DirectFrame(parent=self.base_frame, frameColor=(0, 0, 0, 1),
                           frameSize=(-1.715, 1.715, -.88, .94), pos=(0, 0, 0))

    def make_grid_paper_page(self) -> NodePath:
        frame = DirectFrame(parent=self.base_frame, frameColor=(1, 1, 1, 1),
                            frameSize=(-1.715, 1.715, -.88, .94), pos=(0, 0, 0),
                            frameTexture='../assets/gridpaper_tex.png')
        frame.guiItem.get_state_def(0).set_tex_scale(TextureStage.getDefault(), 1, 0.53)
        return frame

    def make_button_row(self, parent=None, frame_color=(0, 0, 0, 1)) -> NodePath:
        return DirectBoxSizer(orientation=DGG.HORIZONTAL,
                              parent=parent if parent is not None else self.base_frame,
                              frameColor=frame_color,
                              frameSize=(-.25, .25, -.25, .25),
                              pos=(-1.715, 0, -.91))

    def make_content_frame(self, frame_color=(0, 0, 0, 1),
                           frame_size=(-1.715, 1.715, -.46, .94),
                           pos=(0, 0, 0)) -> NodePath:
        return DirectFrame(parent=self.base_frame, frameColor=frame_color,
                           frameSize=frame_size, pos=pos)


# Compatibility for older callers while the application migrates to GuiRoot.
Gui = GuiRoot
