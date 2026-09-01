"""Shared DirectGUI design system using explicit Aspect2D coordinates."""
from pathlib import Path

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from panda3d.core import Filename, NodePath, TextNode, TextureStage


class GuiRoot:
    """Common typography, colors, bounds, and reusable screen components."""

    LEFT, RIGHT = -1.33, 1.33
    BOTTOM, TOP = -1.0, 1.0
    SAFE = (-1.27, 1.27, -0.90, 0.90)
    TITLE, BODY, SMALL, BUTTON = 0.07, 0.05, 0.04, 0.045
    INK = (0.12, 0.07, 0.03, 1)
    GOLD = (0.82, 0.61, 0.22, 1)
    PAPER = (0.92, 0.84, 0.65, 0.96)
    PANEL = (0.10, 0.06, 0.03, 0.82)

    def __init__(self, base):
        self.base_window = base
        root = Path(__file__).resolve().parents[2]
        # Convert Windows paths to Panda3D's VFS format before loading.  Passing
        # the native ``C:\\...`` string directly makes the font loader fail.
        font_path = Filename.fromOsSpecific(
            str(root / "fonts" / "EBGaramond-VariableFont_wght.ttf")
        )
        wood_texture = Filename.fromOsSpecific(
            str(root / "assets" / "wood_table_tex.jpg")
        )
        self.label_font = base.loader.loadFont(str(font_path))
        if self.label_font is None:
            raise RuntimeError(f"Unable to load UI font: {font_path}")
        self.base_frame = DirectFrame(
            frameColor=(1, 1, 1, 1), frameSize=(self.LEFT, self.RIGHT, self.BOTTOM, self.TOP),
            pos=(0, 0, 0), frameTexture=str(wood_texture),
        )
        self.base_frame.guiItem.get_state_def(0).set_tex_scale(TextureStage.getDefault(), 1, 0.562)

    def make_label(self, parent, text="", scale=BODY, pos=(0, 0, 0),
                   align=TextNode.ALeft, wordwrap=None, color=None):
        args = dict(parent=parent, text=text, text_font=self.label_font,
                    text_scale=(scale, scale), text_align=align, pos=pos,
                    frameColor=(0, 0, 0, 0), text_fg=color or self.INK)
        if wordwrap is not None:
            args["text_wordwrap"] = wordwrap
        return DirectLabel(**args)

    def make_button(self, parent, text, command, extra_args=None,
                    hotkey=False, scale=BUTTON):
        """Make a uniform button; brackets visually isolate its keyboard hint."""
        shown = f"[{text[0]}] {text[1:]}" if hotkey and text else text
        return DirectButton(
            parent=parent, text=shown, text_font=self.label_font,
            text_scale=(scale, scale), text_fg=self.INK,
            frameColor=(0.78, 0.58, 0.25, 0.92),
            frameSize=(-1.45, 1.45, -0.42, 0.42), relief=DGG.RAISED,
            command=command, extraArgs=extra_args or [],
        )

    def clear_gui(self):
        self.base_frame.node().removeAllChildren()

    def make_full_page_frame(self) -> NodePath:
        return DirectFrame(parent=self.base_frame, frameColor=self.PANEL,
                           frameSize=self.SAFE, pos=(0, 0, 0))

    def make_grid_paper_page(self) -> NodePath:
        path = Filename.fromOsSpecific(
            str(Path(__file__).resolve().parents[2] / "assets" / "gridpaper_tex.png")
        )
        frame = DirectFrame(parent=self.base_frame, frameColor=(1, 1, 1, 1),
                            frameSize=self.SAFE, pos=(0, 0, 0), frameTexture=str(path))
        frame.guiItem.get_state_def(0).set_tex_scale(TextureStage.getDefault(), 1, 0.53)
        return frame

    def make_button_row(self, parent=None, frame_color=(0, 0, 0, 0)) -> NodePath:
        return DirectBoxSizer(
            orientation=DGG.HORIZONTAL,
            parent=parent if parent is not None else self.base_frame,
            frameColor=frame_color, frameSize=(-1.22, 1.22, -0.13, 0.13),
            pos=(0, 0, -0.77), itemMargin=(0.035, 0.035, 0.02, 0.02),
        )

    def make_content_frame(self, frame_color=PANEL,
                           frame_size=(-1.18, 1.18, -0.62, 0.70), pos=(0, 0, 0)) -> NodePath:
        return DirectFrame(parent=self.base_frame, frameColor=frame_color,
                           frameSize=frame_size, pos=pos)


Gui = GuiRoot
