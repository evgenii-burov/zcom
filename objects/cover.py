from objects.base import GameObject
from util.types import Point, GridPoint


class Cover(GameObject):
    def __init__(self, grid_point:GridPoint, hidden:bool, selected):
        super().__init__()