from enum import Enum

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def tuple(self):
        return (self.x, self.y)


class GridPoint(Point):
    def __init__(self, x: float, y: float):
        self.x = round(x)
        self.y = round(y)

    def tuple(self):
        return (self.x, self.y)


class PixelPoint(Point):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def tuple(self):
        return (self.x, self.y)


class Direction(Enum):
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)

    @property
    def x(self):
        return self.value.x

    @property
    def y(self):
        return self.value.y
