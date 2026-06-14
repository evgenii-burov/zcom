import pygame
from config import COLOR_CURSOR, TILE_SIZE, FRAMERATE, GRID_WIDTH, GRID_HEIGHT
from grid.types import GridPoint, to_pixel
from math import sqrt

class Cursor:
    def __init__(self, position: GridPoint = (GRID_WIDTH//2, GRID_HEIGHT//2), hidden: bool = False):
        self.position = position
        self.hidden = hidden
        self.color = COLOR_CURSOR

        self.color_range = .25
        self.color_state = 0

        self.blink_timer = 0
        self.blink_interval = .5

    def draw(self, surface: pygame.Surface):
        if self.hidden:
            return
        center = to_pixel(self.position)
        center = (center[0] + TILE_SIZE/2, center[1] + TILE_SIZE/2)
        pygame.draw.circle(surface, self.color, center, TILE_SIZE / sqrt(2), 5)

    def update(self):
        # Glimmering cursor

        # Blinking cursor
        self.blink_timer += 1
        if self.blink_timer < FRAMERATE*self.blink_interval:
            return
        self.blink_timer = 0
        self.hidden = not self.hidden

    def move(self, grid_point: GridPoint, bounds: tuple[int, int]):
        new_x = grid_point[0] % bounds[0]
        new_y = grid_point[1] % bounds[1]
        self.position = (new_x, new_y)