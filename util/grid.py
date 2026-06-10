import pygame

from util.types import Point, GridPoint, PixelPoint
from config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, COLOR_TILE, TILE_RENDER_SCALE

class Tile:
    def __init__(self, grid_point: GridPoint):
        self.position = grid_point
        self.has_cover = False
        self.unit = None

    @property
    def blocked(self):
        return self.has_cover

    @property
    def occupied(self):
        return self.unit is not None

    def draw(self, surface):
        origin = to_pixel(self.position)
        pygame.draw.rect(surface, COLOR_TILE, pygame.Rect(origin.x, origin.y, TILE_SIZE*TILE_RENDER_SCALE, TILE_SIZE*TILE_RENDER_SCALE), 1)


def to_pixel(grid_point: GridPoint) -> PixelPoint:
    return PixelPoint(grid_point.x * TILE_SIZE, grid_point.y * TILE_SIZE)


def to_grid(pixel_point: PixelPoint) -> GridPoint:
    return GridPoint(pixel_point.x // TILE_SIZE, pixel_point.y // TILE_SIZE)


class Grid:
    def __init__(self, width: int=GRID_WIDTH, height: int=GRID_HEIGHT):
        self.width = width
        self.height = height
        self.tiles = [[Tile(Point(x, y)) for x in range(width)] for y in range(height)]

    def draw(self, surface: pygame.Surface):
        for line in self.tiles:
            for tile in line:
                tile.draw(surface)

    def get_tile(self, x, y) -> Tile:
        return self.tiles[y][x]

    def in_bounds(self, grid_point: GridPoint) -> bool:
        return 0 <= grid_point.x < self.width and 0 <= grid_point.y < self.height

    # def is_passable(self, x, y) -> bool:
    #     return self.in_bounds(x, y) and not self.tiles[y][x].blocked

# def is_occupied(self, x, y) -> bool: ...
# def place_cover(self, x, y): ...
# def place_unit(self, x, y, unit): ...
# def remove_unit(self, x, y): ...
# def get_unit(self, x, y) -> Unit | None: ...