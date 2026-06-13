from __future__ import annotations
from typing import TYPE_CHECKING
from ui.base import *
from config import *

if TYPE_CHECKING:
    from states.placing_manager import Placeable

class PlacingUI(UI):
    def __init__(self):
        super().__init__()

        self.PLACING_TOOLTIP = MessageBlock(self.font)
        self.PLACING_TOOLTIP.push("ENTER: finish placing", False, 1, MSG_BLACK)
        self.PLACING_TOOLTIP.push("TAB: switch object", False, 1, MSG_BLACK)
        self.PLACING_TOOLTIP.push("SPACE: place object", False, 1, MSG_BLACK)
        self.PLACING_TOOLTIP.push("ARROW KEYS: move cursor", False, 1, MSG_BLACK)

        # self.PLAYER_TURN_TOOLTIP = MessageBlock(self.font)
        # self.PLAYER_TURN_TOOLTIP.push("ENTER: finish turn", False, 1, MSG_BLACK)
        # self.PLAYER_TURN_TOOLTIP.push("SPACE: select unit", False, 1, MSG_BLACK)
        # self.PLAYER_TURN_TOOLTIP.push("ARROW KEYS: move cursor", False, 1, MSG_BLACK)

    def draw_tooltip(self, surface: pygame.Surface):
        self.PLACING_TOOLTIP.render(surface, PixelPoint(TOOLTIP_POSITION_X, TOOLTIP_POSITION_Y))
        # if state == State.PLAYER_TURN:
        #     self.PLAYER_TURN_TOOLTIP.render(surface, PixelPoint(TOOLTIP_POSITION_X, TOOLTIP_POSITION_Y))

    def draw_action_log(self, surface: pygame.Surface):
        self.action_log.render(surface, PixelPoint(ACTION_LOG_POSITION_X, ACTION_LOG_POSITION_Y))

    def draw_cursor_state(self, surface: pygame.Surface, placeable: Placeable):
        text_surface = self.font.render(f'Cursor: {placeable.__str__()}', True, MSG_BLUE)
        surface.blit(text_surface, (CURRENT_TILE_INFO_POSITION_X, CURRENT_TILE_INFO_POSITION_Y))
        # if state == State.PLAYER_TURN:
        #     tooltip = grid.get_tile(cursor.position).__str__()
        #     text_surface = self.font.render(tooltip, True, MSG_BLUE)
        #     surface.blit(text_surface, (CURRENT_TILE_INFO_POSITION_X, CURRENT_TILE_INFO_POSITION_Y))

    def draw(self, surface: pygame.Surface, placeable: Placeable):
        self.draw_tooltip(surface)
        self.draw_cursor_state(surface, placeable)
        self.draw_action_log(surface)