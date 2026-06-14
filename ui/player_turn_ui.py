from ui.base import *
from config import *
from grid.grid import Grid
from states.state_objects.cursor import Cursor

class PlayerTurnUI(UI):
    def __init__(self):
        super().__init__()
        self.PLAYER_TURN_TOOLTIP = MessageBlock(self.font)
        self.PLAYER_TURN_TOOLTIP.push("ENTER: finish turn", False, 1, MSG_BLACK)
        self.PLAYER_TURN_TOOLTIP.push("SPACE: select unit", False, 1, MSG_BLACK)
        self.PLAYER_TURN_TOOLTIP.push("ARROW KEYS: move cursor", False, 1, MSG_BLACK)

    def draw_tooltip(self, surface: pygame.Surface):
        self.PLAYER_TURN_TOOLTIP.render(surface, (TOOLTIP_POSITION_X, TOOLTIP_POSITION_Y))

    def draw_action_log(self, surface: pygame.Surface):
        self.action_log.render(surface, (ACTION_LOG_POSITION_X, ACTION_LOG_POSITION_Y))

    def draw_cursor_state(self, surface: pygame.Surface, grid: Grid, cursor: Cursor, accuracy: float):
        if abs(accuracy - 1e-7) < 0:
            tooltip = grid.get_tile(cursor.position).__str__()
            text_surface = self.font.render(tooltip, True, MSG_BLUE)
            surface.blit(text_surface, (CURRENT_TILE_INFO_POSITION_X, CURRENT_TILE_INFO_POSITION_Y))
        else:
            text_surface = self.font.render(f"Chance to hit: {accuracy}", True, MSG_BLUE)
            surface.blit(text_surface, (CURRENT_TILE_INFO_POSITION_X, CURRENT_TILE_INFO_POSITION_Y))

    def draw(self, surface: pygame.Surface, grid: Grid, cursor: Cursor):
        self.draw_tooltip(surface)
        self.draw_cursor_state(surface, grid, cursor)
        self.draw_action_log(surface)