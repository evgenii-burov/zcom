import pygame
from .base import GameObject
from config import COLOR_CURSOR, TILE_SIZE, FRAMERATE
from util.types import Point
from util.grid import to_pixel
from math import sqrt

class Cursor(GameObject):
    def __init__(self, position: Point, hidden: bool, selected: bool):
        super().__init__(position, hidden, selected)
        self.color = COLOR_CURSOR
        self.blink_timer = 0
        self.blink_interval = .5

    def draw(self, surface: pygame.Surface):
        center = to_pixel(self.position).tuple()
        center = (center[0] + TILE_SIZE/2, center[1] + TILE_SIZE/2)
        pygame.draw.circle(surface, self.color, center, TILE_SIZE / sqrt(2), 3)

    def update(self):
        self.blink_timer += 1
        if self.blink_timer < FRAMERATE*self.blink_interval:
            return
        self.blink_timer = 0
        self.hidden = not self.hidden