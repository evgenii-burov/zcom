from base import GameObject
from util.types import Point, GridPoint
from core.team import Team


class Unit(GameObject):
    def __init__(self, position: GridPoint, hidden: bool, selected: bool, team: Team):
        super().__init__(position, hidden, selected)
        self.team = team

