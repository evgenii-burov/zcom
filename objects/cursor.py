import pygame
from .base import GameObject
from config import COLOR_CURSOR, TILE_SIZE, FRAMERATE
from util.types import Point, Direction, GridPoint
from util.grid import Grid, to_pixel
from math import sqrt

class Cursor(GameObject):
    def __init__(self, position: Point, hidden: bool, selected: bool, grid: Grid):
        super().__init__(position, hidden, selected)
        self.grid = grid
        self.color = COLOR_CURSOR

        self.color_range = .25
        self.color_state = 0

        self.blink_timer = 0
        self.blink_interval = .5

    def draw(self, surface: pygame.Surface):
        if self.hidden:
            return
        center = to_pixel(self.position).tuple()
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

    def move(self, direction: Direction, distance: int):
        self.hidden = False
        self.blink_timer = 0

        new_x = (self.position.x + direction.x * distance) % self.grid.width
        new_y = (self.position.y + direction.y * distance) % self.grid.height
        new_position = GridPoint(new_x, new_y)
        if self.grid.in_bounds(new_position):
            self.position = new_position


        # new_position = GridPoint(self.position.x + direction.x * distance, self.position.y + direction.y * distance)
        # if self.grid.in_bounds(new_position):
        #     self.position = new_position
        # else:
        #     new_x = self.position.x - direction.x * (self.grid.width - 1)
        #     new_y = self.position.y - direction.y * (self.grid.height - 1)
        #     new_position = GridPoint(new_x, new_y)
        #     self.position = new_position