from enum import Enum, auto
from grid.grid_objects.unit import Unit
from grid.grid_objects.cover import Cover
from grid.types import GridPoint
from core.team import Team
from state_manager import StateManager
from states.state_objects.cursor import Cursor

class Placeable(Enum):
    UNIT_TEAM1 = auto()
    UNIT_TEAM2 = auto()
    COVER = auto()
    DELETE = auto()

    def get_instance(self, grid_point: GridPoint):
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
    def __init__(self, game, state):
        super().__init__(game, state)
        self.placeables = [x for x in Placeable]
        self.current_placeable = self.placeables[0]
        self.cursor = Cursor()

    def handle_events(self):
        return super().handle_events()
    
    def update(self):
        return super().update()
    
    def draw(self):
        return super().draw()