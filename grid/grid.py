import pygame

from grid.types import GridPoint, OutOfBoundsError, TileOccupiedError, to_pixel
from  grid.grid_objects.base import GameObject
from config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, COLOR_TILE, TILE_RENDER_SCALE

class Tile:
    def __init__(self, grid_point: GridPoint):
        self.position = grid_point
        self.obj: GameObject | None = None

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
        self.tiles = [[Tile((x, y)) for x in range(width)] for y in range(height)]
        self.objects: list[GameObject] = []

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, surface: pygame.Surface):
        for line in self.tiles:
            for tile in line:
                tile.draw(surface)
        for obj in self.objects:
            obj.draw(surface)

    def get_tile(self, grid_point: GridPoint) -> Tile:
        return self.tiles[grid_point.y][grid_point.x]

    def place_object(self, obj: GameObject):
        """
        Place an object on the grid at its current position.

        Args:
            obj: The game object to place. Its position attribute determines placement.

        Raises:
            OutOfBoundsError: If the object's position is outside the grid.
            TileOccupiedError: If the target tile is already occupied.
        """
        position = obj.position
        if not self.in_bounds(position):
            raise OutOfBoundsError("Trying to place an object outside of the grid")
        if self.occupied(position):
            raise TileOccupiedError("Trying to place an object on an occupied tile")
        self.get_tile(position).obj = obj
        self.objects.append(obj)

    def remove_object(self, grid_point: GridPoint):
        """
        Remove an object at a specified position.
        Sets the tile.obj to None and removes the objects from grid.objects.
        If the tile is empty, does nothing.

        Args:
            grid_point: grid position at which to attempt to remove an object.
        """
        if not self.occupied(grid_point):
            return
        for obj in self.objects[:]:
            if obj.position == grid_point:
                self.objects.remove(obj)
                break
        self.get_tile(grid_point).obj = None

    def move_object(self, start_point: GridPoint, end_point: GridPoint):
        """
        Move an object from start to end.
        Changes the object.position, start and end tile.obj.

        Raises:
            OutOfBoundsError: If either points are outside the grid.
            TileOccupiedError: If the end tile is occupied.
        """
        if not self.in_bounds(start_point):
            raise OutOfBoundsError("Move start tile is out of bounds")
        if not self.in_bounds(end_point):
            raise OutOfBoundsError("Move end tile is out of bounds")
        start_tile = self.get_tile(start_point)
        end_tile = self.get_tile(end_point)
        if not start_tile.occupied:
            return
        if end_tile.occupied:
            raise TileOccupiedError("Trying to move an object onto an occupied tile")
        obj = start_tile.obj
        obj.position = end_point
        end_tile.obj = obj
        start_tile.obj = None
        
        
    def in_bounds(self, grid_point: GridPoint):
        bounded_on_x = grid_point[0] >= 0 and grid_point[0] < self.width
        bounded_on_y = grid_point[1] >= 0 and grid_point[1] < self.height
        return bounded_on_x and bounded_on_y
    
    def occupied(self, grid_point: GridPoint):
        return self.get_tile(grid_point).occupied