import pygame

from grid.types import Point, GridPoint, PixelPoint
from  grid.grid_objects.base import GameObject
from config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, COLOR_TILE, TILE_RENDER_SCALE

class Tile:
    def __init__(self, grid_point: GridPoint):
        self.position = grid_point
        self.obj = None

    @property
    def occupied(self):
        if self.obj is None:
            return False
        return True

    def draw(self, surface):
        origin = to_pixel(self.position)
        pygame.draw.rect(surface, COLOR_TILE, pygame.Rect(origin.x, origin.y, TILE_SIZE*TILE_RENDER_SCALE, TILE_SIZE*TILE_RENDER_SCALE), 1)

    def __str__(self):
        if self.obj is None:
            return 'empty tile'
        else:
            return self.obj.__str__()


class Grid:
    def __init__(self, width: int=GRID_WIDTH, height: int=GRID_HEIGHT):
        self.width = width
        self.height = height
        self.tiles = [[Tile(GridPoint(x, y)) for x in range(width)] for y in range(height)]

    def draw(self, surface: pygame.Surface):
        for line in self.tiles:
            for tile in line:
                tile.draw(surface)

    def place_object(self, obj: GameObject) -> bool:
        if self.get_tile(obj.position.grid_point()).occupied:
            print("Placing on an occupied tile")
            return False
        else:
            self.get_tile(obj.position.grid_point()).obj = obj
            return True

    def get_tile(self, grid_point: GridPoint) -> Tile:
        return self.tiles[grid_point.y][grid_point.x]

    def in_bounds(self, grid_point: GridPoint) -> bool:
        return 0 <= grid_point.x < self.width and 0 <= grid_point.y < self.height
