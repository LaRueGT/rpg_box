"""The in-game, matte-style scene screen.

Scenes are deliberately data-driven.  A scene is an iterable of page mappings
with ``art`` and ``text`` keys, followed by optional ``choices`` on the scene
or on its final page.  This keeps the screen useful before the world/story
systems exist and gives those systems a small, stable UI boundary later.
"""

from pathlib import Path
import textwrap

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectScrolledFrame
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from panda3d.core import CardMaker, Filename, TextNode

from rules import ability_rules


class MatteMenu(DirectObject):
    """Display a sequence of art-and-text pages and then scene choices."""

    def __init__(self, base, ui, party, scene=None, art=None, text=None, choices=None):
        super().__init__()
        self.base_window, self.ui, self.party = base, ui, party
        if scene is None and any(value is not None for value in (art, text, choices)):
            scene = {"art": art, "text": text or "", "choices": choices or []}
        self.scene = scene or self.default_scene()
        self.pages = self._pages_from_scene(self.scene)
        self.page_index = 0
        self._finished_pages = False
        self._art_card = None
        # The matte reference was 4:3, while conf.prc is now 1280x720.
        # Derive the horizontal geometry from the actual aspect ratio so the
        # scene uses the extra 16:9 width without changing its vertical rhythm.
        half_width = min(1.68, ui.screen_bounds[1] - .08)
        self.page_left, self.page_right = -half_width, half_width
        self.divider = -.12
        self.story_width = self.page_right - self.page_left
        self.text_width = max(43, int(self.story_width * 19.5))

        self.art_frame = DirectFrame(
            parent=ui.base_frame, frameColor=(.08, .05, .03, 1),
            frameSize=(self.page_left, self.divider, -.22, .76), pos=(0, 0, 0), relief=1,
        )
        self.party_frame = DirectFrame(
            parent=ui.base_frame, frameColor=ui.PANEL,
            frameSize=(self.divider + .04, self.page_right, .20, .76), pos=(0, 0, 0), relief=1,
        )
        self.status_frame = DirectFrame(
            parent=ui.base_frame, frameColor=ui.PANEL,
            frameSize=(self.divider + .04, self.page_right, -.22, .16), pos=(0, 0, 0), relief=1,
        )
        self.story_frame = DirectScrolledFrame(
            parent=ui.base_frame, frameColor=ui.PANEL,
            frameSize=(self.page_left, self.page_right, -.78, -.27),
            canvasSize=(self.page_left + .10, self.page_right - .10, -.50, .42),
            scrollBarWidth=.035,
        )
        self.story_label = None
        self.prompt = ui.make_label(
            ui.base_frame, "", scale=ui.SMALL, pos=(self.page_right - .05, 0, -.81),
            align=TextNode.ARight, color=ui.GOLD,
        )
        self.buttons = ui.make_button_row()
        self._make_party_panel()
        self._make_status_panel()
        self.accept("enter", self.advance)
        self.accept("space", self.advance)
        self.accept("escape", self.handle_back)

    @staticmethod
    def default_scene():
        return {"pages": [{"art": "assets/slide1.png", "text":
            "The road opens before you.  What waits beyond the next hill is not yet known."}],
            "choices": []}

    @staticmethod
    def _pages_from_scene(scene):
        if isinstance(scene, dict):
            pages = scene.get("pages")
            if pages is None:
                pages = [{"art": scene.get("art"), "text": scene.get("text", "")}]
        else:
            pages = scene
        if isinstance(pages, str):
            pages = [{"text": pages}]
        return list(pages or [{"text": ""}])

    def _make_party_panel(self):
        self.ui.make_label(self.party_frame, "NAME                 AC   HP",
                           scale=self.ui.SMALL, pos=(-.05, 0, .66), color=self.ui.GOLD)
        rows = []
        for member in self.party.members:
            try:
                ac = ability_rules.armor_class(member.dexterity)
            except (AttributeError, TypeError, ValueError):
                ac = "-"
            rows.append(f"{member.name or 'Unnamed':<18.18} {ac:>3} {member.max_hp:>4}")
        self.ui.make_label(self.party_frame, "\n".join(rows) or "(no party)",
                           scale=self.ui.SMALL, pos=(-.05, 0, .58), color=self.ui.PAPER)

    def _make_status_panel(self):
        self.ui.make_label(self.status_frame, "N  1,2\nE  9:00 AM\n    READY",
                           scale=self.ui.SMALL, pos=(-.05, 0, .10), color=self.ui.PAPER)

    def _set_art(self, art):
        if self._art_card:
            self._art_card.removeNode()
            self._art_card = None
        if not art:
            return
        if hasattr(art, "getXSize"):
            texture = art
        else:
            path = Path(art)
            if not path.is_absolute():
                path = Path(__file__).resolve().parents[3] / path
            texture = self.base_window.loader.loadTexture(
                str(Filename.fromOsSpecific(str(path))))
        if texture is None:
            return
        card = CardMaker("scene-art")
        card.setFrame(self.page_left + .12, self.divider - .10, -.12, .64)
        self._art_card = self.art_frame.attachNewNode(card.generate())
        self._art_card.setTexture(texture)

    def _set_story(self, text):
        if self.story_label:
            self.story_label.removeNode()
        lines = str(text or "").splitlines() or [""]
        # DirectLabel wraps at render time, so include wrapped lines when
        # sizing the canvas; otherwise long prose would be clipped without a
        # useful scrollbar.
        wrapped_lines = sum(max(1, len(textwrap.wrap(line, width=self.text_width))) for line in lines)
        line_count = max(8, wrapped_lines + 1)
        canvas_left = self.page_left + .10
        canvas_right = self.page_right - .10
        self.story_frame["canvasSize"] = (canvas_left, canvas_right, -line_count * .065, .42)
        self.story_label = DirectLabel(
            parent=self.story_frame.getCanvas(), text=str(text or ""),
            text_font=self.ui.label_font, text_scale=(self.ui.BODY, self.ui.BODY),
            text_fg=self.ui.PAPER, text_align=TextNode.ALeft,
            text_wordwrap=self.text_width, pos=(canvas_left + .02, 0, .35),
            frameColor=(0, 0, 0, 0),
        )
        self.story_frame.verticalScroll["value"] = 0

    def display(self):
        self._show_page()

    def _show_page(self):
        page = self.pages[self.page_index]
        self._set_art(page.get("art") if isinstance(page, dict) else None)
        self._set_story(page.get("text", "") if isinstance(page, dict) else page)
        self.prompt["text"] = "[ENTER / SPACE] CONTINUE"
        self.buttons.clear_items()

    def advance(self):
        if self._finished_pages:
            return
        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self._show_page()
            return
        self._finished_pages = True
        self._show_choices()

    def _show_choices(self):
        choices = self.scene.get("choices", []) if isinstance(self.scene, dict) else []
        if not choices and isinstance(self.pages[-1], dict):
            choices = self.pages[-1].get("choices", [])
        self.prompt["text"] = ""
        if not choices:
            self._add_button("Back", self.handle_back)
            return
        for choice in choices:
            if isinstance(choice, str):
                label, value = choice, choice
            else:
                label, value = choice.get("label", "Choose"), choice.get("value", choice)
            self._add_button(label, self.handle_choice, value)

    def _add_button(self, label, command, value=None):
        button = DirectButton(parent=self.buttons, text=label, scale=self.ui.BUTTON,
                              text_font=self.ui.label_font, command=command,
                              extraArgs=[] if value is None else [value])
        self.buttons.addItem(button)

    def handle_choice(self, choice):
        messenger.send("matte_menu_choice", [choice])

    def handle_back(self):
        messenger.send("main_menu_requested")
