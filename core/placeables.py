from enum import Enum, auto

class Placeable(Enum):
    UNIT_TEAM1 = auto()
    UNIT_TEAM2 = auto()
    COVER = auto()

    def __str__(self):
        match self:
            case Placeable.UNIT_TEAM1:
                return "Friendly unit"
            case Placeable.UNIT_TEAM2:
                return "Enemy unit"
            case Placeable.COVER:
                return "Cover"