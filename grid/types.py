from config import TILE_SIZE

type GridPoint = tuple[int, int]
type PixelPoint = tuple[int, int]

def to_pixel(grid_point: GridPoint):
    return PixelPoint(GridPoint[0]*TILE_SIZE, GridPoint[1]*TILE_SIZE)

def center(grid_point: GridPoint):
    return PixelPoint(GridPoint[0]*TILE_SIZE + TILE_SIZE//2, GridPoint[1]*TILE_SIZE+ TILE_SIZE//2)