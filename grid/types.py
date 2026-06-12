from config import TILE_SIZE

class OutOfBoundsError(Exception):
    """Exception raised for trying to manipulate a tile outside of the grid.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TileOccupiedError(Exception):
    """Exception raised for trying to place an object on an occupied tile.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

type GridPoint = tuple[int, int]
type PixelPoint = tuple[int, int]

def to_pixel(grid_point: GridPoint):
    return PixelPoint(GridPoint[0]*TILE_SIZE, GridPoint[1]*TILE_SIZE)

def center(grid_point: GridPoint):
    return PixelPoint(GridPoint[0]*TILE_SIZE + TILE_SIZE//2, GridPoint[1]*TILE_SIZE+ TILE_SIZE//2)