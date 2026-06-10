import pygame
from objects.cursor import Cursor
from util.grid import Grid
from core.state import State
from core.placeables import Placeable
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 22)
        self.font.bold = True

    def _render_multiline(self, surface, text, pos, line_spacing=5):
        x, y = pos
        for line in text.splitlines():
            line = line.replace('\t', '    ')  # handle tabs too
            line_surf = self.font.render(line, True, (0,0,0))
            surface.blit(line_surf, (x, y))
            y += self.font.get_linesize() + line_spacing

    def draw(self, surface: pygame.Surface, state:State, cursor: Cursor, grid: Grid, placeable: Placeable):
        if state == State.PLACING:
            text = (f"Placing object: {placeable.__str__()}\n"
                    "ARROW KEYS: move cursor\n"
                    "TAB: switch object")

            self._render_multiline(surface, text, (SCREEN_WIDTH*0, SCREEN_HEIGHT*.8))

