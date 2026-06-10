from enum import Enum, auto
from objects.base import GameObject
from objects.unit import Unit
from objects.cover import Cover
from util.types import GridPoint
from core.team import Team

class Placeable(Enum):
    UNIT_TEAM1 = auto()
    UNIT_TEAM2 = auto()
    COVER = auto()

    def get_instance(self, grid_point: GridPoint)->GameObject:
        match self:
            case Placeable.UNIT_TEAM1:
                return Unit(grid_point, False, False, Team.TEAM1)
            case Placeable.UNIT_TEAM2:
                return Unit(grid_point, False, False, Team.TEAM2)
            case Placeable.COVER:
                return Cover(grid_point, False, False)

    def __str__(self):
        match self:
            case Placeable.UNIT_TEAM1:
                return "Friendly unit"
            case Placeable.UNIT_TEAM2:
                return "Enemy unit"
            case Placeable.COVER:
                return "Cover"