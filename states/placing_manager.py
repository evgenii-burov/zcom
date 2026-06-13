from enum import Enum, auto
from config import *
from grid.grid_objects.base import GameObject
from grid.grid_objects.unit import Unit
from grid.grid_objects.cover import Cover
from grid.types import GridPoint
from grid.grid_objects.unit import Team
from .state_manager import StateManager, State
from .player_turn_manager import PlayerTurnManager
from .state_objects.cursor import Cursor
from .util.handle_cursor_movement import handle_cursor_movement
from ui.placing_ui import PlacingUI
import pygame

class Placeable(Enum):
    UNIT_TEAM1 = auto()
    UNIT_TEAM2 = auto()
    COVER = auto()
    DELETE = auto()

    def get_instance(self, grid_point: GridPoint) -> GameObject | None:
        match self:
            case Placeable.DELETE:
                return None
            case Placeable.UNIT_TEAM1:
                return Unit(grid_point, False, False, Team.TEAM1)
            case Placeable.UNIT_TEAM2:
                return Unit(grid_point, False, False, Team.TEAM2)
            case Placeable.COVER:
                return Cover(grid_point, False, False)

    def __str__(self):
        match self:
            case Placeable.DELETE:
                return "Erase"
            case Placeable.UNIT_TEAM1:
                return "Friendly unit"
            case Placeable.UNIT_TEAM2:
                return "Enemy unit"
            case Placeable.COVER:
                return "Cover"


class PlacingManager(StateManager):
    def __init__(self, game, state=State.PLACING, ui=PlacingUI()):
        super().__init__(game, state, ui)
        self.placeables = [x for x in Placeable]
        self.current_placeable_index = 0
        self.current_placeable = self.placeables[self.current_placeable_index]
        self.cursor = Cursor()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # Cursor movement
            handle_cursor_movement(event, self.cursor, (self.game.grid.width, self.game.grid.height))
            # Space for placing
            if event.key == pygame.K_SPACE:
                obj = self.current_placeable.get_instance(self.cursor.position)
                if obj is None:
                    self.game.grid.remove_object(self.cursor.position)
                    return
                self.game.grid.remove_object(obj.position)
                self.game.grid.place_object(obj)
                self.ui.log_message(f"Placed {obj.__str__()}", True, 3, MSG_BLACK)
                return
            # Tab for placeable switching
            if event.key == pygame.K_TAB:
                self.current_placeable_index = (self.current_placeable_index + 1) % len(self.placeables)
                self.current_placeable = self.placeables[self.current_placeable_index]
                return
            # Enter to finish placing
            if event.key == pygame.K_RETURN:
                self.ui.log_message(f"Finished placing", True, 5, MSG_BLUE)
                self.switch_state(PlayerTurnManager(self.game, State.PLAYER_TURN))
                return
    
    def update(self):
        super().update()

    
    def draw(self):
        super().draw()
        self.cursor.draw(self.game.screen)
        self.ui.draw(self.game.screen, self.current_placeable)